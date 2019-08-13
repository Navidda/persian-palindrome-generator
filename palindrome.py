# -*- coding: utf-8 -*- 

from collections import defaultdict
import datrie

words = set()

past_shenase = [
    'م',
    'ی',
    '',
    'یم',
    'ید',
    'ند',
]

present_shenase = [
    'م',
    'ی',
    'د',
    'یم',
    'ید',
    'ند',
]

zamir = [
    'م',
    'ش',
    'ت',
    'مان',
    'تان',
    'شان',
]

short_verb = [
    'م',
    'ی',
    'ه',
    'یم',
    'ید',
    'ند',
]

persian_chars = set()

with open("verbs.txt") as f:
    for line in f:
        past, present = line.split("#")
        if past:
            for s in past_shenase:
                words.add(past.strip() + s)
        if present:
            for s in present_shenase:
                words.add(present.strip() + s)

with open("words.txt") as f:
    for line in f:
        word = line.split()[0].strip()
        persian_chars.update(set(word))
        words.add(word)
        # for v in short_verb:
        #     words.add(word + v)
        # for z in zamir:
        #     words.add(word + z)


# Ignore the difference of some similiar Farsi characters
trans_table = str.maketrans("صثطحذظضغئآ", "سستهزززقعا", "‌")


def normalized(string):
    """
    :type string: str
    """
    return string.translate(trans_table)


translated_words = defaultdict(set)
for w in words:
    translated_words[normalized(w)].add(w)


# Triple word palindromes
trie = datrie.Trie(persian_chars)
rtrie = datrie.Trie(persian_chars)
for w in words:
    trie[normalized(w)] = True
    rtrie[normalized(w[::-1])] = True

palindromes = set()
cnt = 0
with open('output_triple.txt', 'w') as f:
    for w1 in sorted(words):
        cnt += 1
        for w3 in rtrie.prefixes(w1):
            if len(w1) == len(w3):
                continue
            w3 = w3[::-1]
            w2_suf = w1[-(len(w1) - len(w3)):]
            for w2 in rtrie.keys(w2_suf):
                w2 = w2[::-1]
                w2_pref = w2[:-len(w2_suf)]
                if w2_pref == w2_pref[::-1]:
                    for rw1 in translated_words[w1]:
                        for rw2 in translated_words[w2]:
                            for rw3 in translated_words[w3]:
                                p = ' '.join([rw1, rw2, rw3])
                                f.write(p + '\n')
        if not cnt % 79 or cnt == len(words):
            print('\r' + str(cnt) + "\t / " + str(len(words)), end='')

# Double word palindromes
palindromes = set()
for w in sorted(words):
    for ww in translated_words[normalized(w[::-1])]:
        palindromes.add(w + ' ' + ww)
    for ww in translated_words[normalized(w[::-1][1:])]:
        palindromes.add(w + ' ' + ww)
    for ww in translated_words[normalized(w[1:][::-1])]:
        palindromes.add(ww + ' ' + w)

with open('output_double.txt', 'w') as f:
    for p in sorted(palindromes):
        f.write(p + "\n")


# Single word palindromes
with open('output_single.txt', 'w') as f:
    for w in sorted(words):
        if normalized(w) == normalized(w[::-1]):
            f.write(w + '\n')
