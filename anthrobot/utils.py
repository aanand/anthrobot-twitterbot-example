def truncate(text, seeds):
    text = text.lower()

    start = len(text)

    for s in seeds:
        if s in text and text.index(s) < start:
            start = text.index(s) + len(s)

    delims = set([".", " http", ",", " and", "!", "?", "#" "~", "(", ":", ")", "^", "-", "@", "#", "&", ";"])
    end = min([len(text)] + [text.index(d) for d in delims if d in text])
    return filter_unicode(text[start:end]).strip()


def filter_unicode(s): return "".join(i for i in s if ord(i)<128)
