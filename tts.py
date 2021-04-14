from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

voice = texttospeech.VoiceSelectionParams(language_code="en-GB",
                                          name="en-GB-Wavenet-F")

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3)


def text_to_mp3(input):
    synthesis_input = texttospeech.SynthesisInput(text=input)

    response = client.synthesize_speech(input=synthesis_input,
                                        voice=voice,
                                        audio_config=audio_config)

    return response.audio_content
