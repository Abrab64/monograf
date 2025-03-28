import re
import sys
import unicodedata

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
    "k": ["k", "qu"],
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
    "ž": ["ž", "ž", "ſz", "ſſ", "zs", "zh", "x"]
}

def generate_regex(input_word):
    normalized = normalize_vowels(input_word.lower())
    regex_parts = []
    i = 0
    while i < len(normalized):
        if i >= 1 and i+1 < len(normalized):
            prev = normalized[i-1]
            curr = normalized[i]
            nxt = normalized[i+1]
            if prev in "aeiou" and curr == "j" and nxt in "aeiou":
                regex_parts.append(("j", "(?:j)?"))
                i += 1
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
    return f"(?i).*({regex}).*"

word_pattern = re.compile(r'\b[\w’\+\u0100-\u017F]+\b', flags=re.UNICODE)

def get_word_spans(text):
    return [(m.group(), m.start(), m.end()) for m in word_pattern.finditer(text)]

def get_matching_tokens(corpus_text, pattern):
    tokens = get_word_spans(corpus_text)
    matching = []
    for token, start, end in tokens:
        norm_token = normalize_vowels(token.lower())
        if re.search(pattern, norm_token):
            matching.append((token, start, end))
    return matching

def highlight_match(token, query):
    return f"**{token}**"

def get_kwic_line(corpus_text, token_span, word_spans, context_words=3, query=""):
    token, start, end = token_span
    idx = next((j for j, (t, s, e) in enumerate(word_spans) if s == start and e == end), None)
    if idx is None:
        return token
    left_context = [word_spans[k][0] for k in range(max(0, idx - context_words), idx)]
    right_context = [word_spans[k][0] for k in range(idx + 1, min(len(word_spans), idx + 1 + context_words))]
    highlighted = highlight_match(token, query)
    return f"{' '.join(left_context)} {highlighted} {' '.join(right_context)}"

def search_corpus(query, corpus_text):
    pattern = generate_regex(query)
    word_spans = get_word_spans(corpus_text)
    matching_tokens = get_matching_tokens(corpus_text, pattern)
    results = [get_kwic_line(corpus_text, token_span, word_spans, context_words=3, query=query)
               for token_span in matching_tokens]
    return {
        "regex": pattern,
        "matches": results
    }

def main():
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = input("Unesi upit (npr. 'življen'): ")

    pattern = generate_regex(query)
    corpus_path = "corpus.txt"
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            corpus_text = f.read()
    except FileNotFoundError:
        print(f"Datoteka {corpus_path} nije pronađena.")
        sys.exit(1)

    word_spans = get_word_spans(corpus_text)
    matching_tokens = get_matching_tokens(corpus_text, pattern)

    with open("results.txt", "w", encoding="utf-8") as out:
        out.write("Generirani regex:\n")
        out.write(pattern + "\n\n")
        if not matching_tokens:
            out.write("Nema pronađenih instanci.\n")
        else:
            out.write("Rezultati (tri riječi lijevo i tri riječi desno):\n\n")
            for token_span in matching_tokens:
                kwic = get_kwic_line(corpus_text, token_span, word_spans, context_words=3, query=query)
                out.write(kwic + "\n")

    print("Rezultati su zapisani u 'results.txt'.")

if __name__ == "__main__":
    main()
