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

    # features_geojson = json.dumps(features_geojson['features'], indent = 2)
    # print(features_geojson)

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
        if selection == 1:
        # Get Feature by ID
            id_select = '''Which ID would you like to fetch?\n'''
            feature_id = input(id_select)
            FeatureCollection.get_feature(feature_id)

        elif selection == 2:
        # Get Parent Feature
            print("selected 2")

        elif selection == 3:
        # Get Children of a Feature
            print("selected 3")

        elif selection == 4:
        # Get all Shelves or Facings
            print("Selected 4")

        elif selection == 5:
        # Create compound label for facing
            print("Selected 5")

        elif selection == 6:
        # Exit program
            print("Exiting...")
            raise SystemExit()

    except ValueError:
        print(f"{selection} is not a valid choice. Please use the corresponding numbers to make a selection.")
        shelf_interface()


class FeatureCollection:
    def __init__(self, type, features) -> None:
        self.type = type
        self.features = features


    def get_feature(input_feature_id: str) -> None:
        for feature in features_geojson['features']:
            if feature['properties']['id'] == input_feature_id:
                feature = json.dumps(feature, indent = 2)
                print(feature)


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


# How to ingest json
# nad how to retrieve


    # get_parent_feature(input_feature: Feature) -> Optional [Feature]
    # given Feature Obj as input, retrieve parent Feature Obj, else None

    # get_children_features(input_feature: Feature) -> List[Feature]
    # given Feature obj as input, retrieve its children Feat Objs as List.
    # else return []

    # get_all_shelves() -> List[Feature]
    # get_all_facings() -> List[Feature]
    # Return ALL available Shelf or Facing objs as a List. Else None

    # get_facing_compound_label(facing: Facing) -> str
    # Return formatted string label of parent Shelf label + given Facing label
    # as {shelf_label}_{facing_label}, such as "shelf_01_N"

if __name__ == "__main__":
    # Loads geojson file for processing later
    with open(sys.argv[1], "r") as features_geojson:
        features_geojson = json.load(features_geojson)
        shelf_interface(features_geojson)
    