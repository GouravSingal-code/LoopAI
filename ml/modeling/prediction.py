
from utils.model_get_set_utils import get_model


model = get_model('lstmModel.pkl')


def prediction(data):
   return model.predict(data)
   
