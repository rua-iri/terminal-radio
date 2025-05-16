

import logging
from os import get_terminal_size, getpgid, killpg, setsid
import signal
import subprocess
import sys
import time
from colorama import Fore, Style
import climage
from PIL import Image
import requests
from io import BytesIO

from .utils import clear_screen, get_config


class Station:

    def __init__(
            self,
            name: str,
            url: str,
            img: str,
            is_yt: bool
    ) -> None:
        self.logger = logging.getLogger(__name__)
        config = get_config()
        self.USE_SIXEL = config.get("USE_SIXEL")

        self.is_yt = is_yt

        if self.is_yt:
            self.name, self.url, self.img = self.__fetch_yt_data(url=url)
        else:
            self.name = name
            self.url = url
            self.img = img

    def __fetch_yt_data(self, url: str):
        import yt_dlp

        self.logger.info("Fetching Youtube Data")

        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)

        self.logger.info("Youtube Data: ", info)

        for video_format in info.get("formats"):
            if video_format.get('resolution') == "audio only":
                break

        yt_stream_url = video_format.get('url')

        self.logger.info("Station Title: ", info.get('fulltitle'))
        self.logger.info("Station URL: ", yt_stream_url)

        if not yt_stream_url:
            raise Exception("Youtube Stream Not Found")

        img_url: str = info.get("thumbnail")

        return (
            info.get("fulltitle"),
            yt_stream_url,
            img_url
        )

    def __load_remote_image(self) -> Image.Image:
        headers = {
            "User-Agent": ""
        }
        res = requests.get(self.img, headers=headers)
        bytes_data = BytesIO(res.content)
        return Image.open(bytes_data).convert("RGBA")

    def __calc_terminal_size(self) -> tuple:
        COLS_PX_SCALE = 10
        TERMINAL_COLS, TERMINAL_LINES = get_terminal_size()

        return (
            TERMINAL_COLS * COLS_PX_SCALE,
            TERMINAL_LINES * COLS_PX_SCALE
        )

    def __display_sixel_image(self):

        try:
            TERMINAL_WIDTH, TERMINAL_HEIGHT = self.__calc_terminal_size()
            # print("TERMINAL_HEIGHT: ", TERMINAL_HEIGHT)
            # print("TERMINAL_WIDTH: ", TERMINAL_WIDTH)

            img: Image = self.__load_remote_image()
            IMAGE_WIDTH, IMAGE_HEIGHT = img.size
            # print("IMAGE WIDTH: ", IMAGE_WIDTH)
            # print("IMAGE HEIGHT: ", IMAGE_HEIGHT)

            img_filename: str = "/tmp/terminalradio_img.png"
            img.save(img_filename, format="PNG")
            sixel_command = ["img2sixel", img_filename]

            if IMAGE_HEIGHT >= IMAGE_WIDTH and IMAGE_HEIGHT > TERMINAL_HEIGHT:
                sixel_command.append(f"--height={TERMINAL_HEIGHT}")
            elif IMAGE_WIDTH > TERMINAL_WIDTH:
                sixel_command.append(f"--width={TERMINAL_WIDTH}")

            # print(sixel_command)
            subprocess.run(sixel_command)

        except Exception as e:
            self.logger.error(e, exc_info=True)
            PrintC().error(f"\n\nError: Unable to Load Image ({self.img})\n\n")

    def __display_default_logo(self):
        img_data = self.gen_logo()
        print(img_data)

    def gen_logo(self) -> str:
        TERMINAL_COLS, TERMINAL_LINES = get_terminal_size()
        img_width: int = int(TERMINAL_COLS)

        try:
            img: Image = self.__load_remote_image()

            img_output = climage.convert_pil(
                img=img,
                is_unicode=True,
                is_256color=True,
                width=img_width
            )

            return f"\n\n{img_output}\n\n"

        except Exception as e:
            self.logger.error(e, exc_info=True)
            PrintC().error(f"\n\nError: Unable to Load Image ({self.img})\n\n")
            return ""

    def display_image(self):
        clear_screen()

        if self.USE_SIXEL:
            self.__display_sixel_image()
        else:
            self.__display_default_logo()


class Player:

    def __init__(self) -> None:
        config = get_config()
        self.USE_SIXEL = config.get("USE_SIXEL")

        # self.__cmd = ("mpv -no-video --demuxer-lavf-o=hls_flags=+live+reload"
        #               " --audio-buffer=10 --cache=yes"
        #               " --demuxer-max-bytes=123400KiB"
        #               " --demuxer-readahead-secs=20 {}")
        self.__cmd = "mpv -no-video {}"

        if not config.get("DEBUG"):
            self.__cmd += " --really-quiet"

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
        message = "Refreshing Stream..."
        sys.stdout.write(message)
        sys.stdout.flush()

        self.stop()
        self.play(url=url)

        time.sleep(1)

        clear_message = " " * len(message)
        clear_message = "\r" + clear_message + "\r"
        sys.stdout.write(clear_message)

    def display_options(self, station_name: str):
        print("\nNow Playing: ", station_name, "\n")
        PrintC().error("Press 'q' to return to the menu")
        PrintC().info("Press 'r' to refresh the stream\n")


class PrintC:

    def __reset(self):
        print(Style.RESET_ALL)

    def error(self, message):
        print(Fore.RED + Style.BRIGHT + message)
        self.__reset()

    def info(self, message):
        print(Fore.BLUE + Style.BRIGHT + message)
        self.__reset()

    def success(self, message):
        print(Fore.GREEN + Style.BRIGHT + message)
        self.__reset()


class LoadingIcon:
    def __init__(self):
        self.cursor_symbol = '|/-\\'
        self.stop_animation = False

    def get_current_symbol(self, count: int):
        current_index = count % len(self.cursor_symbol)
        return self.cursor_symbol[current_index]

    def animate(self):
        current_index = 0
        while not self.stop_animation:
            current_cursor = self.get_current_symbol(current_index)

            sys.stdout.write(current_cursor)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b")

            current_index += 1

    def stop(self):
        # raise NotImplementedError("Method not yet implemented")
        self.stop_animation = True
        time.sleep(1)
        self.stop_animation = False
