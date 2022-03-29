import cv2 as cv
import numpy as np
import json
import sys

class FeatureCollection:

    def __init__(self, geojson):
        # setting up lists to contain instances of the classes
        self.shelves = []
        self.facings = []

        # Create instances of Shelves and populating Facing list
        for feature in geojson['features']:
            if feature['properties']['type'] == "shelf":
                id = feature['properties']['id']
                label = feature['properties']['label']
                angle = feature['properties']['angle']
                coordinates = feature['geometry']['coordinates']

                self.shelves.append(Shelf(id, label, angle, coordinates))

        # Instantiating Facing object and populating facing list
        for feature in geojson['features']:
            if feature['properties']['type'] == "facing":
                id = feature['properties']['id']
                label = feature['properties']['label']
                coordinates = feature['geometry']['coordinates']
                startpoint = tuple(coordinates[0])
                endpoint = tuple(coordinates[1])
                parent = feature['properties']['parent']

                facing = Facing(id, label, coordinates, startpoint, endpoint)
                self.facings.append(facing)

                # Matching shelf parents and their facing children
                # Defaults to None if no parent
                # and [] if no children
                for shelf in self.shelves:
                    if parent == shelf.id:
                        shelf.children.append(facing)
                        facing.parent = shelf


    # Get a feature, using the given feature ID 
    def get_feature(self, input_feature_id: str) -> object:
        for feature in self.shelves:
            if feature.id == input_feature_id:
                print('\nFound:\n', feature)
                return feature
        for facing in self.facings:
            if facing.id == input_feature_id:
                print('\nFound:\n', feature)
                return facing

    # Get all shelves in collection
    def get_all_shelves(self) -> list:
        for shelf in self.shelves:
            print(shelf)
        return self.shelves

    # Get all facings in collection 
    def get_all_facings(self) -> list:
        for facing in self.facings:
            print(facing)
        return self.facings

    # Returns parent shelf feature of the given facing feature
    def get_parent_feature(self, input_feature) -> object:
        if input_feature.parent:
            print("\nFound parent:\n", input_feature.parent)
        else:
            print(input_feature.parent)
        return input_feature.parent

    # returns children facings of the given parent shelf
    def get_children_features(self, input_feature) -> list:
        for child in input_feature.children:
            print(child)
        return input_feature.children

# Combines Parent Shelf Label with Facing Label and returns it.
    # =============
    # This will not work correctly with the current structure in Prod
    # due to the lack of "preset" property in the sample GeoJSON provided
    # label = "shelf_01"   VS   (preset: "pharmacy" + _ + label: "01")

    def get_facing_compound_label(self, input_facing) -> str:
        compound_label = input_facing.parent.label + '_' + input_facing.label
        print(compound_label)
        return compound_label
    # =============

    def draw_shelves(self):
        img = np.zeros((400, 400, 3), dtype=np.uint8)
        coords_list = []
        for shelf in self.shelves:
           coords_list.append((np.array((shelf.coordinates[0]), np.int32).reshape((-1,1,2))))
        for pts in coords_list:
            cv.polylines(img, [pts*10], True, (255,0,0), 5)

        cv.imshow("Feature Collection", img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        return coords_list
                
    def draw_facings(self):
        img = np.zeros((400, 400, 3), dtype=np.uint8)
        line_list = []
        for facing in self.facings:
            line_list.append(tuple((facing.coordinates[0])))
            print(facing)
            print(line_list)
            pt0 = facing.startpoint
            pt1 = facing.startpoint
            pt2 = facing.startpoint
            pt3 = facing.startpoint

            cv.line(img, pt0, pt1, (255, 0, 0), 3)
            cv.line(img, pt1, pt2, (255, 0, 0), 3)
            cv.line(img, pt2, pt3, (255, 0, 0), 3)
            cv.line(img, (facing.endpoint[0]) * 10, (facing.startpoint[1]) * 10, (0,255,0), 3)

            # elif feature.__class__.__name__ == "Facing":
            #     for pts in features_list:
            #         print(pts.coordinates)
                    
            #         cv.line(img, ((pts.startpoint)*5), ((pts.endpoint)*5), (0,255,0), 3)
            #         cv.line(img, ((pts.endpoint)*5), ((pts.startpoint)*5), (0,255,0), 3)

    # ==========================================================
        #     # print(feature.coordinates)
            
        #     if feature == "facing":
        #             cv.line(img, shape.startpoint, shape.endpoint,(0,255,0),5)


    # def draw(self, feature_type):
    #     coords_list = []
    #     if feature_type == "1":
    #         for feature in self.shelves:
    #             print(feature)
    #             coords_list.append((np.array((feature.coordinates), np.int32).reshape((-1,1,2))))
    #     elif feature == "2":
    #         for feature in self.shelves:
    #             print(feature)
    #             coords_list.append((np.array((feature.coordinates), np.int32).reshape((-1,1,2))))
    #     img = np.zeros((700, 700, 3), dtype=np.uint8)

    #     for shape in coords_list:
    #         cv.polylines(img, [shape*8], True, (255,0,0), 3)

    #     cv.imshow("windowName", img)
    #     cv.waitKey(0)
    #     cv.destroyAllWindows()


# Sets up class which will provide some properties to subclasses
class Feature:
    def __init__(self, id, label):
        self.id = id
        self.label = label
        self.parent = None
        self.children = []

# Subclass for features with type Shelf
class Shelf(Feature):
    def __init__(self, id, label, angle, coordinates):
        super().__init__(id, label)
        self.angle = angle
        self.coordinates = coordinates

    def __str__(self):
        s = ('\n'
            '"type": %s\n'
            '"label": %s\n'
            '"id": %s\n'
            '"angle:" %s\n'
            '"coordinates": %s\n'
            '"parent": %s\n'
            '"children": %s\n')

        props = (
            self.__class__.__name__,
            self.label,
            self.id,
            self.angle,
            self.coordinates,
            self.parent,
            self.children)

        return s % props

# subclass for features with type Facing
class Facing(Feature):
    def __init__(self, id, label, coordinates, startpoint, endpoint):
        super().__init__(id, label)
        self.coordinates = coordinates
        self.startpoint = startpoint
        self.endpoint = endpoint

    def __str__(self):
        s = ('\n'
            '"type": %s\n'
            '"label": %s\n'
            '"id": %s\n'
            '"coordinates": %s\n'
            '"parent": %s\n'
            '"children": %s\n')

        props = (
            self.__class__.__name__,
            self.label,
            self.id,
            self.coordinates,
            self.parent.id,
            self.children)

        return s % props
