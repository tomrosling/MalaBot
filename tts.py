from dotenv import load_dotenv
from google.cloud import texttospeech

load_dotenv()

client = texttospeech.TextToSpeechClient()

# NOTE: Discord actually wants 48KHz stereo (for some reason). But 96KHz mono works fine for now.
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16, sample_rate_hertz=96000)


def text_to_pcm(input, lang):
    lang = lang or 'en-GB'

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
