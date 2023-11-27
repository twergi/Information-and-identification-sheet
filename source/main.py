import os
from datetime import datetime
from .utils import calculate_hash, make_path, check_or_create_folder
from .template import create_result_document
from .models import File
from .settings import (
    SEARCH_FOLDER,
    OUTPUT_FOLDER,
    SIGNATURE_FOLDER,
    INPUT_DATA_FILENAME,
)
from .csv_files import create_template, read_input_data


def run() -> None:
    if not check_or_create_folder(SEARCH_FOLDER):
        print(
            f'Положите требуемые к оформлению файлы в "{SEARCH_FOLDER}" и запустите программу еще раз'
        )
        return

    print(f"Чтение директории: {SEARCH_FOLDER}")
    filenames = os.listdir(SEARCH_FOLDER)
    files: list[File] = list()

    print("Обработка файлов:")
    for filename in filenames:
        full_path = make_path(SEARCH_FOLDER, filename)

        if os.path.isdir(full_path):
            continue

        print(f"\t{filename}")
        info = os.lstat(full_path)

        files.append(
            File(
                filename,
                datetime.fromtimestamp(info.st_mtime),
                info.st_size,
                calculate_hash(full_path),
            )
        )

    check_or_create_folder(OUTPUT_FOLDER)
    check_or_create_folder(SIGNATURE_FOLDER)

    if not os.path.exists(INPUT_DATA_FILENAME):
        print(f"Не найден файл исходных данных: {INPUT_DATA_FILENAME}")
        create_template(INPUT_DATA_FILENAME, files)
        print(
            f'Заполните файл исходных данных "{INPUT_DATA_FILENAME}" и запустите программу еще раз'
        )
        return

    print(f"Найден файл исходных данных: {INPUT_DATA_FILENAME}")
    data = read_input_data(INPUT_DATA_FILENAME)

    for file in files:
        filedata = data.get(file.filename)

        if filedata is None:
            print(
                f"""В папке "{SEARCH_FOLDER}" найдены файлы, не присутствующие в "{INPUT_DATA_FILENAME}".
Удалите файл исходных данных и запустите программу снова."""
            )
            return

        filedata.filehash = file.filehash
        filedata.size = file.size
        filedata.modtime = file.modtime

    for filedata in data.values():
        create_result_document(filedata)
