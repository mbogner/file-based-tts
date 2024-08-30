import asyncio
import sys
from dataclasses import dataclass

from deep_translator import GoogleTranslator

from utils.file_utils import FileUtils, FileData


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


async def translate_srt(path: str, source_language: str = 'en', target_languages: list[str] = None):
    print(f'processing {path}')
    if target_languages is None:
        target_languages = ['de', 'hi', 'zh-CN', 'ru', ]
    data: FileData = await FileUtils.read_file(path, exp_ext='.srt')
    srt: SRT = await parse_srt_file(data.content)
    for translator in [
        GoogleTranslator(source=source_language, target=lang) for lang in target_languages
    ]:
        print(f'translating to {translator.target}')
        srt.translate(translator).write_to(path=f'{data.dir}/{data.base}_{translator.target}{data.ext}')
    print('done')


if __name__ == '__main__':
    args = len(sys.argv)
    if args < 2:
        print(f"Usage: python {sys.argv[0]} <srt_file> (<source_language> <target_languages_csv>)")
    else:
        if args >= 4:
            asyncio.run(translate_srt(
                path=sys.argv[1],
                source_language=sys.argv[2],
                target_languages=sys.argv[3].split(','),
            ))
        else:
            asyncio.run(translate_srt(path=sys.argv[1]))
