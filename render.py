

# Macast Metadata
# <macast.title>Your Player</macast.title>
# <macast.renderer>YR Renderer</macast.renderer>
# <macast.platform>win32</macast.platform>
# <macast.version>0.1</macast.version>
# <macast.author>wx c</macast.author>
# <macast.desc>支持DLNA投屏的插件</macast.desc>

# TODO
'''

# If there is an error in the media you play (for example, the file format is not supported), call this method
self.set_state_transport_error():

# ATTENTION: Not to call this method in the self.set_media_mute callback
# data : bool
self.set_state_mute(data):

# ATTENTION: Not to call this method in the self.set_media_volume callback
# data : int, range from 0 to 100
self.set_state_volume(data)
'''


import threading

from macast import Renderer, Setting, cli

from gxbzys.mpv import ShutdownError
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

    def set_media_stop(self):
        self.player.stop()

    def set_media_pause(self):
        self.player.pause = True

    def set_media_resume(self):
        self.player.pause = False

    def set_media_volume(self, data):
        """ data : int, range from 0 to 100
        """
        pass

    def set_media_mute(self, data):
        """ data : bool
        """
        pass

    def set_media_title(self, data):
        self.player.title = data

    def set_media_position(self, data):
        time_data: str = data
        time_array = time_data.split(':')
        time_array.reverse()
        seek_to: int = 0
        for i, t_str in enumerate(time_array):
            seek_to += pow(60, i) * int(t_str)
        self.player.seek(seek_to, reference="absolute")


class DLNARenderPlugin(Plugin):

    def __init__(self, smpv: SMPV):
        super().__init__(smpv)
        self.render:YRRenderer = None
        self.dlna_thread = None
        self.end_file_event_thread = None
        self.start_file_event_thread = None
        self.is_running = False

    def start(self):
        self.is_running = True
        super().start()
        self.render = YRRenderer(self.smpv)
        self.dlna_thread = threading.Thread(target=self.start_service)
        self.dlna_thread.start()

    def destroy(self):
        self.is_running = False
        self.uninstall_handlers()
        super().destroy()
        Setting.stop_service()

    def start_service(self):
        self.install_handlers()
        cli(self.render)

    def install_handlers(self):
        self.smpv.observe_property('duration', self.on_duration_changed)
        self.smpv.observe_property('time-pos', self.on_time_pos_changed)
        self.smpv.observe_property('pause', self.on_pause_status_changed)
        self.end_file_event_thread = threading.Thread(target=self.event_loop, args=('end-file', self.on_file_end,), daemon=True)
        self.end_file_event_thread.start()
        self.start_file_event_thread = threading.Thread(target=self.event_loop, args=('start-file', self.on_file_start,), daemon=True)
        self.start_file_event_thread.start()

    def uninstall_handlers(self):
        self.smpv.unobserve_property('duration', self.on_duration_changed)
        self.smpv.unobserve_property('time-pos', self.on_time_pos_changed)
        self.smpv.unobserve_property('pause', self.on_pause_status_changed)
        self.on_file_end()

    def on_duration_changed(self, *args):
        duration = self.smpv.duration
        if duration is None:
            return
        seconds = format_time(duration)
        self.render.set_state_duration(seconds)

    def on_time_pos_changed(self, *args):
        time_pos = self.smpv.time_pos
        if time_pos is None:
            return
        seconds = format_time(time_pos)
        self.render.set_state_position(seconds)

    def on_pause_status_changed(self, *args):
        print(args)
        if self.smpv.pause:
            self.render.set_state_transport('PAUSED_PLAYBACK')
        else:
            self.render.set_state_transport('PLAYING')

    def on_file_end(self, *args):
        self.render.set_state_transport('STOPPED')

    def on_file_start(self, *args):
        self.render.set_state_transport('PLAYING')

    def event_loop(self, event_name, handler):
        while self.is_running:
            try:
                self.smpv.wait_for_event(event_name)
                handler()
            except ShutdownError:
                break


def format_time(seconds) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)
