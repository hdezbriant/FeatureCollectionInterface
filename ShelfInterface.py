import json
import numpy as np
import cv2

# loads image can be grayscale/color/w transparency
img = cv2.imread('./testimg.jpg', 1)
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5 )

# shows image that was loaded in, str is window name
cv2.imshow('hello', img)
# time to wait for input before moving to next step. 0 = infinite
cv2.waitKey(0)
# closes window on key press
cv2.destroyAllWindows()


class FeatureCollection:
    def __init__(self) -> None:
        pass

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