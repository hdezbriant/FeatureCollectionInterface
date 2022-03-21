import json
import numpy as np
import cv2
import sys

# # loads image can be grayscale/color/w transparency
# img = cv2.imread('../testimg.jpg', 1)
# img = cv2.resize(img, (300, 300))

# # shows image that was loaded in, str is window name
# cv2.imshow('hello', img)
# # time to wait for input before moving to next step. 0 = infinite
# cv2.waitKey(0)
# # closes window on key press
# cv2.destroyAllWindows()

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


class FeatureCollection:
    def __init__(self, type, features) -> None:
        self.type = type
        self.features = features

    # Method to find any given feature and return it for further use
    def feature_finder(input_feature_id: str) -> None:
        for feature in features_geojson['features']:
            if feature['properties']['id'] == input_feature_id:
                return feature
            elif feature['properties']['id'] != input_feature_id:
                continue
            else:
                print(f"ID: {input_feature_id} not found.")
                return None

    # Method to retrieve Feature by ID and print it
    def get_feature(feature_id):
        for feature in features_geojson['features']:
            if feature['properties']['id'] == feature_id:
                pretty_feature = json.dumps(feature, indent = 2)
                print(pretty_feature)
                print("Feature found!")
                return feature

            elif feature['properties']['id'] != feature_id:
                continue
            else:
                print(f"ID: {feature_id} not found.")
                return None
                
    # given Feature Obj as input, retrieve parent Feature Obj, else None
    def get_parent_feature(input_feature: dict) -> None:
        childs_parent_id = input_feature['properties']['parent']
        if childs_parent_id:
            for feature in features_geojson['features']:
                if feature['properties']['id'] == childs_parent_id:
                    pretty_parent = json.dumps(feature, indent = 2)
                    print(pretty_parent)
                    print("Parent found!")
                    return feature
                elif feature['properties']['id'] != childs_parent_id:
                    continue
                else:
                    break
        else:
            print(f"This feature does not have a parent.")
            return None

    # Retrieve children of a chosen object
    def get_children_features(input_feature: dict) -> list:
        children_features = []
        parent_id = input_feature['properties']['id']
        for feature in features_geojson['features']:
            if feature['properties']['parent'] == parent_id:
                children_features.append(feature)
                continue
            elif feature['properties']['parent'] != parent_id:
                continue
            else:
                break
        children_features = json.dumps(children_features, indent = 2)
        print(children_features)
        return children_features

    # Retrieve all Shelf objects in file
    def get_all_shelves() -> list:
        all_shelves = []
        for feature in features_geojson['features']:
            if feature['properties']['type'] == "shelf":
                all_shelves.append(feature)
            elif feature['properties']['type'] != "shelf":
                continue
            else:
                break
        all_shelves = json.dumps(all_shelves, indent = 2)
        print(all_shelves)
        return all_shelves
                

    def get_all_facings() -> list:
        all_facings = []
        for feature in features_geojson['features']:
            if feature['properties']['type'] == "facing":
                all_facings.append(feature)
            elif feature['properties']['type'] != "facing":
                continue
            else:
                break
        all_facings = json.dumps(all_facings, indent = 2)
        print(all_facings)
        return all_facings

    # Combines Parent Shelf Label with Facing Label and returns it.
    # =============
    # This will not work correctly with the current structure in Prod
    # due to the lack of "preset" property in the sample GeoJSON provided
    # label = "shelf_01"   VS   (preset: "pharmacy" + _ + label: "01")

    def get_facing_compound_label(facing: dict) -> str:
        # Assigning Parent shelf and facing objects
        parent_shelf = FeatureCollection.get_parent_feature(facing)
        shelf_label = parent_shelf['properties']['label']
        facing_label = facing['properties']['label']

        # Concatenating labels.
        formatted_label = f"{shelf_label}_{facing_label}"
        print(f"Shelf Label: {formatted_label}")
        return formatted_label
    # =============

class Feature:
    def __init__(self, geometry, ) -> None:
        self.geometry = geometry

class geometry:
    def __init__(self, type, coordinates) -> None:
        self.type = type
        self.coordinates = coordinates

class properties:
    def __init__(self, id, angle, label, type, parent) -> None:
        self.id = id
        self.angle = angle
        self.label = label
        self.type = type
        self.parent = parent


if __name__ == "__main__":
    # Loads geojson file for processing later
    with open(sys.argv[1], "r") as features_geojson:
        features_geojson = json.load(features_geojson)
        shelf_interface(features_geojson)
    