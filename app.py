import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

# 1. Page Setup
st.set_page_config(page_title="Translator App", page_icon="🌐")
st.title("🌐 ALL LANGUAGE TRANSLATOR")

# 2. Get Supported Languages
# We use st.cache_data so the app doesn't have to reload the list every time
@st.cache_data
def get_languages():
    return GoogleTranslator().get_supported_languages(as_dict=True)

langs_dict = get_languages()
dropdown_options = {k.capitalize(): v for k, v in langs_dict.items()}

# 3. UI Elements (Streamlit replacement for ipywidgets)
text_input = st.text_area("Type text here...", placeholder="Enter text to translate", height=150)

# Language selection dropdown
target_lang_name = st.selectbox("Select Target Language:", options=list(dropdown_options.keys()), index=list(dropdown_options.keys()).index('Spanish') if 'Spanish' in dropdown_options else 0)
target_lang_code = dropdown_options[target_lang_name]

# 4. Translation Logic
if st.button('Translate Now'):
    if text_input.strip() == "":
        st.warning("Please enter some text first!")
    else:
        try:
            with st.spinner('Translating...'):
                # Perform translation
                translation = GoogleTranslator(source='auto', target=target_lang_code).translate(text_input)
                
                # Display Output (Replaces widgets.Output)
                st.markdown("---")
                st.subheader("Translation:")
                st.success(translation)
                
                # Optional: Add Text-to-Speech since you mentioned gTTS
                tts = gTTS(text=translation, lang=target_lang_code)
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                st.audio(audio_fp, format='audio/mp3')
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
