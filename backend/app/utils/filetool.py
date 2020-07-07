import os
import uuid
from datetime import datetime

from app.utils.response import ResponseCode
from app.utils.util import get_root_dir
from flask import send_from_directory
import json


class FileTool:
    __allowed_suffix = ["xlsx", "xls"]
    __size_limit = 10 ** 7
    __cnt_limit = 50
    __logger = None

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, logger):
        self.__logger = logger

    def __init__(self, user_name):
        self.user_dir = get_root_dir() / f"static/{user_name}"

    def save(self, file, res):
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)

        if not file:
            res.update(code=ResponseCode.NoFileFound)
            return res.data

        suffix = file.filename.split(".")[-1]
        if suffix not in FileTool.__allowed_suffix:
            res.update(code=ResponseCode.FileExtensionNotAllowed)
            return res.data

        if os.fstat(file.fileno()).st_size > FileTool.__size_limit:
            res.update(code=ResponseCode.FileSizeTooLarge)
            return res.data

        files = os.listdir(self.user_dir)
        if len(files) >= FileTool.__cnt_limit:
            res.update(code=ResponseCode.StorageFull)
            os.remove(self.user_dir / files[0])

        filename = (f"{datetime.now().strftime('%Y%m%d_%H%M%S')}-"
                    f"{str(uuid.uuid4().hex)}.{suffix}")
        file.save(self.user_dir / filename)
        res.update(data={'cnt': len(files),
                         'filename': filename})
        return res.data

    def get(self, filename="20200705_172504-e6eef7a541ab4eb7a632b62b8b636a7a.xlsx"):
        response = send_from_directory(self.user_dir, filename,
                                       as_attachment=True)
        return response
