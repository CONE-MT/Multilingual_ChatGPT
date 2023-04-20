import os
import requests
import json
import argparse
import openai
from os.path import join
import whisper
from datetime import datetime
import yaml
import pickle
import logging
logging.basicConfig(level=logging.INFO)


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
    # print("chatgpt response: {}".format(chat_text))
    return {'text': text, 'chat_text': chat_text}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--translate', action='store_true', help='enable translate mode')
    parser.add_argument('--translate_method', type=str, default="cone")
    args = parser.parse_args()

    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)
    with open('name2langid.pickle', 'rb') as f:
        name2langid = pickle.load(f)

    name2langid["javanese"] = "jv"
    name2langid["hebrew"] = "he"

    API_KEY = config["API_KEY"]
    source_lang_name = config["source_lang"].lower()
    target_lang_name = config["target_lang"].lower()

    source_lang = name2langid[source_lang_name]
    target_lang = name2langid[target_lang_name]

    is_trans = True
    is_chatgpt = True
    response_trans = config["response_trans"]

    while True:
        text = input("You:")
        print("\n")

        if not args.translate:
            direct_response = chatgpt_by_api(text)["chat_text"]
            print("ChatGPT: {}".format(direct_response))
            print("\n")
        else:
            translation = translate_by_api(text, False, model=args.translate_method)['translation']
            print("translation: {}".format(translation))
            print("\n")
            if response_trans == "prompt":
                final_result = chatgpt_by_api(
                    text + " " + "Please respond to the above request in {} language.".format(source_lang_name))
                print("ChatGPT: {}".format(final_result["chat_text"]))
                print("\n")

            else:
                response_of_translation = chatgpt_by_api(translation)["chat_text"]
                print("ChatGPT response: {}".format(response_of_translation))
                print("\n")
                translation_of_response = translate_by_api(response_of_translation, True, model=response_trans)['translation']

                # print("translation_of_response: {}".format(translation_of_response))

                print("translation of ChatGPT response: {}".format(translation_of_response))
                print("\n")
