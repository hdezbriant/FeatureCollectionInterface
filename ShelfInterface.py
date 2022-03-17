import json
import numpy as np
import cv2

# loads image can be grayscale/color/w transparency
img = cv2.imread('./testimg.jpg', 1)
img = cv2.resize(img, (300, 300))

# shows image that was loaded in, str is window name
cv2.imshow('hello', img)
# time to wait for input before moving to next step. 0 = infinite
cv2.waitKey(0)
# closes window on key press
cv2.destroyAllWindows()


class FeatureCollection:
    def __init__(feature, type, geometry) -> None:
        pass

        # for i in features:
            # init w/:
                # geometry(?)
                # coords
                # properties(?)
                # id
                # angle?
                # label
                # type 
                # parent: default null


    # Need to define hierarchy
    #  FeatureCollection has n "Features"
        # "Features" have: [
        # {
            # "type": "Feature"(for all),
            # "geometry": {
            # "type": "Polygon", (for shelves) (or "LineString" for facing)
            # "coordinates": [
            #   [[0, 10], [10, 10], [10, 0], [0, 0], [0, 10]]
            # ]
        # },
        # "properties": {
            #  "id": "int",
            #  "angle": 0.0,
            #  "label": "shelf_01",
            #  "type": "shelf", ("LineString", or "")
            #  "parent": null
        #   }
        # },



    # get_feature(input_feature_id: str) -> Optional[Feature]
    # given ID of Feature as input, retrieve Feature Obj else return None

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