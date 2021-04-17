import random

_words = {
    'moved to': [
        (None, 'teleported to'),
        (None, 'slinked away to'),
        (None, 'sneaked to'),
        (None, 'hopped to'),
        (None, 'ran away to')
    ],
    'Hello': [
        (None, 'Hello'),
        (None, 'Bonjour'),
        (None, 'Hola'),
        (None, 'Zdravstvuyte'),
        (None, 'Nǐn hǎo'),
        (None, 'Salve'),
        (None, 'Konnichiwa'),
        (None, 'Guten Tag'),
        (None, 'Olá'),
        (None, 'Goedendag'),
        (None, 'Annyeong')
    ],
    'Goodbye': [
        (None, 'Goodbye'),
        (None, 'Adios'),
        (None, 'Arrivederci)'
        (None, 'Au Revoir'),
        (None, 'Adeus'),
        (None, 'Auf Wiedersehen'),
        (None, 'Sayōnara'),
        (None, 'Do svidaniya'),
        (None, 'Annyeong'),
        (None, 'Slan'),
        (None, 'Tot ziens')
    ]
}


def get_synonym(word):
    return _words[word][random.randint(0, len(_words[word]) - 1)]
