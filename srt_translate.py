import asyncio
import sys
from dataclasses import dataclass

from deep_translator import GoogleTranslator

from utils.file_utils import FileUtils, FileData

translations = ['de', 'hi', 'zh-CN', 'ru', ]
translators = [
    GoogleTranslator(source='en', target=lang) for lang in translations
]


@dataclass(frozen=True)
class SRTEntry:
    timecode: str
    text: str

    def translate(self, translator: GoogleTranslator):
        return SRTEntry(
            timecode=self.timecode,
            text=translator.translate(self.text)
        )


@dataclass(frozen=True)
class SRT:
    entries: list[SRTEntry]

    def translate(self, translator: GoogleTranslator):
        return SRT(entries=[entry.translate(translator) for entry in self.entries])

    def write_to(self, path: str):
        with open(path, 'w') as out_file:
            for i, entry in enumerate(self.entries):
                out_file.write(f'{i}\n')
                out_file.write(f'{entry.timecode}\n')
                out_file.write(f'{entry.text}\n')
                if i < len(self.entries) - 1:
                    out_file.write('\n')


async def parse_srt_file(text: str) -> SRT:
    lines = text.split('\n')
    line_cnt = len(lines)
    if line_cnt % 4 != 0:
        raise RuntimeError('srt file has to have format:\n0: id\n1: timecode\n2: text\n3: newline separator\n')

    srt_entries: list[SRTEntry] = []
    for i in range(int(line_cnt / 4)):
        srt = SRTEntry(
            timecode=lines[1 + 4 * i].strip(),
            text=lines[2 + 4 * i].strip(),
        )
        srt_entries.append(srt)
        print(f'srt: {srt}')
    return SRT(entries=srt_entries)


async def run():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <srt_file>")
        return
    data: FileData = await FileUtils.read_file(sys.argv[1], exp_ext='.srt')
    srt: SRT = await parse_srt_file(data.content)
    for translator in translators:
        print(f'translating to {translator.target}')
        srt.translate(translator).write_to(path=f'{data.dir}/{data.base}_{translator.target}{data.ext}')

    print('done')


if __name__ == '__main__':
    asyncio.run(run())
