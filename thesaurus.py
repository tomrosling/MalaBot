import random

_words = {
    'moved to': [
        ('en-GB', 'teleported to'),
        ('en-GB', 'slinked away to'),
        ('en-GB', 'sneaked to'),
        ('en-GB', 'hopped to'),
        ('en-GB', 'ran away to')
    ],
    'Hello': [
        #('en-GB', 'Hello'),
        ('en-chris', 'Hello'),
        ('fr-FR', 'Bonjour'),
        ('es-ES', 'Hola'),
        ('ru-RU', 'Zdravstvuyte'),
        ('zh-CN', 'Nǐn hǎo'),
        ('it-IT', 'Salve'),
        ('ja-JP', 'Konnichiwa'),
        ('de-DE', 'Guten Tag'),
        ('pt-PT', 'Olá'),
        ('nl-NL', 'Goedendag'),
        ('ko-KR', 'Annyeong'),
        ('sv-SE', 'Hej'),
        ('fi-FI', 'Moi'),
    ],
    'Goodbye': [
        #('en-GB', 'Goodbye'),
        ('es-ES', 'Adios'),
        ('it-IT', 'Arrivederci'),
        ('fr-FR', 'Au Revoir'),
        ('pt-PT', 'Até logo'),
        ('de-DE', 'Auf Wiedersehen'),
        ('ja-JP', 'Sayōnara'),
        ('ru-RU', 'Do svidaniya'),
        ('ko-KR', 'Annyeong'),
        #(None, 'Slan'),#Irish
        ('nl-NL', 'Tot ziens'),
        ('zh-CN', 'Zàijiàn'),
        ('sv-SE', 'Adjö'),
        ('fi-FI', 'Hyvästi'),
    ]
}


def get_synonym(word):
    return _words[word][random.randint(0, len(_words[word]) - 1)]
