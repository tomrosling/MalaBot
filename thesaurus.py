import random

_words = {
    'moved to': [
        'teleported to',
        'slinked away to',
        'sneaked to',
        'hopped to',
        'ran away to'
    ],
    'Hello': [
        'Hello',
        'Bonjour',
        'Hola',
        'Zdravstvuyte',
        'Nǐn hǎo',
        'Salve',
        'Konnichiwa',
        'Guten Tag',
        'Olá',
        'Goedendag',
        'Annyeong'
    ],
    'Goodbye': [
        'Goodbye',
        'Adios',
        'Arrivederci'
        'Au Revoir',
        'Adeus',
        'Auf Wiedersehen',
        'Sayōnara',
        'Do svidaniya',
        'Annyeong',
        'Slan',
        'Tot ziens'
    ]
}


def get_synonym(word):
    return _words[word][random.randint(0, len(_words[word]) - 1)]
