import json
import os
import shutil
from dataclasses import dataclass
from typing import Optional


@dataclass
class FileData:
    path: str
    dir: str
    name: str
    base: str
    ext: str
    content: Optional[str] = None


class FileUtils:

    @staticmethod
    async def create_folder_if_missing(path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def name_without_extension(path: str) -> str:
        return os.path.splitext(os.path.basename(path))[0]

    @staticmethod
    def extension(path: str) -> str:
        return os.path.splitext(os.path.basename(path))[1]

    @staticmethod
    async def read_file(path: str, exp_ext: Optional[str] = None) -> FileData:
        if not os.path.isfile(path):
            raise RuntimeError(f'file does not exist: {path}')

        filename = os.path.basename(path)
        split = os.path.splitext(filename)
        file_dir = os.path.dirname(path)

        if len(split) < 2:
            raise RuntimeError(f'could not parse filename {path}')
        ext = split[1]
        if exp_ext is not None and exp_ext != ext:
            raise RuntimeError(f'unexpected extensions: {ext}')
        return FileData(
            path=path,
            dir=file_dir,
            name=filename,
            base=split[0],
            ext=ext,
            content=await FileUtils.slurp_file(path)
        )

    @staticmethod
    async def slurp_paragraphs(file_path: str) -> list[str]:
        with open(file_path) as x:
            data = x.readlines()
        del x
        # get rid of newline chars
        data = [y.strip() for y in data]
        # get rid of empty lines
        data = list(filter(lambda z: z, data))
        return data

    @staticmethod
    async def slurp_file(file_path: str) -> str:
        with open(file_path) as x:
            return x.read()

    @staticmethod
    async def move_file_to_folder(file: str, target_dir: str):
        await FileUtils.create_folder_if_missing(target_dir)
        shutil.move(file, target_dir)

    @staticmethod
    async def files_in_folder(folder: str) -> list[str]:
        if not os.path.isdir(folder):
            raise f'folder {folder} is not directory'
        return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    @staticmethod
    async def write_to_new_file(text: str, file: str):
        if os.path.exists(file):
            raise f'file {file} already exists'
        with open(file, 'w') as file:
            file.write(text)

    @staticmethod
    async def parse_json(file: str, required: bool = False) -> Optional[dict]:
        if os.path.isfile(file):
            speaker_json_str = await FileUtils.slurp_file(file)
            return json.loads(speaker_json_str)
        else:
            if required is True:
                raise f'required file {file} not found'
            else:
                return None
