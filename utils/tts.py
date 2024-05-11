import asyncio

import edge_tts


class TTS:
    @staticmethod
    async def list_voices():
        voices = await edge_tts.list_voices()
        for voice in voices:
            print(f"{voice}")


if __name__ == '__main__':
    asyncio.run(TTS.list_voices())
