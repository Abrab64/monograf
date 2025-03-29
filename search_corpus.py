import re
import sys
import unicodedata
import streamlit as st

# Funkcija koja "normalizira" samo vokale (a, e, i, o, u) – uklanja dijakritike samo kod njih
def normalize_vowels(text):
    vowels = "aeiouAEIOU"
    result = ""
    for char in text:
        if char in vowels:
            decomposed = unicodedata.normalize('NFD', char)
            base = "".join(c for c in decomposed if not unicodedata.combining(c))
            result += base
        else:
            result += char
    return result

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if not unicodedata.combining(c))

def is_pure_consonant(token):
    vowels = set("aeiou")
    token_lower = token.lower()
    return all(ch.isalpha() and ch not in vowels for ch in token_lower)

graphematic_map = {
    "a": ["a"],
    "b": ["b"],
    "c": ["cz"],
    "č": ["ç"],
    "ć": ["chi", "ch", "tj"],
    "d": ["d"],
    "đ": ["gi", "g", "gj", "dj", "dg"],
    "e": ["e"],
    "f": ["f"],
    "g": ["g", "gh"],
    "h": ["h"],
    "i": ["i"],
    "j": ["j"],
    "k": ["k"],
    "l": ["l"],
    "lj": ["gli", "gl", "l’j", "l’", "l+j", "li"],
    "m": ["m"],
    "n": ["n"],
    "nj": ["gni", "gn", "nj", "n’j", "n’", "n+j"],
    "o": ["o"],
    "p": ["p", "ph"],
    "r": ["r", "ar"],
    "s": ["ſ", "s"],
    "š": ["ſc", "sc"],
    "t": ["t"],
    "u": ["u"],
    "v": ["v", "u"],
    "z": ["z"],
    "ž": ["ž", "ź", "ſz", "ſſ", "zs", "zh", "x"]
}

def generate_regex(input_word, match_whole_word=False):
    normalized = normalize_vowels(input_word.lower())
    regex_parts = []
    i = 0
    while i < len(normalized):
        if i >= 1 and i+1 < len(normalized):
            prev = normalized[i-1]
            curr = normalized[i]
            nxt = normalized[i+1]
            if curr == "j" and prev in "aeiou" and nxt in "aeiou":
                regex_parts.append(("j", "(?:j)?"))
                i += 1
                continue
            if prev + curr == "ij" or curr + nxt == "ji":
                regex_parts.append(("j", "(?:ij|ji|i|j)"))
                i += 1
                continue

        if normalized[i:i+2] in ("kv", "ku"):
            group = "(?:k|q)+" + re.escape(normalized[i+1]) + "+"
            regex_parts.append(("kv-ku", group))
            i += 2
            continue

        matched = False
        for length in [4, 3, 2]:
            if i + length <= len(normalized):
                chunk = normalized[i:i+length]
                if chunk in graphematic_map:
                    variants = graphematic_map[chunk]
                    group = "(?:" + "|".join(re.escape(v) for v in variants) + ")"
                    if chunk.isalpha():
                        group += "+"
                    regex_parts.append((chunk, group))
                    i += length
                    matched = True
                    break
        if not matched:
            char = normalized[i]
            if char in graphematic_map:
                variants = graphematic_map[char]
            else:
                variants = [re.escape(char)]
            group = "(?:" + "|".join(re.escape(v) for v in variants) + ")"
            if char.isalpha():
                group += "+"
            regex_parts.append((char, group))
            i += 1

    regex = "".join(group for _, group in regex_parts)
    if match_whole_word:
        return f"(?i)^" + regex + "$"
    else:
        return f"(?i).*({regex}).*"

def is_invalid_final_cluster(word, query=None):
    lower = word.lower()
    if lower.endswith("chi") and not (query and query.lower().endswith("ć")):
        return True
    if lower.endswith("gni") and not (query and query.lower().endswith("nj")):
        return True
    if lower.endswith("gli") and not (query and query.lower().endswith("lj")):
        return True
    return False

def get_word_spans(text):
    words = []
    for match in re.finditer(r'\S+', text):
        word = match.group()
        words.append((word, match.start(), match.end()))
    return words

def get_matching_tokens(corpus_text, pattern, query=None):
    tokens = get_word_spans(corpus_text)
    matching = []
    for token, start, end in tokens:
        norm_token = normalize_vowels(token.lower())
        if re.fullmatch(pattern, norm_token) or re.search(pattern, norm_token):
            if not is_invalid_final_cluster(token, query=query):
                matching.append((token, start, end))
    return matching

# NOVO: Funkcija za pokretanje pretrage u aplikaciji

def search_corpus(query, corpus_text, match_whole_word=False):
    pattern = generate_regex(query, match_whole_word=match_whole_word)
    word_spans = get_word_spans(corpus_text)
    matching_tokens = get_matching_tokens(corpus_text, pattern, query=query)
    results = [get_kwic_line(corpus_text, token_span, word_spans, context_words=3)
               for token_span in matching_tokens]
    return {
        "regex": pattern,
        "matches": results
    }

def get_kwic_line(corpus_text, token_span, word_spans, context_words=3):
    token, start, end = token_span
    idx = None
    for j, (t, s, e) in enumerate(word_spans):
        if s == start and e == end:
            idx = j
            break
    if idx is None:
        return token
    center = word_spans[idx][0]
    left_context = " ".join(word_spans[k][0] for k in range(max(0, idx-context_words), idx))
    right_context = " ".join(word_spans[k][0] for k in range(idx+1, min(len(word_spans), idx+1+context_words)))
    return f"{left_context} **{center}** {right_context}".strip()
