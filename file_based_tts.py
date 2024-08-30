import os
from dataclasses import dataclass

import edge_tts
import ffmpeg

from utils.file_utils import FileUtils


class Speaker:
    @dataclass
    class Paragraph:
        index: int
        text: str
        filename: str

    @dataclass
    class ProcessedFile:
        dir: str
        input: str
        paragraphs: list['Speaker.Paragraph']

    @dataclass
    class VoiceConfig:
        voice: str = 'en-US-AndrewMultilingualNeural'
        rate: str = "+0%"
        volume: str = "+0%"
        pitch: str = "+0Hz"

    @staticmethod
    async def __speak_into_file(text: str,
                                file_base_name: str,
                                directory: str,
                                voice_config: VoiceConfig):
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice_config.voice,
            rate=voice_config.rate,
            volume=voice_config.volume,
            pitch=voice_config.pitch
        )
        await communicate.save(f'{directory}/{file_base_name}.wav')

    @staticmethod
    async def __write_paragraph_to_file(text: str, file_base_name: str, directory: str):
        await FileUtils.write_to_new_file(text, f'{directory}/{file_base_name}.txt')

    @staticmethod
    def __create_output_filename(index, filename) -> str:
        formatted_line = '{:03d}'.format(index)
        file_without_extension = FileUtils.name_without_extension(filename)
        return f'{file_without_extension}-p{formatted_line}'

    @staticmethod
    async def __text_to_speech(session_dir: str,
                               filename: str,
                               file_path: str,
                               voice_config: VoiceConfig) -> ProcessedFile:
        text = await FileUtils.slurp_paragraphs(file_path)

        paragraphs: list[Speaker.Paragraph] = []
        for index, paragraph in enumerate(text):
            await FileUtils.create_folder_if_missing(session_dir)
            file_base_name = Speaker.__create_output_filename(index, filename)

            paragraphs.append(Speaker.Paragraph(
                index=index, text=paragraph, filename=file_base_name
            ))

            await Speaker.__speak_into_file(
                text=paragraph, file_base_name=file_base_name, directory=session_dir,
                voice_config=voice_config
            )
            await Speaker.__write_paragraph_to_file(
                text=paragraph, file_base_name=file_base_name, directory=session_dir
            )

        return Speaker.ProcessedFile(
            dir=session_dir, input=filename, paragraphs=paragraphs
        )

    @staticmethod
    async def read_files_from(data_dir: str,
                              session: int,
                              config_file: str,
                              voice_config: VoiceConfig = VoiceConfig()) -> list[ProcessedFile]:
        session_dir = f'{data_dir}/{session}'
        print(f'session: {session}, dir: {session_dir}, config_file: {config_file}')

        ext_conf = await FileUtils.parse_json(config_file)
        if ext_conf is not None:
            voice_config = Speaker.VoiceConfig(
                voice=ext_conf['voice'],
                rate=ext_conf['rate'],
                volume=ext_conf['volume'],
                pitch=ext_conf['pitch']
            )
            print(f'speaker json config: {voice_config}')

        all_processed: list[Speaker.ProcessedFile] = []
        await FileUtils.create_folder_if_missing(data_dir)
        file_in_folder = sorted(await FileUtils.files_in_folder(data_dir))
        for filename in file_in_folder:
            file_path = f'{data_dir}/{filename}'
            if filename == '.DS_Store':
                os.remove(file_path)
                continue
            print(f'processing {file_path}')
            processed = await Speaker.__text_to_speech(
                session_dir=session_dir, filename=filename, file_path=file_path,
                voice_config=voice_config)
            all_processed.append(processed)
        return all_processed

    @staticmethod
    async def wav_to_mp3(path_without_extension: str):
        wav = f'{path_without_extension}.wav'
        if os.path.isfile(wav):
            await ffmpeg.input(wav).output(f'{path_without_extension}.mp3').run(quiet=True)
        else:
            print(f'file {wav} does not exist')
