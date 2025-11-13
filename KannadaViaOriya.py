import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from aksharamukha.transliterate import process as aksharamukha_process
from gtts import gTTS
from io import BytesIO
import pandas as pd

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(
    page_title="Odia → Kannada Learning",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------ HIDE STREAMLIT UI ------------------ #
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ------------------ AUDIO GENERATOR ------------------ #
def make_audio(text, lang="kn"):
    fp = BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

# ------------------ PAGE TITLE ------------------ #
st.title("📝 Learn Kannada using Odia Script")
st.subheader("ଓଡ଼ିଆ ଲିପି ଦ୍ୱାରା କନ୍ନଡ୍ ଶିଖନ୍ତୁ")

text = st.text_area("Enter Odia text here:", height=120)

if st.button("Translate"):
    if text.strip():
        try:
            # ---------------- FULL SENTENCE PROCESSING ---------------- #

            # Odia → Kannada sentence translation
            kannada = GoogleTranslator(source="or", target="kn").translate(text)

            # Kannada → Odia script
            kannada_in_odia = aksharamukha_process("Kannada", "Oriya", kannada)

            # Kannada → English phonetics
            kannada_english = transliterate(kannada, sanscript.KANNADA, sanscript.ITRANS)

            # Kannada audio (sentence)
            audio_sentence = make_audio(kannada)

            # ---------------- OUTPUT ---------------- #
            st.markdown("## 🔹 Translation Results")

            st.markdown(f"**Odia Input:**  \n:blue[{text}]")
            st.markdown(f"**Kannada Translation:**  \n:green[{kannada}]")
            st.markdown(f"**Kannada in Odia Script:**  \n:orange[{kannada_in_odia}]")
            st.markdown(f"**English Phonetics:**  \n`{kannada_english}`")

            st.markdown("### 🔊 Kannada Audio (Sentence)")
            st.audio(audio_sentence, format="audio/mp3")
            st.download_button("Download Sentence Audio", audio_sentence, "sentence.mp3")

            # ---------------- WORD-BY-WORD FLASHCARDS ---------------- #

            st.markdown("---")
            st.markdown("## 🃏 Flashcards (Word-by-Word)")

            odia_words = text.split()
            kan_words = kannada.split()

            # Handle mismatch carefully
            limit = min(len(odia_words), len(kan_words))

            for i in range(limit):
                ow = odia_words[i]
                kw = kan_words[i]

                # Kannada → Odia script (word)
                kw_or = aksharamukha_process("Kannada", "Oriya", kw)

                # Phonetic (word)
                kw_ph = transliterate(kw, sanscript.KANNADA, sanscript.ITRANS)

                # Audio (word)
                kw_audio = make_audio(kw)

                with st.expander(f"Word {i+1}: {ow}", expanded=False):
                    st.write("**Odia word:**", ow)
                    st.write("**Kannada word:**", kw)
                    st.write("**Kannada in Odia script:**", kw_or)
                    st.write("**Phonetics:**", kw_ph)

                    st.audio(kw_audio, format="audio/mp3")
                    st.download_button(
                        f"Download Audio (Word {i+1})",
                        kw_audio,
                        f"word_{i+1}.mp3"
                    )

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Please enter Odia text.")
