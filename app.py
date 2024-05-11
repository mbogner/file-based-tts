import asyncio

from file_based_tts import Speaker
from utils.file_utils import FileUtils
from utils.time_utils import TimeUtils


async def run():
    session = TimeUtils.utc_unix()
    folders = (await FileUtils.parse_json(file="./data/tts.json", required=True))['folders']
    for folder in folders:
        await Speaker.read_files_from(data_dir=folder['dir'], session=session, config_file=folder['config'])
    print('done')


if __name__ == '__main__':
    asyncio.run(run())
