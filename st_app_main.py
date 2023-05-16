# streamlit_audio_recorder by stefanrmmr (rs. analytics) - version January 2023

import os
import streamlit as st
from st_custom_components import st_audiorec
import yaml
import pickle
import requests
import json
import openai
from os.path import join
import whisper
from datetime import datetime
import yaml
import pickle
import spacy
import itertools
from multiprocessing import Pool
import logging
logging.basicConfig(level=logging.INFO)

# # DESIGN implement changes to the standard streamlit UI/UX
# # --> optional, not relevant for the functionality of the component!
# st.set_page_config(page_title="streamlit_audio_recorder")
st.set_page_config(layout="wide")

# # Design move app further up and remove top padding
# st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
#             unsafe_allow_html=True)
# # Design change st.Audio to fixed height of 45 pixels
# st.markdown('''<style>.stAudio {height: 45px;}</style>''',
#             unsafe_allow_html=True)
# # Design change hyperlink href link color
# st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
#             unsafe_allow_html=True)  # darkmode
# st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
#             unsafe_allow_html=True)  # lightmode

st.title("Multilingual ChatGPT Demo")
st.markdown("This is a simple ChatGPT demo that supports multilingual speech. We support both speech and text input.")


def completions(text, src, tar, org_text=None):
    url = 'https://cone.x-venture.tech/gw/service/cone/v1/engines/175b/completions'
    headers = {'Content-Type': 'application/json'}

    if org_text is None:
        res = requests.post(url, json={"prompt": text, "src": src, "tar": tar, "origin_prompt": text}, headers=headers)
    else:
        res = requests.post(url, json={"prompt": text, "src": src, "tar": tar, "origin_prompt": org_text},
                            headers=headers)

    # print(res, tar)
    # print(json.loads(res.content), tar)
    return json.loads(res.content)


def translate_by_api(text, reverse, model="cone"):
    translation = "You have turned off the translation function."
    if is_trans:
        # print("start translation")
        if model == "cone":
            if reverse is False:
                result_s1 = completions(text, source_lang, target_lang)
                translation = result_s1["choices"][0]["text"]
            else:
                result_s1 = completions(text, target_lang, source_lang)
                translation = result_s1["choices"][0]["text"]
        elif model == "chatgpt":
            if reverse is False:
                prompt = "translate the following text from {} to {}: {}".format(source_lang_name, target_lang_name, text)
                translation = chatgpt_by_api(prompt)['chat_text']
            else:
                prompt = "translate the following text from {} to {}: {}".format(target_lang_name, source_lang_name, text)
                translation = chatgpt_by_api(prompt)['chat_text']
        else:
            print("unknown model: {}".format(model))
            translation = "unknown model: {}".format(model)
    # print("translation: {}".format(translation))
    return {'translation': translation}


def chatgpt_response(prompt):
    # print(API_KEY)
    openai.api_key = API_KEY
    logging.info("prompt: {}".format(prompt))
    chatgpt_input = [
            {"role": "user", "content": "{}".format(prompt)}
        ]
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=chatgpt_input,
    )

    chat_text = response.choices[0].message.content
    return chat_text


def chatgpt_by_api(text):
    chat_text = "You have turned off the ChatGPT function."
    if is_chatgpt:
        # print("start request chatgpt: {}".format(text))
        prompt = text
        chat_text = chatgpt_response(prompt)
    print("chatgpt response: {}".format(chat_text))
    return {'text': text, 'chat_text': chat_text}


def stateful_button(*args, key=None, **kwargs):
    if key is None:
        raise ValueError("Must pass key")

    if key not in st.session_state:
        st.session_state[key] = False

    if st.button(*args, **kwargs):
        st.session_state[key] = not st.session_state[key]

    return st.session_state[key]


def audiorec_demo_app():
    st.markdown('**Voice Input:**')
    st.write('\n')

    wav_audio_data = st_audiorec()

    st.write('\n')
    st.write('\n')
    return wav_audio_data


def recognize_audio(audio_data):
    current_datetime = datetime.now()
    str_current_datetime = str(current_datetime).replace(" ", "-")
    print("str_current_datetime: {}".format(str_current_datetime))
    file_name = str_current_datetime + ".wav"
    wav_path = join(output_root, file_name)

    try:
        with open(wav_path, 'wb') as f:
            f.write(audio_data)
        print("Successfully wrote to {}".format(wav_path))
    except IOError as e:
        print("Failed to write to {}: {}".format(wav_path, e))

    model = whisper.load_model("base")
    result = model.transcribe(wav_path)
    text = result["text"]
    print(result)
    print("voice: {}".format(text))

    os.system("rm {}".format(wav_path))

    # final_result = pipline(text)
    # return final_result
    # return text
    return text


