import pickle
def read_dictionary_from_file():
    with open("ports.pkl", "rb") as file:
        my_dict_new = pickle.load(file)
        return my_dict_new