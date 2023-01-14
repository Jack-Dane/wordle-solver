
import os
import subprocess

from wordle import ROOT_DIR


class VNCViewer:

    def __init__(self):
        configPath = os.path.join(ROOT_DIR, "vnc/config.vnc")
        self._process = subprocess.Popen(
            ["vinagre", "-F", configPath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def kill(self):
        self._process.kill()