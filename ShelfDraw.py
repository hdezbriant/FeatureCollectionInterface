import cv2 as cv
import numpy as np
import math
import json
import sys


class ShelfDraw:

    def now():
        with open(sys.argv[1], "r") as geojson:
            coords_list = []
            geojson = json.load(geojson)
            for feature in geojson['features']:
                coords_list.append((np.array((feature['geometry']['coordinates']), np.int32).reshape((-1,1,2))))

            img = np.zeros((700, 700, 3), dtype=np.uint8)

            # coord_list = [[[30, 100], [120, 100], [100, 30], [30, 30], [30, 100]],
            # [[20, 10], [30, 10], [30, 0], [20, 0], [20, 10]]]
            # array_list = []
            # for coords in coord_list:
            #     array_list.append((np.array(coords).reshape((-1,1,2))))

            # coords = np.array([[30, 100], [120, 100], [100, 30], [30, 30], [30, 100]], np.int32)
            # coords = coords.reshape((-1, 1, 2))
            # square = np.array((coords), dtype=np.int32)
            # cv.line(img, (0,0), (300,300), (255,0,0), 2)
            for shape in coords_list:
                cv.polylines(img, [shape*13], True, (255,0,0), 1)
                
# ================== !STAY IN SCOPE! ============================
# TO DO:
# Figure out if Rectangle works better for this purpose
# Or using lines for everything. 
# 
# POLYLINES NOT SUITABLE
# FOCUS ON THE TWO BOXES.
# ================== !STAY IN SCOPE! ============================


            cv.imshow("windowName", img)
            cv.waitKey(0)
            cv.destroyAllWindows()

        # def drawthing(geojson):
    #     with open(geojson, "r") as feature_collection:
    #         collection_json = json.load(feature_collection)
    #         features = collection_json['features']

    #     img = np.zeros((512,512,3),np.int8)
    #     img[:] = 0,0,0

    #     def wtp(p, min_x, min_y, max_x, max_y):
    #         scale = 10
    #         c = tuple([(p[0]-min_x) * scale, (p[1] - min_y) * scale])
    #         c = tuple([round(c[0]), round((max_y - min_y) * scale - c[1])])
    #         return c

    #     max_x = -math.inf
    #     max_y = -math.inf
    #     min_x = math.inf
    #     min_y = math.inf
    #     for feature in features:
    #         if feature["properties"]["type"] == "shelf":
    #             for coordinates_pair in feature["geometry"]["coordinates"]:
    #                 for coordinates in coordinates_pair:
    #                     if max_x < coordinates[0]:
    #                         max_x = coordinates[0]
    #                     if max_y < coordinates[1]:
    #                         max_y = coordinates[1]
    #                     if min_x > coordinates[0]:
    #                         min_x = coordinates[0]
    #                     if min_y > coordinates[1]:
    #                         min_y = coordinates[1]

    #     img = np.ascontiguousarray(np.zeros([int(abs(max_y - min_y)*20) + 1, int(abs(max_x - min_x) * 20 + 1), 3], dtype=np.int32))

    #     for feature in features:
    #         if feature["properties"]["type"] == "shelf":
    #             coords = feature['geometry']['coordinates'][0]

    #             p0 = wtp(coords[0], min_x, min_y, max_x, max_y)
    #             p1 = wtp(coords[1], min_x, min_y, max_x, max_y)
    #             p2 = wtp(coords[2], min_x, min_y, max_x, max_y)
    #             p3 = wtp(coords[3], min_x, min_y, max_x, max_y)

    #             cv.line(img, p0, p1, (255, 0, 0), 3)
    #             cv.line(img, p1, p2, (255, 0, 0), 3)
    #             cv.line(img, p2, p3, (255, 0, 0), 3)
    #             cv.line(img, p3, p0, (255, 0, 0), 3)

    #     if img is not None:
    #         img = np.array(img, dtype='float32')

    #     cv.imshow("image", img)
    #     cv.waitKey(0)


if __name__ == "__main__":
    ShelfDraw.now()
