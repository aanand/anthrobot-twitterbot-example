from pattern.en import parsetree

import re

from .utils import truncate


def generate(config, tweets):
    seeds = config.characteristic_seeds()
    tweets = [t for t in tweets if not config.reject_tweet(tweets)]

    matches = get_matches(tweets, seeds)
    truncated = [truncate(m, seeds) for m in matches]
    transformed = [transform(m) for m in truncated]
    nonempty = [c for c in transformed if len(c) > 0]
    unique = list(set(nonempty))
    filtered = [c for c in unique if not filter_verbs(c)]

    return filtered


def get_matches(tweets, seeds):
    searches = [
        re.search(seed + ".*", tweet, flags=re.IGNORECASE)
        for seed in seeds
        for tweet in tweets
    ]
    return [s.group() for s in searches if s]


def transform(text):
    transformations = []

    # text
    text = text.lower() + " "

    # transform first person to third
    transformations += [(" me ", " u ")]
    transformations += [(" my ", " ur ")]

    transformations += [(" i'm ", " ur ")]
    transformations += [(" im ", " ur ")]
    transformations += [(" i am ", " ur ")]
    transformations += [(" i ", " u ")]
    transformations += [(" i ", " u ")]
    transformations += [(" i've ", " u've ")]
    transformations += [(" ive ", " u've ")]
    transformations += [(" i'd ", " u'd ")]
    transformations += [(" id ", " u'd ")]

    transformations += [(" we ", " u ")]
    transformations += [(" ours ", " urs ")]
    transformations += [(" our ", " ur ")]
    transformations += [(" us ", " ur ")]

    # transform third person to first person
    transformations += [(" his ", " my ")]
    transformations += [(" him ", " me ")]
    transformations += [(" her ", " me ")]
    transformations += [(" he ", " i ")]
    transformations += [(" she ", " i ")]
    transformations += [(" he's ", " im ")]
    transformations += [(" she's ", " im ")]
    transformations += [(" hes ", " im ")]
    transformations += [(" shes ", " im ")]
    transformations += [(" shes ", " im ")]

    transformations += [(" n't ", " not ")]

    for orig, repl in transformations:
        text = text.replace(orig, repl)

    return text.strip()


def filter_verbs(text):
    t = parsetree(text)[0]
    if t[0].pos.startswith('RB') and len(t) > 1:
        return t[1].pos.startswith('VB')
    else:
        return t[0].pos.startswith('VB')


