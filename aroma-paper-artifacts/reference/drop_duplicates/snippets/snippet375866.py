import time, warnings, os, sys
import re, math
import numpy as np
import pandas as pd
from autogluon.utils.tabular.utils.loaders import load_pd
from autogluon.utils.tabular.ml.constants import BINARY, MULTICLASS, REGRESSION
from google.cloud import storage
from google.cloud import automl_v1beta1 as automl
import google.cloud.automl_v1beta1.proto.data_types_pb2 as data_types
from google.oauth2 import service_account
from google.api_core import operations_v1


def gcptables_fit_predict(train_data, test_data, dataset_name, label_column, problem_type, output_directory, gcp_info, eval_metric=None, runtime_sec=3600, fit_model=True, model_name=None, make_predictions=True):
    " Use GCP AutoML tables for both fitting and prediction. \n        Returns all outputs of AbstractBaseline.fit(), AbstractBaseline.predict() as one big tuple, with one final element: class_order\n        Also takes in the same arguments as these methods, except for num_cores.\n        Other Args:\n            dataset_name: str Name\n                GCP data and outputs will be stored in GCS Storage Bucket under this name, should be unique for every GCP run on a new dataset.\n            gcp_info: dict of critical informtion regarding GCP configuration, project, and access keys.\n            fit_model: bool indicating whether or not to actually fit models using GCP AutoML Tables.\n                If a previous run of this function crashed after the model had been trained, then you just produce predictions via: \n                fit_model = False. Similarly, you can set this False in order to get predictions in a separate process from the fit() call.\n                When False, you must specify: model_name as the string corresponding to the model.name entry from previous fit(),\n                but without the project/path prefix (this thus matches the display name of the model in the GCP console).\n            make_predictions: bool indicating whether or not we should return after fit() without making predictions.\n    \n        Note: For classification, your class labels cannot end with suffix: '_score'\n    "
    train_data = train_data.copy()
    test_data = test_data.copy()
    label_column_index = train_data.columns.get_loc(label_column)
    train_data.columns = [re.sub('\\W+', '_', col) for col in train_data.columns.tolist()]
    test_data.columns = [re.sub('\\W+', '_', col) for col in test_data.columns.tolist()]
    label_column = train_data.columns[label_column_index]
    train_data[id_column] = list(train_data.index)
    test_data[id_column] = list(test_data.index)
    data_colnames = list(set(train_data.columns))
    if (label_column in test_data.columns):
        test_data = test_data.drop([label_column], axis=1)
    og_dataset_name = dataset_name
    dataset_name = re.sub('\\W+', '_', dataset_name)
    dataset_name = dataset_name[:(GCP_DISPLAY_NAME_MAXCHARS - len(GCP_MODEL_PREFIX))]
    if (model_name is None):
        model_display_name = (GCP_MODEL_PREFIX + dataset_name)
    else:
        model_display_name = model_name
    if (og_dataset_name != dataset_name):
        print(('GCP will complain about provided dataset_name, renamed to: %s' % dataset_name))
    PROJECT_ID = gcp_info['PROJECT_ID']
    BUCKET_NAME = gcp_info['BUCKET_NAME']
    COMPUTE_REGION = gcp_info['COMPUTE_REGION']
    GOOGLE_APPLICATION_CREDENTIALS = gcp_info['GOOGLE_APPLICATION_CREDENTIALS']
    num_models_trained = None
    num_models_ensemble = None
    fit_time = None
    y_pred = None
    y_prob = None
    predict_time = None
    class_order = None
    if (len(train_data) < 1000):
        raise ValueError('GCP AutoML tables can only be trained on datasets with >= 1000 rows')
    storage_client = storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
    bucket = storage_client.get_bucket(BUCKET_NAME)
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
    automl_client = automl.AutoMlClient(credentials=credentials)
    tables_client = automl.TablesClient(project=PROJECT_ID, region=COMPUTE_REGION, credentials=credentials)
    if (not os.path.exists(output_directory)):
        os.makedirs(output_directory)
    gcs_train_path = ((dataset_name + '/') + GCS_TRAIN_FILENAME)
    train_file_exists = storage.Blob(bucket=bucket, name=gcs_train_path).exists(storage_client)
    if (not train_file_exists):
        print('Uploading training data')
        train_file_path = (output_directory + GCS_TRAIN_FILENAME)
        train_data.to_csv(train_file_path, index=False)
        blob = bucket.blob(gcs_train_path)
        blob.upload_from_filename(train_file_path)
    else:
        print('Training data already uploaded')
    gcs_test_path = ((dataset_name + '/') + GCS_TEST_FILENAME)
    test_file_exists = storage.Blob(bucket=bucket, name=gcs_test_path).exists(storage_client)
    if (not test_file_exists):
        print('Uploading test data')
        test_file_path = (output_directory + GCS_TEST_FILENAME)
        test_data.to_csv(test_file_path, index=False)
        blob = bucket.blob(gcs_test_path)
        blob.upload_from_filename(test_file_path)
    else:
        print('Test data already uploaded')
    if (not train_file_exists):
        os.remove(train_file_path)
    if (not test_file_exists):
        os.remove(test_file_path)
    dataset = tables_client.create_dataset(dataset_display_name=dataset_name)
    tables_dataset_name = dataset.name
    import_data_response = tables_client.import_data(dataset=dataset, gcs_input_uris=(((GCS_PREFIX + BUCKET_NAME) + '/') + gcs_train_path))
    print('Dataset import operation: {}'.format(import_data_response.operation))
    print('Dataset import response: {}'.format(import_data_response.result()))
    list_table_specs_response = tables_client.list_table_specs(dataset=dataset)
    table_specs = [s for s in list_table_specs_response]
    print(table_specs)
    if (problem_type in [BINARY, MULTICLASS]):
        type_code = 'CATEGORY'
        update_column_response = tables_client.update_column_spec(dataset=dataset, column_spec_display_name=label_column, type_code=type_code, nullable=False)
        print(update_column_response)
    update_dataset_response = tables_client.set_target_column(dataset=dataset, column_spec_display_name=label_column)
    print(update_dataset_response)
    gcp_metric = None
    if fit_model:
        if (eval_metric is not None):
            metrics_map = {'accuracy': 'MINIMIZE_LOG_LOSS', 'f1': 'MAXIMIZE_AU_PRC', 'log_loss': 'MINIMIZE_LOG_LOSS', 'roc_auc': 'MAXIMIZE_AU_ROC', 'balanced_accuracy': 'MAXIMIZE_AU_ROC', 'precision': 'MAXIMIZE_PRECISION_AT_RECALL', 'recall': 'MAXIMIZE_RECALL_AT_PRECISION', 'mean_squared_error': 'MINIMIZE_RMSE', 'median_absolute_error': 'MINIMIZE_MAE', 'mean_absolute_error': 'MINIMIZE_MAE', 'r2': 'MINIMIZE_RMSE'}
            if (eval_metric in metrics_map):
                gcp_metric = metrics_map[eval_metric]
        else:
            warnings.warn(('Unknown metric will not be used by GCP AutoML Tables: %s' % eval_metric))
        t0 = time.time()
        model_train_hours = math.ceil((runtime_sec / 3600.0))
        print(('Training model for %s hours' % model_train_hours))
        print(('Training model with name: %s' % model_display_name))
        create_model_response = tables_client.create_model(model_display_name=model_display_name, dataset=dataset, train_budget_milli_node_hours=(model_train_hours * 1000), optimization_objective=gcp_metric, exclude_column_spec_names=[id_column, label_column])
        operation_id = create_model_response.operation.name
        print('Create GCP model operation: {}'.format(create_model_response.operation))
        check_interval = 60
        keep_checking = True
        check_time = time.time()
        while keep_checking:
            if ((time.time() - check_time) > check_interval):
                api = operations_v1.OperationsClient(channel=automl_client.transport.channel)
                status_update = api.get_operation(operation_id)
                print('Status update on GCP model: \n {}'.format(status_update))
                print(('Time Elapsed: %s of %s' % ((time.time() - t0), runtime_sec)))
                check_time = time.time()
                if (hasattr(status_update, 'done') and status_update.done):
                    keep_checking = False
        model = create_model_response.result()
        model_name = model.name
        print(('GCP training completed, produced model object with name: %s' % model_name))
        print(('You can use this trained model for batch prediction by specifying model_name=%s' % model_display_name))
        print(model)
        t1 = time.time()
        fit_time = (t1 - t0)
        print(('GCP Tables Model fit complete, runtime: %s' % fit_time))
        print(('GCP model name = %s' % model_name))
    else:
        fit_time = None
        print('Skipping GCP Tables Model fit, just using trained model for prediction')
        if (model_name is None):
            raise ValueError('When fit_model=False,\xa0model_name must be specified.')
        model = tables_client.get_model(model_display_name=model_name)
    num_models_trained = (- 1)
    num_models_ensemble = (- 1)
    summary_list = tables_client.list_model_evaluations(model=model)
    model_eval_summaries = [s for s in summary_list]
    if (problem_type in [BINARY, MULTICLASS]):
        log_losses = [model_eval_summaries[(i + 1)].classification_evaluation_metrics.log_loss for i in range((len(model_eval_summaries) - 1))]
        log_loss = np.mean(np.array(log_losses))
        print(('Validation log_loss = %s' % log_loss))
    if (problem_type == BINARY):
        auc_rocs = [model_eval_summaries[(i + 1)].classification_evaluation_metrics.au_roc for i in range((len(model_eval_summaries) - 1))]
        auc_roc = np.mean(np.array(auc_rocs))
        print(('Validation AUC_ROC = %s' % auc_roc))
    if (not make_predictions):
        print(('Skipping predictions, set model_name = %s to use this trained model for prediction later on' % model_name))
        return (num_models_trained, num_models_ensemble, fit_time, y_pred, y_prob, predict_time, class_order)
    t2 = time.time()
    preds_file_prefix = ((((GCS_PREFIX + BUCKET_NAME) + '/') + dataset_name) + '/pred')
    batch_predict_response = tables_client.batch_predict(model=model, gcs_input_uris=(((GCS_PREFIX + BUCKET_NAME) + '/') + gcs_test_path), gcs_output_uri_prefix=preds_file_prefix)
    print('Batch prediction operation: {}'.format(batch_predict_response.operation))
    batch_predict_result = batch_predict_response.result()
    print(batch_predict_response.metadata)
    t3 = time.time()
    predict_time = (t3 - t2)
    preds_gcs_folder = batch_predict_response.metadata.batch_predict_details.output_info.gcs_output_directory
    preds_gcs_filename = 'tables_1.csv'
    preds_gcs_file = ((preds_gcs_folder + '/') + preds_gcs_filename)
    local_preds_file = (output_directory + LOCAL_PREDS_FILENAME)
    with open(local_preds_file, 'wb') as file_obj:
        storage_client.download_blob_to_file(preds_gcs_file, file_obj)
    test_pred_df = load_pd.load(local_preds_file)
    same_cols = [col for col in test_pred_df.columns if (col in data_colnames)]
    keep_cols = [col for col in test_pred_df.columns if (col not in data_colnames)]
    original_gcp_length = len(test_pred_df)
    original_test_length = len(test_data)
    print('test orig:')
    print(test_data)
    print('before dedupe...')
    print(test_pred_df)
    test_pred_df = test_pred_df.drop_duplicates(subset=[id_column])
    print('before merge...')
    print(test_pred_df)
    test_pred_df = test_data.merge(test_pred_df, on=[id_column], how='left')
    print('after merge...')
    print(test_pred_df)
    test_pred_df = test_pred_df[keep_cols]
    if (len(test_pred_df) != len(test_data)):
        warnings.warn('GCP failed to produce predictions for some test data rows')
        print(('diff: %s | %s' % (len(test_pred_df), len(test_data))))
        print('DIFF ORIGINAL:')
        print(original_test_length)
        print(original_gcp_length)
    if (problem_type != REGRESSION):
        gcp_classes = list(test_pred_df.columns)
        og_classes = list(train_data[label_column].unique())
        print('Num Classes orig:', len(og_classes))
        print('Num Classes GCP: ', len(gcp_classes))
        print('GCP Class Names                 : ', gcp_classes)
        print('Original Class Names            : ', og_classes)
        orig_colnames = [column[(len(label_column) + 1):(- len('_score'))] for column in gcp_classes]
        print('Original Class Names (Reordered): ', orig_colnames)
        if (len(gcp_classes) != len(og_classes)):
            warnings.warn('GCP AutoML Tables predictions are missing classes')
            raise AssertionError(('GCP AutoML did not predict with all classes! GCP returned %s of %s classes!' % (len(gcp_classes), len(og_classes))))
        test_pred_df.columns = orig_colnames
    else:
        test_pred_df.columns = [label_column]
    if test_pred_df.isnull().values.any():
        test_pred_df = impute_dummy_predictor(test_pred_df=test_pred_df, train_data=train_data, label_column=label_column, problem_type=problem_type)
    if (problem_type == REGRESSION):
        if (len(keep_cols) != 1):
            warnings.warn('GCP AutoML Tables regression predictions are incorrectly formatted')
            print('keep_cols:', keep_cols)
            raise AssertionError(('GCP AutoML did not return a valid regression prediction! GCP returned %s of %s classes!' % (len(keep_cols), 1)))
        y_pred = test_pred_df[label_column]
        y_prob = None
        return (num_models_trained, num_models_ensemble, fit_time, y_pred, y_prob, predict_time, class_order)
    else:
        y_pred = test_pred_df.idxmax(axis=1)
        class_order = list(test_pred_df.columns)
        y_prob = np.array(test_pred_df)
        return (num_models_trained, num_models_ensemble, fit_time, y_pred, y_prob, predict_time, class_order)
