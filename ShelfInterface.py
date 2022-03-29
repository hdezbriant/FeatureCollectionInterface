import json
import sys
import numpy as np
from FeatureCollection import FeatureCollection, Shelf, Facing

def shelf_interface(geojson):
    # Displays menu for user to select desired operation
    # (More or less could be considered simplified representation of API routes)
    menu = """Select one of the following options: 
    1. Retrieve Feature object by ID(if it exists).
    2. Retrieve Parent Feature object(if any).
    3. Show all children of a Feature Object(if any).
    4. Show all available Shelves or Facings, if they exist.
    5. Create full label for a Facing.
    6. Draw an image of the features in the geoJSON.
    7. Quit.\nEnter your selection: """

    selection = input(menu)

    # Handles user selection to perform chosen task.
    try:
        # Get Feature by ID
        if selection == "1":
            id_select = """Which ID would you like to fetch(Case-Sensitive)?\n"""
            feature_id = input(id_select)
            fc.get_feature(feature_id)

        # Get Parent of given Feature
        elif selection == "2":
            id_select = """Please enter the ID for the Child Feature object(Case-Sensitive):\n"""
            feature_id = input(id_select)
            input_feature = fc.get_feature(feature_id)
            fc.get_parent_feature(input_feature)   

        # Get Children of a Feature
        elif selection == "3":
            id_select = """Please enter the ID for the Parent Feature object(Case-Sensitive):\n"""
            feature_id = input(id_select)
            parent_feature = fc.get_feature(feature_id)
            fc.get_children_features(parent_feature)

        # Get all Shelves or Facings
        elif selection == "4":
            type_selection = """\nSelect one of the following:
            1. Get all Shelves
            2. Get all Facings
            Enter Selection:"""
            type_selection = int(input(type_selection))
            
            if type_selection == 1:
                fc.get_all_shelves()
            elif type_selection == 2:
                fc.get_all_facings()
            else:
                print("Invalid selection\n Exiting...")
                raise SystemExit()
            
        # Return formatted string label of parent Shelf label + given Facing label
        # as {shelf_label}_{facing_label}, such as "shelf_01_N"
        elif selection == "5":
            id_select = """Please enter the Facing ID(Case-Sensitve):\n"""
            facing_id = input(id_select)
            # Finds a given feature by ID and checks if it is a facing
            facing = fc.get_feature(facing_id)
            if facing.parent:
                fc.get_facing_compound_label(facing)
            elif facing.parent == None:
                print("Invalid ID\n Exiting...")
                raise SystemExit()

        # Draw Shelves/Facings in window with OpenCV
        elif selection == "6":
            feature_type = input("""\n1. Draw all shelves.
            2. Draw all facings\n""")
            if feature_type == "1":
                Shelf.draw(fc)               
            elif feature_type == "2":
                Facing.draw(fc)

        # Exit program
        elif selection == "7":
            print("Exiting...")
            raise SystemExit()

    except ValueError:
        print(f"Value Error. Use the corresponding numbers to make a selection.")
        raise SystemExit()    

if __name__ == "__main__":
    # Loading geojson and instantiating class objects
    fc = None
    with open(sys.argv[1], "r") as geojson:
        geojson = json.load(geojson)
        fc = FeatureCollection(geojson)
    shelf_interface(fc)
    