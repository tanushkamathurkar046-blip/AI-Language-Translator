import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS
import time

from langdetect import DetectorFactory
DetectorFactory.seed = 0
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="wide"
)

if "history" not in st.session_state:
    st.session_state.history = []

# Theme
theme = st.sidebar.radio(
    "🎨 Select Theme",
    ["Dark", "Light"]
)

with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
if theme == "Light":
    st.markdown("""
    <style>

    .stApp{
        background:#F8FAFC;
        color:black;
    }

    h1{
        color:#2563EB;
    }

    p{
        color:#374151;
    }

    section[data-testid="stSidebar"]{
        background:#E5E7EB;
    }

    </style>
    """, unsafe_allow_html=True)
st.sidebar.title("🌍 CodeAlpha AI Project")
st.markdown("""
<div class="welcome-card">
<h2>👋 Welcome!</h2>

<p>
Translate text instantly into 100+ languages with AI.
</p>

</div>
""", unsafe_allow_html=True)
st.sidebar.info("""
Developer: Tanushka Mathurkar

Task: AI Language Translator


Technology:
- Streamlit
- Google Translator
- gTTS
- LangDetect
""")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Project Status")

st.sidebar.progress(100)

st.sidebar.success("Completed")

st.sidebar.metric(
    "🌍 Total Translations",
    len(st.session_state.history)
)

total_words = sum(
    len(item["Original"].split())
    for item in st.session_state.history
)

st.sidebar.metric(
    "📝 Total Words",
    total_words
)
st.markdown("""
<div class="hero">

<h1>🌍 AI Language Translator</h1>

<p>
Translate text into 100+ languages using Artificial Intelligence
</p>

</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.success("⚡ Fast Translation")

with col2:
    st.success("🌍 Multiple Languages")

with col3:
    st.success("🔊 Text to Speech")

languages = {
    "🇺🇸 English": "en",
    "🇮🇳 Hindi": "hi",
    "🇮🇳 Marathi": "mr",
    "🇫🇷 French": "fr",
    "🇩🇪 German": "de",
    "🇪🇸 Spanish": "es",
    "🇯🇵 Japanese": "ja",
    "🇨🇳 Chinese": "zh-CN"
}

text = st.text_area("Enter Text")

c1, c2 = st.columns(2)

with c1:
    st.metric("📄 Characters", len(text))

with c2:
    st.metric("📝 Words", len(text.split()))
col1, col2, col3 = st.columns([5,1,5])

with col1:
    source = st.selectbox(
        "Source Language",
        ["Auto Detect"] + list(languages.keys())
    )

with col2:
    swap = st.button("🔄")

with col3:
    target = st.selectbox(
        "Target Language",
        list(languages.keys())
    )

if swap and source != "Auto Detect":
    source, target = target, source

if st.button("🚀 Translate"):
    start = time.time()
    if text.strip() == "":
        st.warning("Please enter some text.")
    
    else:
        
        if source == "Auto Detect":
            detected = detect(text)
            translated = GoogleTranslator(
                source=detected,
                target=languages[target]
            ).translate(text)

            st.info(f"Detected Language Code: {detected}")

        else:
            translated = GoogleTranslator(
                source=languages[source],
                target=languages[target]
        ).translate(text)
        st.success("Translation Completed!")
        st.balloons()
# Calculate time FIRST
        end = time.time()
        translation_time = round(end - start, 2)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📄 Characters", len(text))

        with col2:
            if source == "Auto Detect":
                st.metric("🌍 Detected", detected.upper())
            else:
                st.metric("🌍 Source", source)

        with col3:
            st.metric("🎯 Target", target)

        with col4:
            st.metric("⏱ Time", f"{translation_time} sec")



        st.session_state.history.append({
            "Original": text,
            "Translated": translated,
            "Language": target
        })
        end = time.time()
        translation_time = round(end - start, 2)

        st.markdown(f"""
<div style="
background:rgba(255,255,255,.08);
padding:25px;
border-radius:15px;
border-left:6px solid #3B82F6;
font-size:22px;
color:white;
">

🌍 {translated}

</div>
""",unsafe_allow_html=True)
        
        tts = gTTS(text=translated, lang=languages[target])

        tts.save("translated.mp3")

        with open("translated.mp3", "rb") as audio_file:
            audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mp3")
        st.code(translated)
        st.download_button(
            label="📥 Download Translation",
            data=translated,
            file_name="translation.txt",
            mime="text/plain"
        )   
        
        st.markdown("---")

        col1, col2 = st.columns([5,1])

with col2:
    if st.button("🗑 Clear History"):
        st.session_state.history = []
        st.rerun()
st.subheader("🕒 Translation History")

if st.session_state.history:

    for item in reversed(st.session_state.history):

        st.markdown(f"""
        **Original:** {item['Original']}

        **Translated:** {item['Translated']}

        **Language:** {item['Language']}
        """)

        st.markdown("---")

else:
    st.info("No translations yet.")

    st.markdown("---")


st.markdown("---")

st.markdown("""
<div class="footer">

<h3>🌍 AI Language Translator</h3>

<p>
Made with ❤️ by <b>Tanushka Mathurkar</b>
</p>

<p>
Python • Streamlit • Google Translator • gTTS
</p>

<p>
© 2026
</p>

</div>
""", unsafe_allow_html=True)
