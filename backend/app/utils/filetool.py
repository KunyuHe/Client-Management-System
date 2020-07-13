import os
import uuid
from datetime import datetime

import pandas as pd
from app.utils.response import ResponseCode
from app.utils.util import get_root_dir, create_dir
from flask import send_from_directory


class FileTool:
    __allowed_suffix = ["xlsx", "xls"]
    __size_limit = 10 ** 7
    __cnt_limit = 50

    def __init__(self, user_name):
        self.user_dir = get_root_dir() / f"static/{user_name}"

    def save(self, file, res):
        create_dir(self.user_dir)

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

    def process(self, filename, text):
        df = pd.read_excel(self.user_dir / filename)
        df = df.append({'input': text}, ignore_index=True)

        df.to_excel(self.user_dir / filename, index=False)

    def get(self, filename):
        response = send_from_directory(self.user_dir, filename,
                                       as_attachment=True)
        return response
