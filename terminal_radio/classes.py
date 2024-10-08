

import logging


class Station:
    def __init__(self, name: str, url: str, img: str, isYT: bool):
        self.logger = logging.getLogger(__name__)

        self.isYT = isYT

        if self.isYT:
            self.name, self.url, self.img = self.fetch_yt_station(url=url)
        else:
            self.name = name
            self.url = url
            self.img = img

    def fetch_yt_station(self, url: str):
        import yt_dlp
        import requests

        self.logger.info("Fetching Youtube Data")

        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)

        self.logger.info("Youtube Data: ", info)

        yt_stream_url = info.get('formats')[0].get('url')

        if not yt_stream_url:
            raise Exception("Youtube Stream Not Found")

        img_url: str = info.get("thumbnail")
        res: requests.Response = requests.get(img_url)
        img_filename: str = "resource/img/yt_img.jpg"

        with open(img_filename, 'wb') as img_file:
            img_file.write(res.content)

        self.logger.info("Station Title: ", info.get('fulltitle'))
        self.logger.info("Station URL: ", yt_stream_url)

        return (
            info.get("fulltitle"),
            yt_stream_url,
            img_filename
        )
