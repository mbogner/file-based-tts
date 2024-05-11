from dataclasses import dataclass

import edge_tts

from utils.file_utils import FileUtils
from utils.time_utils import TimeUtils


class FileBasedTts:
    @dataclass
    class Paragraph:
        index: int
        text: str
        filename: str

    @dataclass
    class ProcessedFile:
        dir: str
        input: str
        paragraphs: list['FileBasedTts.Paragraph']

    def __init__(self, voice: str):
        self.voice: str = voice

    async def __speak_into_file(self, text: str, file_base_name: str, directory: str):
        communicate = edge_tts.Communicate(text, voice=self.voice)
        await communicate.save(f'{directory}/{file_base_name}.wav')

    @staticmethod
    async def __write_paragraph_to_file(text: str, file_base_name: str, directory: str):
        await FileUtils.write_to_new_file(text, f'{directory}/{file_base_name}.txt')

    @staticmethod
    def generation_filename(index, filename) -> str:
        formatted_line = '{:03d}'.format(index)
        file_without_extension = FileUtils.name_without_extension(filename)
        return f'{file_without_extension}-p{formatted_line}'

    async def __text_to_speech(self, session_dir: str, filename: str, file_path: str) -> ProcessedFile:
        text = await FileUtils.slurp_paragraphs(file_path)

        paragraphs: list[FileBasedTts.Paragraph] = []
        for index, paragraph in enumerate(text):
            await FileUtils.create_folder_if_missing(session_dir)
            file_base_name = FileBasedTts.generation_filename(index, filename)

            paragraphs.append(FileBasedTts.Paragraph(
                index=index, text=paragraph, filename=file_base_name
            ))

            await self.__speak_into_file(
                text=paragraph, file_base_name=file_base_name, directory=session_dir
            )
            await FileBasedTts.__write_paragraph_to_file(
                text=paragraph, file_base_name=file_base_name, directory=session_dir
            )

        await FileUtils.move_file_to_folder(file_path, session_dir)
        return FileBasedTts.ProcessedFile(
            dir=session_dir, input=filename, paragraphs=paragraphs
        )

    async def process_files(self, data_dir: str) -> list[ProcessedFile]:
        session = TimeUtils.utc_unix()
        session_dir = f'{data_dir}/{session}'
        print(f'session: {session}, dir: {session_dir}')

        all_processed: list[FileBasedTts.ProcessedFile] = []
        await FileUtils.create_folder_if_missing(data_dir)
        for filename in await FileUtils.files_in_folder(data_dir):
            file_path = f'{data_dir}/{filename}'
            print(f'processing {file_path}')
            processed = await self.__text_to_speech(session_dir, filename, file_path)
            all_processed.append(processed)
        return all_processed
