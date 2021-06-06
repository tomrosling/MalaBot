import random

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

_user_weights = {
    151776854435430400: [ # Mala
        ('en-chris', 0.3),
        ('fr-FR', 0.3),
    ],
    143476957122658306: [ # James
        ('en-chris', 0.5),
        ('ko-KR', 0.25),
    ],
    93408269434884096: [ # Zoetrope
        ('en-chris', 1),
    ],
    148237285190533120: [ # Sarah
        ('en-chris', 0.6),
    ],
    135476235831607296: [ # Grumpy Cookie
        ('en-chris', 0.25),
        ('it-IT', 0.2),
        ('ko-KR', 0.2),
    ],
}

_default_weights = [
    ('en-chris', 0.5)
]


def get_synonym(word, user_id):
    options = _words[word]

    def pick_language(word, user_id):
        weights = _user_weights.get(user_id) or _default_weights
        assert(sum(map(lambda pair: pair[1], weights)) <= 1)
        r = random.random()
        accumulator = 0
        for pair in weights:
            lang = pair[0]

            # Skip language if there isn't an entry for this word.
            if not lang in options:
                continue

            # Accumulate probabilities and check RNG against this language.
            accumulator += pair[1]
            if r < accumulator:
                return lang
        
        # If we got this far, remove any entries from options that were in the weighting list,
        # then split the remaining probability between all other options.
        assert(r > 0)
        weighted_langs = map(lambda pair: pair[0], weights)
        filtered_options = list(filter(lambda lang: not lang in weighted_langs, options.keys()))
        index = int(r * len(filtered_options))
        return filtered_options[index]

    lang = pick_language(word, user_id)
    return lang, options[lang]
