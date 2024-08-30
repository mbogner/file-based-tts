import asyncio
import edge_tts

async def list_available_voices():
    voices = await edge_tts.list_voices()
    # Sort the voices alphabetically by their short name
    sorted_voices = sorted(voices, key=lambda voice: voice["Locale"])

    # Print the sorted list of voice names with both ShortName and FriendlyName
    for voice in sorted_voices:
        print(f'{voice["Locale"]}, {voice["ShortName"]} (gender: {voice["Gender"]}): {voice["FriendlyName"]}')

# Run the asynchronous function
asyncio.run(list_available_voices())
