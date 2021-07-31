import random
import json

_words = {
    'Hello': {
        #'en-GB': 'Hello',
        'en-chris': 'Hello',
        'fr-FR': 'Bonjour',
        'es-ES': 'Hola',
        'ru-RU': 'Zdravstvuyte',
        'zh-CN': 'Nǐn hǎo',
        'it-IT': 'Salve',
        'ja-JP': 'Konnichiwa',
        'de-DE': 'Guten Tag',
        'pt-PT': 'Olá',
        'nl-NL': 'Goedendag',
        'ko-KR': 'Annyeong',
        'sv-SE': 'Hej',
        'fi-FI': 'Moi',
    },
    'Goodbye': {
        #'en-GB': 'Goodbye',
        'es-ES': 'Adios',
        'it-IT': 'Arrivederci',
        'fr-FR': 'Au Revoir',
        'pt-PT': 'Até logo',
        'de-DE': 'Auf Wiedersehen',
        'ja-JP': 'Sayōnara',
        'ru-RU': 'Do svidaniya',
        'ko-KR': 'Annyeong',
        'nl-NL': 'Tot ziens',
        'zh-CN': 'Zàijiàn',
        'sv-SE': 'Adjö',
        'fi-FI': 'Hyvästi',
    }
}


_default_weights = [
    ('en-chris', 0.5)
]


# Load user weights from a given file as a JSON object.
# This will all be stored as strings, and the format is:
#
# {
#   "display_name": [
#     ["lang", "weight"],
#     ...
#   ],
#   ...
# }
#
def load_weights(filename):
    try:
        with open(filename, 'r') as f:
            user_weights = json.load(f)
            # TODO: check format is legit
            return user_weights
    except Exception as e:
        print(f'Failed to load user RNG weights from \'{filename}\': {e}')

_user_weights = load_weights('config/user_weights.json')

def get_synonym(word, user_display_name):
    options = _words[word]

    def pick_language(word, user_display_name):
        weights = _user_weights.get(user_display_name) or _default_weights
        assert(sum(map(lambda pair: float(pair[1]), weights)) <= 1)
        r = random.random()
        accumulator = 0
        for pair in weights:
            lang = pair[0]

            # Skip language if there isn't an entry for this word.
            if not lang in options:
                continue

            # Accumulate probabilities and check RNG against this language.
            accumulator += float(pair[1])
            if r < accumulator:
                return lang
        
        # If we got this far, remove any entries from options that were in the weighting list,
        # then split the remaining probability between all other options.
        assert(r > 0)
        weighted_langs = map(lambda pair: pair[0], weights)
        filtered_options = list(filter(lambda lang: not lang in weighted_langs, options.keys()))
        index = int(r * len(filtered_options))
        return filtered_options[index]

    lang = pick_language(word, user_display_name)
    return lang, options[lang]
