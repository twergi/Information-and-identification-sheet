from zlib import crc32
from os.path import exists
from os import mkdir

FS_SEPARATOR = "/"


def make_path(*args: str) -> str:
    result = ["."]

    for arg in args:
        result.append(arg)

    return FS_SEPARATOR.join(result)


def calculate_hash(filepath: str) -> str:
    file_hash = 0
    with open(filepath, "rb") as file:
        for line in file:
            file_hash = crc32(line, file_hash)

    return f"{file_hash:08X}"


def make_docx_from_filename(filename: str) -> str:
    return "".join(filename.split(".")[:-1]) + ".docx"


def check_or_create_folder(folderpath: str) -> bool:
    """
    If folder exists, returns `True`, otherwise creates folder and returns `False`
    """
    if exists(folderpath):
        return True

    print(f"Создание папки: {folderpath}")
    mkdir(folderpath)
    return False
