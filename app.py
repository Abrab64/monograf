import streamlit as st
from search_corpus import search_corpus

st.set_page_config(page_title="Grafematička korpusna pretraga", layout="wide")
st.title("📚 Graphematičko korpusno pretraživanje")

st.markdown("""
Unesi riječ ili dio riječi standardnim pravopisom (npr. **življenje**, **kršćanin**) kako bi pretražio/la sve moguće grafematičke varijante u korpusu.
""")

query = st.text_input("🔍 Upit:", "")
match_whole = st.checkbox("Pretraži samo cijele riječi")

if st.button("Pretraži") and query:
    try:
        with open("corpus.txt", "r", encoding="utf-8") as f:
            corpus = f.read()

        # Dodajemo drugu liniju analize u rezultat
        results = search_corpus(query, corpus, match_whole_word=match_whole, apply_post_filters=True)

        st.subheader("🎯 Generirani regex:")
        st.code(results['regex'], language="regex")

        st.subheader(f"📄 Rezultati (KWIC): Ukupno: {len(results['matches'])}")
        if results['matches']:
            for match in results['matches']:
                st.markdown(match)
        else:
            st.info("Nema rezultata za zadani upit.")

    except Exception as e:
        st.error(f"Došlo je do pogreške: {e}")
