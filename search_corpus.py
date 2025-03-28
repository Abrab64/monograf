import re
import sys
import unicodedata

# Funkcija koja "normalizira" samo vokale (a, e, i, o, u) – uklanja dijakritike samo kod njih
def normalize_vowels(text):
    vowels = "aeiouAEIOU"
    result = ""
    for char in text:
        if char in vowels:
            # Na NFD formu se razlaže znak; zadržavamo samo osnovno slovo
            decomposed = unicodedata.normalize('NFD', char)
            base = "".join(c for c in decomposed if not unicodedata.combining(c))
            result += base
        else:
            result += char
    return result

# Funkcija koja uklanja sve dijakritike – koristimo je samo za kompletan upit ako je potrebno
def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if not unicodedata.combining(c))

# Funkcija koja provjerava je li token sastavljen isključivo od suglasnika
def is_pure_consonant(token):
    # Definiramo samoglasnike (bez dijakritika, budući da su normalizirani kod vokala)
    vowels = set("aeiou")
    token_lower = token.lower()
    return all(ch.isalpha() and ch not in vowels for ch in token_lower)

# Mapping pravila – definirano prema pravilima iz članka
graphematic_map = {
    "a": ["a"],
    "b": ["b"],
    "c": ["cz"],                   # /c/ se bilježi isključivo kao <cz>
    "č": ["ç"],                    # /č/ se bilježi kao <ç>
    "ć": ["chi", "ch", "tj"],      # za /ć/ primarni je <chi>
    "d": ["d"],
    "đ": ["gi", "g", "gj", "dj", "dg"],
    "e": ["e"],
    "f": ["f"],
    "g": ["g", "gh"],
    "h": ["h"],
    "i": ["i"],
    "j": ["j"],
    "k": ["k", "qu"],             # uključujemo i mogućnost qu = kv
    "l": ["l"],
    "lj": ["gli", "gl", "l’j", "l’", "l+j", "li"],
    "m": ["m"],
    "n": ["n"],
    "nj": ["gni", "gn", "nj", "n’j", "n’", "n+j"],
    "o": ["o"],
    "p": ["p", "ph"],
    "r": ["r", "ar"],             # /r/ – slogotvorno se bilježi kao ar (ako nije u kontaktu sa samoglasnicima)
    "s": ["ſ", "s"],
    "š": ["ſc", "sc"],
    "t": ["t"],
    "u": ["u"],
    "v": ["v", "u"],              # Alternacije u/v: obje mogućnosti
    "z": ["z"],
    "ž": ["ž", "ž", "ſz", "ſſ", "zs", "zh", "x"]
}

def generate_regex(input_word):
    # Normaliziramo upit – ovdje uklanjamo dijakritike samo kod vokala
    normalized = normalize_vowels(input_word.lower())
    regex = ""
    i = 0
    # Pokušavamo mapirati što veće segmente (4, 3, 2 znakova), pa pojedinačno
    while i < len(normalized):
        matched = False
        for length in [4, 3, 2]:
            if i + length <= len(normalized):
                chunk = normalized[i:i+length]
                if chunk in graphematic_map:
                    variants = graphematic_map[chunk]
                    group = "(?:" + "|".join(re.escape(v) for v in variants) + ")"
                    # Ako je cijeli chunk sastavljen od suglasnika, dopustimo geminaciju (jedan ili dva puta)
                    if is_pure_consonant(chunk):
                        group += "{1,2}"
                    regex += group
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
            if is_pure_consonant(char):
                group += "{1,2}"
            regex += group
            i += 1
        # Opcionalno: ako se između dvije vokalne sekvence može pojaviti intervokalno 'j'
        if i > 0 and i < len(normalized):
            prev = normalized[i-1]
            next_ = normalized[i]
            if prev in "aeiou" and next_ in "aeiou":
                regex += "(?:j)?"
    # Omotamo regex da se niz može pojaviti bilo gdje u riječi
    return "(?i).*" + regex + ".*"

# Pattern za tokenizaciju riječi – riječ definiranom bjelinama i pravopisnim znakovima
word_pattern = re.compile(r'\b[\w’\+\u0100-\u017F]+\b', flags=re.UNICODE)

def get_word_spans(text):
    return [(m.group(), m.start(), m.end()) for m in word_pattern.finditer(text)]

def get_matching_tokens(corpus_text, pattern):
    tokens = get_word_spans(corpus_text)
    matching = []
    for token, start, end in tokens:
        # Normaliziramo token (vokale bez naglasaka) i provjeravamo match
        norm_token = normalize_vowels(token.lower())
        if re.search(pattern, norm_token):
            matching.append((token, start, end))
    return matching

def get_kwic_line(corpus_text, token_span, word_spans, context_words=3):
    token, start, end = token_span
    idx = None
    for j, (t, s, e) in enumerate(word_spans):
        if s == start and e == end:
            idx = j
            break
    if idx is None:
        return token
    left_context = " ".join(word_spans[k][0] for k in range(max(0, idx-context_words), idx))
    right_context = " ".join(word_spans[k][0] for k in range(idx+1, min(len(word_spans), idx+1+context_words)))
    return f"{left_context} [{token}] {right_context}".strip()

def main():
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = input("Unesi upit (npr. 'življen'): ")
    
    # Generiramo regex iz upita
    pattern = generate_regex(query)
    
    corpus_path = "corpus.txt"
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            corpus_text = f.read()
    except FileNotFoundError:
        print(f"Datoteka {corpus_path} nije pronađena.")
        sys.exit(1)
    
    # Tokeniziramo originalni tekst (originalni dijakritici ostaju)
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
                kwic = get_kwic_line(corpus_text, token_span, word_spans, context_words=3)
                out.write(kwic + "\n")
    
    print("Rezultati su zapisani u 'results.txt'.")
def search_corpus(query, corpus_text):
    pattern = generate_regex(query)
    word_spans = get_word_spans(corpus_text)
    matching_tokens = get_matching_tokens(corpus_text, pattern)
    results = [get_kwic_line(corpus_text, token_span, word_spans, context_words=3)
               for token_span in matching_tokens]
    return {
        "regex": pattern,
        "matches": results
    }

if __name__ == "__main__":
    main()
