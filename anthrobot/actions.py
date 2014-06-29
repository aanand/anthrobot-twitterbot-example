from pattern.en import conjugate, lemma, tag

import re

from .utils import truncate


def generate(config, tweets):
    seeds = config.action_seeds()
    tweets = [t for t in tweets if not config.reject_tweet(tweets)]

    matches = get_matches(tweets, seeds)
    truncated = [truncate(m, seeds) for m in matches]
    transformed = [transform(m) for m in truncated]
    unique = list(set(transformed))

    return unique


def get_matches(tweets, seeds):
    searches = [
        re.search(seed + " [a-z]+ing.*", tweet, flags=re.IGNORECASE)
        for seed in seeds
        for tweet in tweets
    ]
    return [s.group() for s in searches if s]


def transform(text):
    transformations = []

    # text
    text = text.lower() + " "

    # change "going to do something" -> "do something", while preserving "going to a thing"
    tags = tag(text)
    if tags[0][0] == "going" and tags[1][0] == "to" and tags[2][1] == "VB":
        text = " ".join(text.split()[2:]) + " "

    # transform the verb
    orig_verb = text.split()[0]

    if "fuck" in orig_verb:
        transformations += [(orig_verb, "")]
        try:
            orig_verb = text.split()[1]
        except IndexError:
            return ''

    elif "something" in orig_verb or "anything" in orig_verb:
        return ''

    new_verb = conjugate(lemma(orig_verb), person=3)

    # weird "lies" bug?
    if new_verb == 'layers':
        new_verb = 'lies'

    transformations += [(orig_verb, new_verb)]

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

    # transform third person to gender-neutral
    transformations += [(" his ", " her ")]
    transformations += [(" him ", " her ")]
    transformations += [(" her ", " her ")]
    transformations += [(" he ", " she ")]
    transformations += [(" she ", " she ")]
    transformations += [(" he's ", " she's ")]
    transformations += [(" she's ", " she's ")]
    transformations += [(" hes ", " she's ")]
    transformations += [(" shes ", " she's ")]

    transformations += [(" n't ", " not ")]

    for orig, repl in transformations:
        text = text.replace(orig, repl)

    return text.strip()
