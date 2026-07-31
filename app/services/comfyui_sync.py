"""Sincronizacao automatica da URL do tunel do ComfyUI.

O Colab publica a URL atual do tunel num documento jsonblob.com,
e o Forge vigia esse documento e atualiza a config sozinho.
"""

import json
import threading
import time
import urllib.request


class ComfyUISync:
    """Compartilha a URL do tunel entre o Colab e o Forge."""

    BASE_URL = "https://jsonblob.com/api/jsonBlob"

    @staticmethod
    def create_link():
        """Cria um link de sincronizacao novo (jsonblob)."""
        data = json.dumps({"tunnel": ""}).encode("utf-8")
        req = urllib.request.Request(
            ComfyUISync.BASE_URL,
            data=data,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=20)
        location = resp.headers.get("Location", "")
        if location.startswith("http"):
            return location
        return "https://jsonblob.com" + location

    @staticmethod
    def read_link(link):
        """Le a URL do tunel publicada no link de sincronizacao."""
        req = urllib.request.Request(
            link,
            headers={"User-Agent": "project-forge"}
        )
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode("utf-8"))
        url = str(data.get("tunnel", "")).strip().rstrip("/")
        if url.startswith("http"):
            return url
        return None

    @staticmethod
    def url_alive(url):
        try:
            req = urllib.request.Request(
                f"{url}/system_stats",
                headers={"User-Agent": "project-forge"}
            )
            urllib.request.urlopen(req, timeout=6)
            return True
        except Exception:
            return False


class ComfyUISyncPoller(threading.Thread):
    """Vigia o link de sincronizacao e atualiza a config."""

    def __init__(self, config, interval=8):
        super().__init__(daemon=True)
        self.config = config
        self.interval = interval
        self._stop_flag = threading.Event()
        self.last_url = (
            config.config.get("comfyui", {})
            .get("server_url", "")
            .rstrip("/")
        )

    def stop(self):
        self._stop_flag.set()

    def run(self):
        while not self._stop_flag.wait(self.interval):
            link = (
                self.config.config.get("comfyui", {})
                .get("sync_url", "")
            )
            if not link:
                continue

            try:
                url = ComfyUISync.read_link(link)
                if not url or url == self.last_url:
                    continue

                if ComfyUISync.url_alive(url):
                    self.config.set(
                        "comfyui",
                        "server_url",
                        url
                    )
                    self.last_url = url
                    print(f"[tunel] nova URL detectada: {url}")
            except Exception:
                pass
