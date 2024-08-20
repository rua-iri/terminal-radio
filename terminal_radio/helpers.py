


def initialise_logs(file_name: str):
    try:
        with open(file_name, "a") as file:
            file.write("\n\n-------------------------\n")
    except Exception as e:
        raise e


def load_station_logo(img_src: str) -> str:
    try:
        import climage
        img_output = climage.convert(img_src)
        return img_output
    except Exception as e:
        raise e
