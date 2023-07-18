import env
from modeling.model import model
from txt_get_set_utils import get_txt
from model_get_set_utils import save_model
from train_test_data_utils import input_data, output_data
from keras.layers import LSTM, Dense
from modeling.evaluation import evaluate_model

def train_model(input_array, output_array):
    train_x = input_data(input_array, 'train')
    train_y = output_data(output_array, 'train')
    test_x = input_data(input_array, 'test')
    test_y = output_data(output_array, 'test')
    print("training started")
    model.add(LSTM(units=50, return_sequences=True, input_shape=(train_x.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(train_x, train_y, epochs=10, batch_size=32)
    print("saving the model")
    save_model(model,env.PATH_DIR  + '\\ml\\modeling\\'+ env.MODEL_NAME + str(env.STEP_INTERPOLATION_VALUE))
    print("evaluating the model")
    evaluate_model(test_x, test_y)