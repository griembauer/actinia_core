# -*- coding: utf-8 -*-
from actinia_core.resources.common.aws_sentinel_interface import AWSSentinel2AInterface
from actinia_core.resources.common.config import global_config
import unittest
from pprint import pprint
import magic
from urllib.request import urlopen

__license__ = "GPLv3"
__author__     = "Sören Gebbert"
__copyright__  = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


class AWSSentinelInterfaceTestCase(unittest.TestCase):
    """This class tests theAWS interface to collect download
    urls of sentinel data
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def validate_result(self, result, bands):

        for scene in result:
            for tile in scene["tiles"]:

                url = tile["info"]
                response = urlopen(url)
                mime_type = magic.from_buffer(response.read(256), mime=True).lower()
                print(mime_type)
                self.assertTrue(mime_type in ["text/plain"])

                url = tile["metadata"]
                response = urlopen(url)
                mime_type = magic.from_buffer(response.read(256), mime=True).lower()
                print(mime_type)
                self.assertTrue(mime_type in ["application/xml"] or mime_type in ["text/xml"])

                url = tile["preview"]
                response = urlopen(url)
                mime_type = magic.from_buffer(response.read(256), mime=True).lower()
                print(mime_type)
                self.assertTrue(mime_type in ["image/jpeg"])

                for band in bands:
                    url = tile[band]["public_url"]

                    # Download 256 bytes from the url and check its mimetype
                    response = urlopen(url)
                    mime_type = magic.from_buffer(response.read(256), mime=True).lower()
                    print(mime_type)

                    self.assertTrue(mime_type in ["image/jp2"])

    def test_query_for_sentinel_scenes_single_old(self):
        aws = AWSSentinel2AInterface(global_config)
        result = aws.get_sentinel_urls(["S2A_OPER_PRD_MSIL1C_PDMC_20151207T031157_R102_V20151207T003302_20151207T003302",],
                                       ["B12", "B08"])
        pprint(result)

        self.assertTrue("S2A_OPER_PRD_MSIL1C_PDMC_20151207T031157_R102_V20151207T003302_20151207T003302" in result[0]["product_id"])
        self.validate_result(result, ["B12", "B08"])


    def test_query_for_sentinel_scenes_single_old_geojson(self):
        aws = AWSSentinel2AInterface(global_config)
        result = aws.get_sentinel_urls(["S2A_OPER_PRD_MSIL1C_PDMC_20151207T031157_R102_V20151207T003302_20151207T003302",],
                                       ["B12", "B08"])
        pprint(result)

        self.assertTrue("S2A_OPER_PRD_MSIL1C_PDMC_20151207T031157_R102_V20151207T003302_20151207T003302" in result[0]["product_id"])

        for tile in result[0]["tiles"]:
            geojson = aws.get_sentinel_tile_footprint(tile)
            print(geojson)

    def test_query_for_sentinel_scenes_single_new(self):
        aws = AWSSentinel2AInterface(global_config)
        result = aws.get_sentinel_urls(["S2A_MSIL1C_20170212T104141_N0204_R008_T31TGJ_20170212T104138",],
                                       ["B12", "B08"])
        pprint(result)

        self.assertTrue("S2A_MSIL1C_20170212T104141_N0204_R008_T31TGJ_20170212T104138" in result[0]["product_id"])
        self.validate_result(result, ["B12", "B08"])

    def test_query_for_sentinel_scenes_single_new_safe(self):
        aws = AWSSentinel2AInterface(global_config)
        result = aws.get_sentinel_urls(["S2A_MSIL1C_20170212T104141_N0204_R008_T31TGJ_20170212T104138.SAFE",],
                                       ["B12", "B08"])
        pprint(result)

        self.assertTrue("S2A_MSIL1C_20170212T104141_N0204_R008_T31TGJ_20170212T104138" in result[0]["product_id"])
        self.validate_result(result, ["B12", "B08"])

    def test_query_for_sentinel_scenes_singler_eplacement_bug(self):
        aws = AWSSentinel2AInterface(global_config)
        result = aws.get_sentinel_urls(["S2A_MSIL1C_20171210T020751_N0206_R017_T50HPG_20171210T052001",],
                                       ["B12", "B08"])
        pprint(result)

        self.assertTrue("S2A_MSIL1C_20171210T020751_N0206_R017_T50HPG_20171210T052001" in result[0]["product_id"])
        self.validate_result(result, ["B12", "B08"])

    def test_query_for_sentinel_scenes_singler_eplacement_bug_2(self):
        aws = AWSSentinel2AInterface(global_config)
        result = aws.get_sentinel_urls(["S2A_OPER_PRD_MSIL1C_PDMC_20161031T014722_R087_V20161030T235752_20161030T235752",],
                                       ["B12", "B08"])
        pprint(result)

        self.assertTrue("S2A_OPER_PRD_MSIL1C_PDMC_20161031T014722_R087_V20161030T235752_20161030T235752" in result[0]["product_id"])
        self.validate_result(result, ["B12", "B08"])



    def test_query_for_sentinel_scenes_mutli_mixed(self):
        aws = AWSSentinel2AInterface(global_config)
        result = aws.get_sentinel_urls(["S2A_MSIL1C_20170202T090201_N0204_R007_T36TVT_20170202T090155",
                                        "S2A_OPER_PRD_MSIL1C_PDMC_20151207T031157_R102_V20151207T003302_20151207T003302",
                                        "S2A_MSIL1C_20170218T143751_N0204_R096_T20PRT_20170218T143931"],
                                        ["B04", "B08"])
        pprint(result)

        self.assertTrue("S2A_MSIL1C_20170202T090201_N0204_R007_T36TVT_20170202T090155" in result[0]["product_id"])
        self.assertTrue("S2A_OPER_PRD_MSIL1C_PDMC_20151207T031157_R102_V20151207T003302_20151207T003302" in result[1]["product_id"])
        self.assertTrue("S2A_MSIL1C_20170218T143751_N0204_R096_T20PRT_20170218T143931" in result[2]["product_id"])
        self.validate_result(result, ["B04", "B08"])

    def test_query_for_sentinel_scenes_single_error(self):
        aws = AWSSentinel2AInterface(global_config)

        try:
            result = aws.get_sentinel_urls(["S2A_MSIL1C_20170212T104141_N0204_R008_T31TGJ_20170212T104138_NOPE",],
                                           ["B12", "B08"])
            pprint(result)
            self.assertTrue(False, "The error was not found")
        except Exception as e:
            self.assertTrue(True, "An exception was raised for the correct reason: %s"%str(e))

    def test_query_for_sentinel_scenes_multi_error(self):
        aws = AWSSentinel2AInterface(global_config)

        try:
            result = aws.get_sentinel_urls(["S2A_MSIL1C_20170202T090201_N0204_R007_T36TVT_20170202T090155",
                                            "S2A_OPER_PRD_MSIL1C_PDMC_20151207T031157_R102_V20151207T003302_20151207T003302",
                                            "S2A_MSIL1C_20170218T143751_N0204_R096_T20PRT_20170218T143931_NOPE"],
                                            ["B04", "B08"])
            pprint(result)
            self.assertTrue(False, "The error was not found")
        except Exception as e:
            self.assertTrue(True, "An exception was raised for the correct reason: %s"%str(e))

    def test_query_for_sentinel_scenes_band_error(self):
        aws = AWSSentinel2AInterface(global_config)

        try:
            result = aws.get_sentinel_urls(["S2A_MSIL1C_20170212T104141_N0204_R008_T31TGJ_20170212T104138_NOPE",],
                                           ["B120", "B080"])
            # pprint(result)
            self.assertTrue(False, "The error was not found")
        except Exception as e:
            self.assertTrue(True, "An exception was raised for the correct reason: %s"%str(e))


if __name__ == '__main__':
    unittest.main()