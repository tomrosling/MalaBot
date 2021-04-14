import random

_words = {
    'moved to':[
        'teleported to',
        'slinked away to',
        'sneaked to',
        'hopped to',
        'ran away to'
    ],
    'joined':[
        'apparated into',
        'joined',
        'has appeared in',
        'popped into'
    ],
    'left':[
        'ragequit',
        'abandoned',
        'left',
    ]
}


def get_synonym(word):
    return _words[word][random.randint(0, len(_words[word]) - 1)]
    