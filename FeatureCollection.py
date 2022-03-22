class FeatureCollection:
    def __init__(self, geojson):
        self.shelves = []
        self.facings = []

        # Two passes
        # First pass, you can see which feature is of type Shelf, and create Shelf objects, storing
        # them in self.shelves
        for feature in geojson['features']:
            if feature['properties']['type'] == "shelf":
                id = feature['properties']['id']
                label = feature['properties']['label']
                angle = feature['properties']['angle']
                coordinates = feature['geometry']['coordinates']

                self.shelves.append(Shelf(id, label, angle, coordinates))

        # Second pass, you can see which ones are type Facing, and create Facing objects, storing
        # them in self.facings.
        for feature in geojson['features']:
            if feature['properties']['type'] == "facing":
                id = feature['properties']['id']
                label = feature['properties']['label']
                coordinates = feature['geometry']['coordinates']
                startpoint = tuple(coordinates[0])
                endpoint = tuple(coordinates[1])
                parent = feature['properties']['parent']

                facing = Facing(id, label, startpoint, endpoint)
                self.facings.append(facing)

                for shelf in self.shelves:
                    if parent == shelf.id:
                        shelf.children.append(facing)
                        facing.parent = shelf
        # Then, if the specific Facing object
        # has a parent, iterate through your shelves, adding this Facing to the parent shelf's facings and
        # adding the parent shelf to the facing as facing.parent

    def get_all_shelves(self):
        return self.shelves

    def get_all_facings(self):
        return self.facings

    def get_feature(self, input_feature_id):
        for feature in self.shelves:
            if feature.id == input_feature_id:
                return feature
        for facing in self.facings:
            if facing.id == input_feature_id:
                return facing

    def get_parent_feature(self, input_feature) -> object:
        return input_feature.parent

    def get_children_features(self, input_feature) -> list:
        return input_feature.children

    def get_facing_compound_label(self, input_facing) -> str:
        compound_label = input_facing.parent.label + '_' + input_facing.label
        return compound_label


class Feature:
    def __init__(self, id, label):
        self.id = id
        self.label = label
        self.parent = None
        self.children = []


class Shelf(Feature):
    def __init__(self, id, label, angle, coordinates):
        super().__init__(id, label)
        self.angle = angle
        self.coordinates = coordinates

    def draw():
        pass


class Facing(Feature):
    def __init__(self, id, label, startpoint, endpoint):
        super().__init__(id, label)
        self.startpoint = startpoint
        self.endpoint = endpoint

    def draw():
        pass
