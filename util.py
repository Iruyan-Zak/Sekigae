import re
from itertools import chain


def extract_numbers(s):
    range_re = re.compile(r"([0-9]+)-([0-9]+)")
    l = []
    while True:
        m = range_re.search(s)
        if m is None:
            break
        a, b = m.groups()
        l.append(range(int(a), int(b)+1))
        s = s[:m.start()] + " " + s[m.end():]
    single_re = re.compile(r"[0-9]+")
    l2 = []
    while True:
        m = single_re.search(s)
        if m is None:
            break
        l2.append(int(m.group()))
        s = s[:m.start()] + " " + s[m.end():]
    l.append(l2)
    return sorted(chain(*l))
