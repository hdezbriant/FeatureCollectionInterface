import cv2 as cv
import numpy as np

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
    def get_feature(self, input_feature_id) -> str:
        for feature in self.shelves:
            if feature.id == input_feature_id:
                print('\nFound:\n', feature)
                return feature
        for facing in self.facings:
            if facing.id == input_feature_id:
                print('\nFound:\n', facing)
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
        print(input_feature.parent)
        return input_feature.parent

    # returns children facings of the given parent shelf
    def get_children_features(self, input_feature) -> list:
        for child in input_feature.children:
            print(child)
        return input_feature.children

    # Combines Parent Shelf Label with Facing Label and returns it.
    def get_facing_compound_label(self, input_facing) -> str:
        compound_label = input_facing.parent.label + '_' + input_facing.label
        print(compound_label)
        return compound_label

# Provides shared properties to subclasses
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

    # Method which provides some to class objects for readability
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

    # Draws all features with type "Shelf"
    def draw(self):
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

# subclass for features with type Facing
class Facing(Feature):
    def __init__(self, id, label, coordinates, startpoint, endpoint):
        super().__init__(id, label)
        self.coordinates = coordinates
        self.startpoint = startpoint
        self.endpoint = endpoint

    # Method which provides some to class objects for readability
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

     # Draws all features with type "Facing"
    def draw(self):
        img = np.zeros((400, 400, 3), dtype=np.uint8)
        for facing in self.facings:
            spt = tuple([(facing.startpoint[0])*10, (facing.startpoint[1]*10)])
            ept = tuple([(facing.endpoint[0])*10, (facing.endpoint[1]*10)])
            cv.line(img, spt, ept, (0, 2550, 0), 1)

        cv.imshow("Feature Collection", img)
        cv.waitKey(0)
        cv.destroyAllWindows()