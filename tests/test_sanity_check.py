
import collections
import os
import sys
import SocketServer
import multiprocessing
import time
import unittest
import mock


def patch_path():
    """
    Add files dir to PYTHONPATH, so we can import sanity_check.py
    """
    THIS_FILE = os.path.abspath(__file__)
    ROOT_DIR = os.path.split(os.path.split(THIS_FILE)[0])[0]

    sys.path.append(os.path.join(ROOT_DIR, 'files'))

patch_path()

import sanity_check

MockStatvfs = collections.namedtuple("MockStatvfs", ['f_bavail', 'f_blocks'])

class UrlopenResponse(object):
    def __init__(self, code):
        super(UrlopenResponse, self).__init__()
        self.code = code

    def getcode(self):
        return self.code


class TestSanityCheck(unittest.TestCase):

    def test_port_negative(self):
        # This port is reserved, and in low range so no one should use it
        self.assertFalse(sanity_check.check_port('localhost', 1023))

    def test_port_positive(self):
        # We can assume that SSH will be working w
        def run():
            server = SocketServer.TCPServer(('localhost', 10123), SocketServer.BaseRequestHandler)
            server.serve_forever()
        proc = multiprocessing.Process(target=run)
        try:
            proc.start()
            has_connection = False
            for ii in range(100):
                if sanity_check.check_port('localhost', 10123):
                    has_connection = True
                    time.sleep(.01)
                    break
            self.assertTrue(has_connection)
        finally:
            proc.terminate()

    def test_command_positive(self):
        self.assertTrue(sanity_check.check_command("echo 1"))

    def test_command_positive_and(self):
        self.assertTrue(sanity_check.check_command("echo 1 && echo 2"))

    def test_command_positive_redirect(self):
        self.assertTrue(sanity_check.check_command("echo foo canary bar | grep canary"))

    def test_command_negative(self):
        self.assertFalse(sanity_check.check_command("exit 1"))

    def test_command_negative_and(self):
        self.assertFalse(sanity_check.check_command("exit 1 && echo 1"))

    def test_command_negative_pipe(self):
        self.assertFalse(sanity_check.check_command("echo foo bar | grep canary"))

    def test_free_percentage(self):
        with mock.patch('os.statvfs') as patched_statvfs:
            patched_statvfs.return_value = MockStatvfs(2, 10)
            self.assertAlmostEqual(20, sanity_check.get_free_percentage_on_mount("/test"))
            patched_statvfs.assert_called_once_with("/test")

    def test_http_checker_positive_http(self):
        self.assertTrue(sanity_check.check_heartbeat_url("http://example.com"))

    def test_http_checker_positive_https(self):
        self.assertTrue(sanity_check.check_heartbeat_url("https://example.com"))

    def test_http_checker_negative_http(self):
        self.assertFalse(sanity_check.check_heartbeat_url("http://192.168.255.10"))

    def test_http_checker_negative_https(self):
        self.assertFalse(sanity_check.check_heartbeat_url("https://192.168.255.10"))

    def test_http_checker_statuscode_positive(self):
        with mock.patch('urllib2.urlopen') as patched_open:
            patched_open.return_value = UrlopenResponse(201)
            self.assertTrue(sanity_check.check_heartbeat_url("http://test"))
            patched_open.assert_called_once_with("http://test", timeout=1)

    def test_http_checker_statuscode_negative_100(self):
        with mock.patch('urllib2.urlopen') as patched_open:
            patched_open.return_value = UrlopenResponse(102)
            self.assertFalse(sanity_check.check_heartbeat_url("http://test"))
            patched_open.assert_called_once_with("http://test", timeout=1)

    def test_http_checker_statuscode_negative_500(self):
        with mock.patch('urllib2.urlopen') as patched_open:
            patched_open.return_value = UrlopenResponse(500)
            self.assertFalse(sanity_check.check_heartbeat_url("http://test"))
            patched_open.assert_called_once_with("http://test", timeout=1)

if __name__ == "__main__":
    unittest.main()