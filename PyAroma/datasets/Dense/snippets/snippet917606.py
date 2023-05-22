from keras import backend
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from model.root.traditional.root_rnn import RootRnn


def _training__(self):
    self.model = Sequential()
    self.model.add(LSTM(units=self.hidden_sizes[0], return_sequences=True, input_shape=(None, 1), activation=self.activations[0]))
    self.model.add(LSTM(units=self.hidden_sizes[1], activation=self.activations[1]))
    self.model.add(Dense(units=1, activation=self.activations[2]))
    self.model.compile(loss=self.loss, optimizer=self.optimizer)
    backend.set_session(backend.tf.Session(config=backend.tf.ConfigProto(intra_op_parallelism_threads=2, inter_op_parallelism_threads=2)))
    ml = self.model.fit(self.X_train, self.y_train, epochs=self.epoch, batch_size=self.batch_size, verbose=self.print_train)
    self.loss_train = ml.history['loss']
