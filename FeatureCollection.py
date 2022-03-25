class FeatureCollection:
    def __init__(self, geojson):
        # setting up lists to contain instances of the classes
        self.shelves = []
        self.facings = []

        # iterating through geojson file and populating the shelves list
        for feature in geojson['features']:
            if feature['properties']['type'] == "shelf":
                id = feature['properties']['id']
                label = feature['properties']['label']
                angle = feature['properties']['angle']
                coordinates = feature['geometry']['coordinates']

                self.shelves.append(Shelf(id, label, angle, coordinates))

        # Second pass, instantiating Facing object and populating facing list
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
                for shelf in self.shelves:
                    if parent == shelf.id:
                        shelf.children.append(facing)
                        facing.parent = shelf


    # method to retrieve a feature given the feature ID 
    def get_feature(self, input_feature_id) -> None:
        for feature in self.shelves:
            if feature.id == input_feature_id:
                print(feature)
                return feature
        for facing in self.facings:
            if facing.id == input_feature_id:
                print(feature)
                return facing

    # retrieve all shelves in collection
    def get_all_shelves(self) -> list:
        for shelf in self.shelves:
            print(shelf)
        return self.shelves

    # retrieve fall facings in collection 
    def get_all_facings(self) -> list:
        for facing in self.facings:
            print(facing)
        return self.facings

    # returns parent shelf feature of the given facing feature
    def get_parent_feature(self, input_feature) -> None:
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

# sets up class which will provide some properties to subclasses
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

    def draw():
        pass


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

    def draw():
        pass
