import pickle,os

def save_model(model,location):
    with open(os.path.abspath(location), 'wb') as file:
        pickle.dump(model, file)


def get_model(location):
    with open(os.path.abspath(location), 'rb') as file:
        model = pickle.load(file)
    return model

