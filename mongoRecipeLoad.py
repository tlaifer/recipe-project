import pymongo
import pandas as pd
import numpy as np
import ast
import mongoconnection

DATA_DIRECTORY = "/home/croce2/data/"

TECHNIQUES_LIST = [
    'bake',
    'barbecue',
    'blanch',
    'blend',
    'boil',
    'braise',
    'brine',
    'broil',
    'caramelize',
    'combine',
    'crock pot',
    'crush',
    'deglaze',
    'devein',
    'dice',
    'distill',
    'drain',
    'emulsify',
    'ferment',
    'freez',
    'fry',
    'grate',
    'griddle',
    'grill',
    'knead',
    'leaven',
    'marinate',
    'mash',
    'melt',
    'microwave',
    'parboil',
    'pickle',
    'poach',
    'pour',
    'pressure cook',
    'puree',
    'refrigerat',
    'roast',
    'saute',
    'scald',
    'scramble',
    'shred',
    'simmer',
    'skillet',
    'slow cook',
    'smoke',
    'smooth',
    'soak',
    'sous-vide',
    'steam',
    'stew',
    'strain',
    'tenderize',
    'thicken',
    'toast',
    'toss',
    'whip',
    'whisk'
    ]

#names from original data 
#add ingredient_tokens for ingredient indices
SELECTED_COLUMNS = [
    "id", 
    "name", 
    "contributor_id",
    "minutes", 
    "description", 
    "ingredients", 
    "techniques", 
    "steps"
    ]

COLUMN_RENAMES = {
    "id" : "recipeId",
    "name" : "recipeName", 
    "contributor_id" : "chefId"
    }    


def loadRecipes():

    #load into pandas from csv
    pp_df = pd.read_csv(DATA_DIRECTORY+"PP_recipes.csv")
    raw_df = pd.read_csv(DATA_DIRECTORY+"RAW_recipes.csv")
    print("Loaded data, now cleaning...")

    #join tables on recipe id and clean
    joined_df = pd.merge(pp_df, raw_df, on="id")
    joined_df = joined_df[SELECTED_COLUMNS]
    joined_df["techniques"] = joined_df["techniques"].apply(cleanTechniques)
    joined_df["ingredients"] = joined_df["ingredients"].apply(ast.literal_eval)
    joined_df["steps"] = joined_df["steps"].apply(ast.literal_eval)
    joined_df = joined_df.rename(columns=COLUMN_RENAMES)
    print("Data cleaned, ready for upload")

    mongoconnection.mongo_setup().insert_many(joined_df.to_dict('records'))
    print("Recipes loaded in MongoDb!")


def cleanTechniques(rawTechniqueArr):
    '''
    Input is string wrapped array with 1 or 0 if technique at that index is used
    Output is an array with string entries of techniques used
    Note: return indices array if we don't want to store strings in db
    '''
    indicesArr =  np.nonzero(ast.literal_eval(rawTechniqueArr))[0]
    return [TECHNIQUES_LIST[x] for x in indicesArr]

loadRecipes()