import streamlit as st
from search_corpus import search_corpus

st.set_page_config(page_title="Graphematic Corpus Search", layout="wide")
st.title("📚 Graphematic Corpus Search")
st.markdown("""
Unesi riječ standardnim pravopisom (npr. **življenje**, **kršćanin**) kako bi pretražio/la sve moguće grafematske varijante u korpusu.
""")

query = st.text_input("🔍 Upit:", "")

if st.button("Pretraži") and query:
    try:
        with open("corpus.txt", "r", encoding="utf-8") as f:
            corpus = f.read()

        results = search_corpus(query, corpus)

        st.subheader("🎯 Generirani regex:")
        st.code(results['regex'], language="regex")

        st.subheader("📄 Rezultati (KWIC):")
        if results['matches']:
            for match in results['matches']:
                st.markdown(f"- {match}")
        else:
            st.info("Nema rezultata za zadani upit.")

    except Exception as e:
        st.error(f"Došlo je do pogreške: {e}")