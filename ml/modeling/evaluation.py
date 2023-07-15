import env
from utils.train_test_data_utils import input_data, output_data
from utils.model_get_set_utils import get_model

def evaluate_model(test_x, test_y):
    model = get_model('ml/modeling/' + env.MODEL_NAME + str(env.STEP_INTERPOLATION_VALUE))
    loss = model.evaluate(test_x, test_y)
    print("loss :", loss)
