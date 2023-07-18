import pickle,os

def save_model(model,location):
    with open(location, 'wb') as file:
        pickle.dump(model, file)


def get_model(location):
    with open(location, 'rb') as file:
        model = pickle.load(file)
    return model