if __name__ == '__main__':
    if "recognized_text" not in st.session_state:
        st.session_state.recognized_text = ""
    if "text_input" not in st.session_state:
        st.session_state.text_input = ""
    if "translation" not in st.session_state:
        st.session_state.translation = ""
    if "response_of_translation" not in st.session_state:
        st.session_state.response_of_translation = ""
    if "translation_of_response" not in st.session_state:
        st.session_state.translation_of_response = ""
    if "text_input2" not in st.session_state:
        st.session_state.text_input2 = ""
    if "response_of_translation2" not in st.session_state:
        st.session_state.response_of_translation2 = ""

    with open("./config.yml", "r") as f:
        config = yaml.safe_load(f)
    with open('./name2langid.pickle', 'rb') as f:
        name2langid = pickle.load(f)

    name2langid["javanese"] = "jv"
    name2langid["hebrew"] = "he"

    API_KEY = config["API_KEY"]
    source_lang_name = config["source_lang"].lower()
    target_lang_name = config["target_lang"].lower()

    source_lang = name2langid[source_lang_name]
    target_lang = name2langid[target_lang_name]

    print("source_lang_name: {} target_lang_name: {} source_lang: {} target_lang: {}".format(source_lang_name,
                                                                                             target_lang_name,
                                                                                             source_lang, target_lang))
    output_root = config["output_root"]
    is_trans = True
    is_chatgpt = True
    split_sentence = config["split_sentence"]
    response_trans = config["response_trans"]

    # call main function
    audio = audiorec_demo_app()

    try:
        if st.button('Recognize Audio'):
            recognized_text = recognize_audio(audio)
            st.markdown("**Recognized Text:**")
            st.write(recognized_text)
            st.session_state.recognized_text = recognized_text

            st.session_state.text_input = st.session_state.recognized_text
            st.session_state.text_input2 = st.session_state.recognized_text

        else:
            st.write(st.session_state.recognized_text)

    except Exception as e:
        logging.info(e)
        st.write("error, try it again")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Service with Translation')
        try:
            if st.session_state.text_input:
                text_input = st.text_area('**Text Input:**', value=st.session_state.text_input, height=300)
                st.session_state.text_input = text_input
            else:
                text_input = st.text_area('**Text Input:**', value=st.session_state.recognized_text, height=300)
                st.session_state.text_input = text_input
        except Exception as e:
            logging.info(e)
            text_input = st.text_area('**Text Input:**', value="error, try it again", height=300)
            st.session_state.text_input = text_input

        # logging.info("current text_input: {}".format(text_input))
        try:
            if st.button('Translate'):
                translation = translate_by_api(st.session_state.text_input, False, model=response_trans)['translation']
                translation = st.text_area('**Translation Text:**', value=translation, height=300)
                st.session_state.translation = translation
            else:
                translation = st.text_area('**Translation Text:**', value=st.session_state.translation, height=300)
                st.session_state.translation = translation
        except Exception as e:
            logging.info(e)
            translation = st.text_area('**Translation Text:**', value="error, try it again", height=300)
            st.session_state.translation = translation

        try:
            if st.button('ChatGPT Dialogue'):
                response_of_translation = chatgpt_by_api(st.session_state.translation)["chat_text"]
                response_of_translation = st.text_area('**ChatGPT Response Text:**', value=response_of_translation, height=300)
                st.session_state.response_of_translation = response_of_translation
            else:
                response_of_translation = st.text_area('**ChatGPT Response Text:**', value=st.session_state.response_of_translation, height=300)
                st.session_state.response_of_translation = response_of_translation
        except Exception as e:
            logging.info(e)
            response_of_translation = st.text_area('**ChatGPT Response Text:**',
                                                   value="error, try it again", height=300)
            st.session_state.response_of_translation = response_of_translation

        try:
            if st.button('Translate Response'):
                translation_of_response = translate_by_api(st.session_state.response_of_translation, True, model=response_trans)[
                    'translation']
                translation_of_response = st.text_area('**Translation of ChatGPT Response Text:**',
                                                       value=translation_of_response, height=300)

                st.session_state.translation_of_response = translation_of_response
            else:
                translation_of_response = st.text_area('**Translation of ChatGPT Response Text:**',
                                                       value=st.session_state.translation_of_response, height=300)
                st.session_state.translation_of_response = translation_of_response
        except Exception as e:
            logging.info(e)
            translation_of_response = st.text_area('**Translation of ChatGPT Response Text:**',
                                                   value="error, try it again", height=300)
            st.session_state.translation_of_response = translation_of_response

    with col2:
        st.subheader('Service without Translation')
        try:
            if st.session_state.text_input2:
                text_input2 = st.text_area('**Text Input:**', value=st.session_state.text_input2, key='Text_Input2', height=300)
                st.session_state.text_input2 = text_input2
            else:
                text_input2 = st.text_area('**Text Input:**', value=st.session_state.recognized_text, key='Text_Input2', height=300)
                st.session_state.text_input2 = text_input2
        except Exception as e:
            logging.info(e)
            text_input2 = st.text_area('**Text Input:**', value="error, try it again", key='Text_Input2',
                                       height=300)
            st.session_state.text_input2 = text_input2

        try:
            if st.button('ChatGPT Dialogue', key='ChatGPT_Dialogue2'):
                response_of_translation2 = chatgpt_by_api(st.session_state.text_input2)["chat_text"]
                response_of_translation2 = st.text_area('**ChatGPT Response Text:**', value=response_of_translation2,
                                                        key='ChatGPT_Response_Text2', height=300)
                st.session_state.response_of_translation2 = response_of_translation2

            else:
                response_of_translation2 = st.text_area('**ChatGPT Response Text:**', value=st.session_state.response_of_translation2,
                                                        key='ChatGPT_Response_Text2', height=300)
                st.session_state.response_of_translation2 = response_of_translation2
        except Exception as e:
            logging.info(e)
            response_of_translation2 = st.text_area('**ChatGPT Response Text:**',
                                                    value="error, try it again",
                                                    key='ChatGPT_Response_Text2', height=300)

            st.session_state.response_of_translation2 = response_of_translation2

