import os
import sys
import unittest
from mock import patch
from wrf4g.wrapper import PilotParams, WRF4GWrapper


class TestWrapper(unittest.TestCase):
    testargs = [
        "../../bin/wrf_wrapper.py",
        "test_experiment",
        "test_realization",
        "1",
        "2001-01-01_00:00:00",
        "2001-01-07_00:00:00",
        "0"
    ]

    os.environ["GW_HOSTNAME"] = "bender"
    os.environ["GW_JOB_ID"] = "0"
    os.environ["GW_RESTARTED"] = "0"

    @patch.object(sys, 'argv', testargs)
    def test_pilot_params(self):
        print(sys.argv)
        params = PilotParams(json="test_experiment/realization.json")
        print(params)


class TestWRF4GWrapper(unittest.TestCase):
    testargs = [
        "../../bin/wrf_wrapper.py",
        "test_experiment",
        "test_realization",
        "1",
        "2001-01-01_00:00:00",
        "2001-01-07_00:00:00",
        "0"
    ]
    @patch.object(sys, 'argv', testargs)
    def test_init(self):
        params = PilotParams(json="test_experiment/realization.json")
        self.wrf4g_wrapper = WRF4GWrapper(params)
        print(self.wrf4g_wrapper)
