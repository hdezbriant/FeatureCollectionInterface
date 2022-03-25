import json
import unittest
import FeatureCollection as fc


class TestShelfInterface(unittest.TestCase):

    # test_facing_id = "01_N"

    def setUp(self):
        with open("geojson.json", "r") as geojson:
            geojson = json.load(geojson)
            self.test_fc = fc.FeatureCollection(geojson)
            self.test_feature_id = "01"

    def test_get_feature(self):
        test_feature = self.test_fc.get_feature(self.test_feature_id)
        self.assertEqual(test_feature.id, "01", 'Incorrect feature ID')
        self.assertEqual(test_feature.label, "shelf_01", 'Incorrect Label')

        for child in test_feature.children:
            self.assertEqual(child.__class__, list)

    # def test_get_feature(self):
    #     # test features when ID is correct:
    #     self.assertAlmostEqual(FeatureCollection.feature_finder())
