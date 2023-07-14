import sys
sys.path.append('../data_preparation')
sys.path.append('../../utils')
from model import model

from data_preprocessing import createInputFormat
from data_loading import dataCreation
from model_get_set_utils import save_model
from train_test_data_utils import input_data, output_data
from keras.layers import LSTM, Dense


input_array , output_array = createInputFormat(dataCreation())
train_x = input_data(input_array, 'train')

train_y = output_data(output_array, 'train')


model.add(LSTM(units=50, return_sequences=True, input_shape=(train_x.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(train_x, train_y, epochs=1, batch_size=32)


save_model(model)
