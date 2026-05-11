# search for pages containing given words
def find_pages(index, words):

    if not words:
        return []

    words = [w.lower() for w in words]
    matches = None

    for w in words:
        if w not in index:
            return []  # any word missing = no match
        pages = set(index[w].keys())
        if matches is None:
            matches = pages
        else:
            matches = matches & pages  # AND

    return sorted(matches) if matches else []
