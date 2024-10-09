

import logging
from os import get_terminal_size, getpgid, killpg, setsid
import signal
import subprocess


class Station:

    def __init__(
            self,
            name: str,
            url: str,
            img: str,
            isYT: bool
    ) -> None:
        self.logger = logging.getLogger(__name__)

        self.isYT = isYT

        if self.isYT:
            self.name, self.url, self.img = self.__fetch_yt_data(url=url)
        else:
            self.name = name
            self.url = url
            self.img = img

    def __fetch_yt_data(self, url: str):
        import yt_dlp
        import requests

        self.logger.info("Fetching Youtube Data")

        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)

        self.logger.info("Youtube Data: ", info)

        yt_stream_url = info.get('formats')[0].get('url')

        self.logger.info("Station Title: ", info.get('fulltitle'))
        self.logger.info("Station URL: ", yt_stream_url)

        if not yt_stream_url:
            raise Exception("Youtube Stream Not Found")

        img_url: str = info.get("thumbnail")
        res: requests.Response = requests.get(img_url)
        img_filename: str = "resource/img/yt_img.jpg"

        with open(img_filename, 'wb') as img_file:
            img_file.write(res.content)

        return (
            info.get("fulltitle"),
            yt_stream_url,
            img_filename
        )

    def gen_logo(self) -> str:
        terminal_cols, terminal_lines = get_terminal_size()
        img_width: int = int(terminal_cols / 2)

        import climage
        img_output = climage.convert(
            filename=self.img,
            is_unicode=True,
            is_256color=True,
            width=img_width
        )
        return f"\n\n{img_output}\n\n"


class Player:

    def __init__(self) -> None:
        self.__cmd = "ffplay {} -nodisp -loglevel quiet -infbuf"
        self.process_id = None

    def play(self, url):
        process = subprocess.Popen(
            self.__cmd.format(url),
            stdout=subprocess.PIPE,
            shell=True,
            preexec_fn=setsid
        )
        self.process_id = process.pid

    def stop(self):
        if self.process_id:
            killpg(
                getpgid(self.process_id),
                signal.SIGTERM
            )

        self.process_id = None

    def restart(self, url):
        self.stop()
        self.play(url=url)
