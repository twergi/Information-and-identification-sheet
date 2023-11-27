from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


class File:
    def __init__(self, filename: str, modtime: "datetime", size: int, filehash: str):
        self.filename = filename
        self.modtime = modtime
        self.size = size
        self.filehash = filehash


class FileData:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Person:
    def __init__(self, full_name: str, job_title: str):
        self.full_name = full_name
        self.job_title = job_title
