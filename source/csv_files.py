from .models import File, FileData, Person
from .settings import ENCODING, DATE_FORMAT, TIME_FORMAT, TEMPLATE_TABLE, HEADER
import csv
from os.path import exists
from typing import Dict


def write_data_to_csv(filename: str, container: list[File]) -> int:
    print(f"Создание файла данных: {filename}")
    file = (
        open(filename, "w", encoding=ENCODING, newline="")
        if exists(filename)
        else open(filename, "x", encoding=ENCODING, newline="")
    )
    print("Запись данных:")
    csvwriter = csv.writer(file, delimiter=";")
    csvwriter.writerow(HEADER)
    counter = 0
    for entry in container:
        print(f"\t{entry.filename}")
        csvwriter.writerow(
            [
                entry.filename,
                entry.modtime.strftime(DATE_FORMAT),
                entry.modtime.strftime(TIME_FORMAT),
                entry.size,
                entry.filehash,
            ]
        )
        counter += 1

    file.close()
    print("Запись завершена")
    return counter


def create_template(filename: str, container: list[File]) -> None:
    print(f"Создание файла исходных данных")

    files_row = ["", ""] + [entry.filename for entry in container]

    with open(filename, "x", encoding=ENCODING, newline="") as file:
        writer = csv.writer(file, delimiter=";")

        writer.writerow(files_row)
        writer.writerows(TEMPLATE_TABLE)


def read_input_data(filepath: str) -> Dict[str, FileData]:
    print("Чтение исходных данных")
    data = dict()

    with open(filepath, "r", newline="", encoding=ENCODING) as file:
        reader = csv.reader(file, delimiter=";")

        filenames = reader.__next__()[2:]
        sections = reader.__next__()[2:]
        facilitynames = reader.__next__()[2:]
        documentnames = reader.__next__()[2:]
        documentcodes = reader.__next__()[2:]

        # skipping rows without data
        _ = reader.__next__()
        _ = reader.__next__()

        for i in range(len(filenames)):
            data[filenames[i]] = FileData(
                filename=filenames[i],
                section=sections[i],
                facilityname=facilitynames[i],
                documentname=documentnames[i],
                documentcode=documentcodes[i],
                persons=list(),
            )

        while True:
            try:
                row = reader.__next__()
            except StopIteration:
                break

            if len(data) <= 2:
                continue

            full_name, job_title, includes = row[0], row[1], row[2:]

            person = Person(full_name, job_title)

            for i in range(len(includes)):
                if includes[i].strip() != "+":
                    continue
                data[filenames[i]].persons.append(person)
    return data
