import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimated_price(area_m2, rooms, general_condition, heating, neighborhood):
    try:
        gen_cond_index = __data_columns.index(('general_condition_' + general_condition).lower())
    except:
        gen_cond_index = None
        if general_condition != 'Delimicna rekonstrukcija':
            print(f"'{general_condition}' was not recognized as correct value for general condition, so 'Standardna gradnja' was used.")
    try:
        heat_index = __data_columns.index(('heating_' + heating).lower())
    except:
        heat_index = None
        if heating != 'Centralno':
            print(f"'{heating}' was not recognized as correct value for heating, so 'Centralno' was used.")
    try:
        neighborhood_index = __data_columns.index(('neighborhood_' + neighborhood).lower())
    except:
        neighborhood_index = None
        print(f"'{neighborhood}' was not recognized as correct value for neighborhood, so 'Other' was used.")

    x = np.zeros(len(__data_columns))
    x[0] = area_m2
    x[1] = rooms
    if gen_cond_index:
        x[gen_cond_index] = 1
    if heat_index:
        x[heat_index] = 1
    if neighborhood_index:
        x[neighborhood_index] = 1
    
    return round(__model.predict([x])[0], 2)


def get_data_columns():
    return __data_columns

def get_location_names():
    return __locations

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations

    with open("belgrade_rpp/server/artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = [location[13:] for location in __data_columns[9:-6]]
    
    global __model
    if __model is None:
        with open('belgrade_rpp/server/artifacts/nekretnine_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")
    

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price(40, 2, "Novogradnja", "Centralno", "Vracar"))