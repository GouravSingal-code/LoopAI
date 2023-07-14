import pickle

def save_model(model):
    model_filename = "lstmModel.pkl"
    with open(model_filename, 'wb') as file:
        pickle.dump(model, file)


def get_model(name):
    # Load the model from the file
    with open(name, 'rb') as file:
        model = pickle.load(file)
    return model

