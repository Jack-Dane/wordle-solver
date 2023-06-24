
import os
import time
import subprocess

import socket

from wordle import ROOT_DIR


class VNCViewer:

    _VNC_PORT = 5900

    def __init__(self):
        configPath = os.path.join(ROOT_DIR, "vnc/config.vnc")
        self._waitForVNCServer()
        self._process = subprocess.Popen(
            ["vinagre", "-F", configPath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def _waitForVNCServer(self):
        attempts = 0
        while attempts < 20:
            try:
                connection = socket.create_connection(("localhost", 5900))
                protocolVersion = connection.recv(12).decode()

                if "RFB" in protocolVersion:
                    # protocol version handshake expected eg:
                    # RFB 003.008\n
                    # https://datatracker.ietf.org/doc/html/rfc6143#section-7.1.1
                    return

            except socket.error:
                pass

            attempts += 1
            time.sleep(.5)
            print("Failed to connect to VNC, trying again.")
        else:
            raise Exception(
                f"Failed to connect to VNC server on port {self._VNC_PORT}"
            )

    def kill(self):
        self._process.kill()
