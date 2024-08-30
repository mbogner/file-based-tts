import asyncio
import sys

from file_based_tts import Speaker
from utils.file_utils import FileUtils
from utils.time_utils import TimeUtils


async def run():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <folder_name>")
        return
    folder_name = sys.argv[1]
    session = TimeUtils.utc_unix()
    folders = (await FileUtils.parse_json(file=f"./{folder_name}/tts.json", required=True))['folders']
    for folder in folders:
        created_files = await Speaker.read_files_from(data_dir=folder['dir'], session=session,
                                                      config_file=folder['config'])
        print(f"done with {folder['dir']} - created {len(created_files)} files:")
        for created_file in created_files:
            for paragraph in created_file.paragraphs:
                p_file = f'{created_file.dir}/{paragraph.filename}'
                print(f" - {created_file.input}: {p_file}")
                await Speaker.wav_to_mp3(p_file)
    print('done')


if __name__ == '__main__':
    asyncio.run(run())
