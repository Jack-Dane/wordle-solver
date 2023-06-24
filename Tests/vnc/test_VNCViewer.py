
from unittest import TestCase
from unittest.mock import patch, MagicMock

import socket

from wordle.vnc.VNCViewer import VNCViewer


MODULE_PATH = "wordle.vnc.VNCViewer."


@patch(MODULE_PATH + "time")
@patch(MODULE_PATH + "socket")
class Test_VNCViewer(TestCase):

    @patch(MODULE_PATH + "subprocess")
    def test_ok(self, subprocess, socket_, _time):
        socket_.create_connection.return_value.recv.side_effect = [
            b"abc", b"RFB 003.008\n"
        ]

        vncViewer = VNCViewer()

        self.assertEqual(
            subprocess.Popen.return_value,
            vncViewer._process
        )

    def test_failed_to_connect_to_vnc_server(self, socket_, _time):
        socket_.error = socket.error
        socket_.create_connection.side_effect = [
            MagicMock(), socket.error("Error")
        ] * 10
        socket_.create_connection.return_value.recv.side_effect = [
            b"abc"
        ] * 10

        with self.assertRaisesRegex(
            Exception,
            "Failed to connect to VNC server on port 5900"
        ):
            VNCViewer()
