import asyncio

from file_based_tts import FileBasedTts

if __name__ == '__main__':
    asyncio.run(FileBasedTts('en-US-AndrewMultilingualNeural').process_files('./data'))
    print('done')
