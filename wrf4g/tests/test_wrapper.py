import mock
import os
import sys
import unittest
from os import stat, path
from collections import namedtuple
from wrf4g.wrapper import PilotParams, WRF4GWrapper


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


class MockStat(object):
    st_mode = 0


def mock_makedirs(idir):
    print("\nRunning os.makedirs({})".format(idir))


def mock_chmod(ifile, perm):
    print("\nRunning os.chmod({}, {})".format(ifile, perm))


def mock_stat(ifile):
    print("\nRunning os_stat({})".format(ifile))
    return MockStat()


def mock_chdir(idir):
    print("\nRunning os.chdir({})".format(idir))


def mock_rmtree(idir):
    print("\nRunning shutil.rmtree({})".format(idir))


def mock_copy_file(orig, dest):
    print("\nRunning copy_file with {} and {}".format(orig, dest))


def mock_shutil_copyfile(orig, dest):
    print("\nRunning shutil.copyfile with {} and {}".format(orig, dest))


def mock_extract_file(dest, to_path):
    print("\nExtracting file {} to {}".format(dest, to_path))


def mock_exec_cmd(app_cmd):
    print("\nExecuting command {}".format(app_cmd))


@mock.patch.object(sys, 'argv', testargs)
def get_wrf4g_wrapper():
    params = PilotParams(json="test_experiment/realization.json")
    return WRF4GWrapper(params)


class TestWRF4GWrapper(unittest.TestCase):
    @mock.patch('wrf4g.wrapper.os.makedirs', side_effect=mock_makedirs)
    @mock.patch('wrf4g.wrapper.os.chmod', side_effect=mock_chmod)
    @mock.patch('wrf4g.wrapper.os_stat', side_effect=mock_stat)
    @mock.patch('wrf4g.wrapper.os.chdir', side_effect=mock_chdir)
    @mock.patch('wrf4g.wrapper.shutil.rmtree', side_effect=mock_rmtree)
    @mock.patch('wrf4g.wrapper.shutil.copyfile',
                side_effect=mock_shutil_copyfile)
    @mock.patch('wrf4g.wrapper.copy_file', side_effect=mock_copy_file)
    @mock.patch('wrf4g.wrapper.extract', side_effect=mock_extract_file)
    @mock.patch('wrf4g.wrapper.exec_cmd', side_effect=mock_exec_cmd)
    def test_launch(self, *args):
        wrf4g_wrapper = get_wrf4g_wrapper()
        wrf4g_wrapper.launch()
