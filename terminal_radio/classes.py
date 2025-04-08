

import logging
from os import get_terminal_size, getpgid, killpg, setsid
import signal
import subprocess
from colorama import Fore, Style
import climage
from PIL import Image
import requests
from io import BytesIO


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

    def display_sixel_image(self):

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
            self.logger.error(e)
            PrintC().error(f"\n\nError: Unable to Load Image ({self.img})\n\n")

    def display_default_logo(self):
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
            self.logger.error(e)
            PrintC().error(f"\n\nError: Unable to Load Image ({self.img})\n\n")
            return ""


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
