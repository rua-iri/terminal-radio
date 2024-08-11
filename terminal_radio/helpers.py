import climage


def initialise_logs(file_name: str):
    with open(file_name, "a") as file:
        file.write("\n\n-------------------------\n")


def load_station_logo(img_src: str) -> str:
    img_output = climage.convert(img_src)
    return img_output
