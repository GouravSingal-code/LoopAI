import env
from utils.model_get_set_utils import get_model

model = get_model('ml/modeling/' + env.MODEL_NAME + str(env.STEP_INTERPOLATION_VALUE))

def prediction(data):
   return model.predict(data)[0][0]
