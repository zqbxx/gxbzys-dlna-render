import threading

from macast import Renderer, Setting, cli

from gxbzys.plugin import Plugin
from gxbzys.smpv import SMPV


class YRRenderer(Renderer):

    def __init__(self, player: SMPV):
        super().__init__()
        self.player = player

    def set_media_url(self, url):
        self.player.stop()
        self.player.playlist_clear()
        self.player.playlist_append(url)
        self.player.playlist_pos = 0


class DLNARenderPlugin(Plugin):

    def __init__(self, smpv: SMPV):
        super().__init__(smpv)
        self.render = None

    def start(self):
        super().start()
        self.render = YRRenderer(self.smpv)
        threading.Thread(target=self.start_service).start()

    def destroy(self):
        super().destroy()
        Setting.stop_service()

    def start_service(self):
        cli(self.render)



