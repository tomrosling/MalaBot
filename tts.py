from dotenv import load_dotenv
from google.cloud import texttospeech
import wave

load_dotenv()

client = texttospeech.TextToSpeechClient()

# NOTE: Discord actually wants 48KHz stereo (for some reason). But 96KHz mono works fine for now.
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16, sample_rate_hertz=96000)


def text_to_pcm(input, lang):
    lang = lang or 'en-GB'

    if lang == 'en-chris':
        chris = get_chris_audio(input, lang)
        if chris:
            return chris
        
        # Fallback to English TTS if there is no pre-recorded sample.
        lang = 'en-GB'

    overrides = { 
        'en-GB': 'en-GB-Wavenet-F',
        'de-DE': 'de-DE-Wavenet-F'
    }
    voice_name = overrides.get(lang) or lang + '-Wavenet-A'

    voice = texttospeech.VoiceSelectionParams(language_code=lang,
                                              name=voice_name)

    synthesis_input = texttospeech.SynthesisInput(text=input)

    response = client.synthesize_speech(input=synthesis_input,
                                        voice=voice,
                                        audio_config=audio_config)

    return response.audio_content


def get_chris_audio(input, lang):
    try:
        # Remove punctuation, replace spaces with underscores.
        sanitised_input = input.translate(str.maketrans(' ', '_', '!,.'))

        # Open pre-recorded audio.
        with wave.open(f'audio/{lang}/{sanitised_input}.wav', mode='rb') as f:
            return f.readframes(f.getnframes())
    
    except (OSError, wave.Error) as err:
        # Catch error, return None so we fall back to TTS.
        print(f'en-chris failed: {err}')
