import json
import cv2 as cv
import sys
import math
import numpy as np
from FeatureCollection import FeatureCollection

def shelf_interface(features_geojson):

    # Displays menu for user to select desired operation
    menu = """Select one of the following options: 
    1. Retrieve Feature object by ID(if it exists).
    2. Retrieve Parent Feature object(if any).
    3. Show all children of a Feature Object(if any).
    4. Show all available Shelves or Facings, if they exist.
    5. Create full label for a Facing.
    6. Quit.\nEnter your selection: """

    selection = int(input(menu))

    # Handles user selection to perform chosen task.
    try:
        # Get Feature by ID
        if selection == 1:
            id_select = """Which ID would you like to fetch?\n"""
            feature_id = input(id_select)
            FeatureCollection.get_feature(feature_id)

        # Get Parent of given Feature
        elif selection == 2:
            id_select = """Please enter the ID for the Child Feature object:\n"""
            feature_id = input(id_select)

            # Finds the requested object and passes into Class method, if it exists
            child = FeatureCollection.feature_finder(feature_id)
            if child == None:
                print("Child not found.")
                return None
            elif child:
                FeatureCollection.get_parent_feature(child)
            

        # Get Children of a Feature
        elif selection == 3:
            id_select = """Please enter the ID for the Parent Feature object:\n"""
            feature_id = input(id_select)

            # Finds the requested object and passes into Class method, if it exists
            parent_feature = FeatureCollection.feature_finder(feature_id)
            if parent_feature == None:
                print("Parent Object does not exist.")
                return None
            elif parent_feature:
                FeatureCollection.get_children_features(parent_feature)

        # Get all Shelves or Facings
        elif selection == 4:
            type_selection = """Select one of the following:
            1. Get all Shelves
            2. Get all Facings
            Enter Selection:"""
            type_selection = int(input(type_selection))
            
            if type_selection == 1:
                FeatureCollection.get_all_shelves()
            elif type_selection == 2:
                FeatureCollection.get_all_facings()
            else:
                print("Invalid selection\n Exiting...")
                raise SystemExit()
            
        # Return formatted string label of parent Shelf label + given Facing label
        # as {shelf_label}_{facing_label}, such as "shelf_01_N"
        elif selection == 5:
            id_select = """Please enter the Facing ID:\n"""
            facing_id = input(id_select)

            # Targets a specified facing by ID
            facing = FeatureCollection.feature_finder(facing_id)
            if facing:
                FeatureCollection.get_facing_compound_label(facing)
            elif facing == None:
                print("Invalid ID\n Exiting...")
                raise SystemExit()

        # Exit program
        elif selection == 6:
            print("Exiting...")
            raise SystemExit()

    except ValueError:
        print(f"{selection} is not a valid choice. Please use the corresponding numbers to make a selection.")
        raise SystemExit()    

if __name__ == "__main__":
    # Loads geojson file for processing later
    with open(sys.argv[1], "r") as features_geojson:
        features_geojson = json.load(features_geojson)
        shelf_interface(features_geojson)
    