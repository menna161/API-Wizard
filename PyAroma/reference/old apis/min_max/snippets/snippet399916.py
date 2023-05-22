from pyspark import SparkConf
from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoderEstimator, StringIndexer, QuantileDiscretizer, MinMaxScaler
from pyspark.ml.linalg import VectorUDT, Vectors
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F


def ratingFeatures(ratingSamples):
    ratingSamples.printSchema()
    ratingSamples.show()
    movieFeatures = ratingSamples.groupBy('movieId').agg(F.count(F.lit(1)).alias('ratingCount'), F.avg('rating').alias('avgRating'), F.variance('rating').alias('ratingVar')).withColumn('avgRatingVec', udf((lambda x: Vectors.dense(x)), VectorUDT())('avgRating'))
    movieFeatures.show(10)
    ratingCountDiscretizer = QuantileDiscretizer(numBuckets=100, inputCol='ratingCount', outputCol='ratingCountBucket')
    ratingScaler = MinMaxScaler(inputCol='avgRatingVec', outputCol='scaleAvgRating')
    pipelineStage = [ratingCountDiscretizer, ratingScaler]
    featurePipeline = Pipeline(stages=pipelineStage)
    movieProcessedFeatures = featurePipeline.fit(movieFeatures).transform(movieFeatures)
    movieProcessedFeatures.show(10)
