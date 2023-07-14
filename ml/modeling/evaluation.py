from ml.data_preparation.data_loading import dataCreation
from ml.data_preparation.data_preprocessing import createInputFormat
from ml.modeling.model import model
from utils.train_test_data_utils import input_data, output_data
from utils.model_get_set_utils import get_model


model = get_model('lstmModel.pkl')

input_array , output_array = createInputFormat(dataCreation())
test_x = input_data(input_array, 'test')
test_y = output_data(output_array, 'test')


loss = model.evaluate(test_x, test_y)