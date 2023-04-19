import os
from flask import Flask, render_template, request, jsonify
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

app = Flask(__name__, template_folder='./')


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


def completions(text, src, tar, org_text=None):
    text = " ".join(text)

    url = 'https://cone.x-venture.tech/gw/service/cone/v1/engines/175b/completions'
    headers = {'Content-Type': 'application/json'}

    if org_text is None:
        res = requests.post(url, json={"prompt": text, "src": src, "tar": tar, "origin_prompt": text}, headers=headers)
    else:
        res = requests.post(url, json={"prompt": text, "src": src, "tar": tar, "origin_prompt": org_text},
                            headers=headers)

    # print(res, tar)
    print(json.loads(res.content), tar)
    return json.loads(res.content)


def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x


def translate_by_api(text, reverse, model="cone"):
    translation = "You have turned off the translation function."
    if is_trans:
        print("start translation")
        if model == "cone":
            if reverse is False:
                if split_sentence and source_lang in ["en", "zh"]:
                    sentence_segment_model = spacy.load("{}_core_web_md".format(source_lang))
                    doc = sentence_segment_model(text)
                    all_sentence = [str(sent) for sent in doc.sents]
                    if len(all_sentence) < 2:
                        result_s1 = completions([text], source_lang, target_lang)
                        translation = result_s1["choices"][0]["text"]
                    else:
                        p = Pool(processes=min(20, len(all_sentence)))
                        node_divisor = len(p._pool) * 1
                        node_chunks = list(chunks(all_sentence, len(all_sentence) // node_divisor))
                        num_chunks = len(node_chunks)
                        logging.info("num of chunks: {} {}".format(num_chunks, node_chunks))

                        parallel_return = p.starmap(
                            completions,
                            zip(
                                node_chunks,
                                [source_lang] * num_chunks,
                                [target_lang] * num_chunks,
                            ),
                        )

                        results_list = [i["choices"][0]["text"] for i in parallel_return]
                        translation = " ".join(results_list)
                else:
                    result_s1 = completions([text], source_lang, target_lang)
                    translation = result_s1["choices"][0]["text"]
            else:
                if split_sentence and target_lang in ["en", "zh"]:
                    sentence_segment_model = spacy.load("{}_core_web_md".format(target_lang))
                    doc = sentence_segment_model(text)
                    all_sentence = [str(sent) for sent in doc.sents]
                    # print(all_sentence)
                    if len(all_sentence) < 2:
                        result_s1 = completions([text], target_lang, source_lang)
                        translation = result_s1["choices"][0]["text"]
                    else:
                        p = Pool(processes=min(20, len(all_sentence)))
                        node_divisor = len(p._pool) * 1
                        node_chunks = list(chunks(all_sentence, len(all_sentence) // node_divisor))
                        num_chunks = len(node_chunks)
                        logging.info("num of chunks: {}".format(num_chunks))
                        # print(node_chunks)

                        parallel_return = p.starmap(
                            completions,
                            zip(
                                node_chunks,
                                [target_lang] * num_chunks,
                                [source_lang] * num_chunks,
                            ),
                        )

                        results_list = [i["choices"][0]["text"] for i in parallel_return]
                        translation = " ".join(results_list)
                else:
                    result_s1 = completions([text], target_lang, source_lang)
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
    print("translation: {}".format(translation))
    return {'translation': translation}


def chatgpt_by_api(text):
    chat_text = "You have turned off the ChatGPT function."
    if is_chatgpt:
        print("start request chatgpt: {}".format(text))
        prompt = text
        chat_text = chatgpt_response(prompt)
    print("chatgpt response: {}".format(chat_text))
    return {'text': text, 'chat_text': chat_text}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_audio', methods=['POST'])
def process():
    print("start")

    # output_root = "./cache"
    # os.system("mkdir -p {}".format(output_root))
    current_datetime = datetime.now()
    str_current_datetime = str(current_datetime).replace(" ", "-")
    print("str_current_datetime: {}".format(str_current_datetime))
    file_name = str_current_datetime + ".wav"
    wav_path = join(output_root, file_name)

    audio_data = request.files.get('audio_data')

    # 将音频数据保存为wav文件
    try:
        with open(wav_path, 'wb') as f:
            f.write(audio_data.read())
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
    return jsonify({'text': text})


@app.route('/process_info', methods=['POST'])
def process_info():
    credentials = request.get_json()
    global API_KEY
    API_KEY = credentials.get('API_key')

    # print("API_KEY: {}".format(API_KEY))
    return jsonify({'status': 'success'})


@app.route('/get_translation', methods=['POST'])
def get_translation():
    # 从请求中获取输入文本
    text = request.get_json().get('input_text')
    reverse = request.get_json().get('reverse')
    model = request.get_json().get('model')

    print("input text: {}".format(text))

    final_result = translate_by_api(text, reverse=reverse, model=model)
    return jsonify(final_result)


@app.route('/get_chatgpt', methods=['POST'])
def get_chatgpt():
    # 从请求中获取输入文本
    text = request.get_json().get('input_text')
    translate = request.get_json().get('translate')
    print("input text: {}, translate: {} response_trans: {}".format(text, translate, response_trans))

    if not translate:
        final_result = chatgpt_by_api(text)
        return jsonify(final_result)
    else:
        if response_trans == "prompt":
            final_result = chatgpt_by_api(text + " " + "Please respond to the above request in {} language.".format(source_lang_name))
            return jsonify(final_result)
        else:
            final_result = chatgpt_by_api(text)
            chat_text = final_result["chat_text"]
            translation = translate_by_api(chat_text, True, model=response_trans)['translation']
            return jsonify({'text': final_result['text'], 'chat_text': translation})


if __name__ == '__main__':
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

    print("source_lang_name: {} target_lang_name: {} source_lang: {} target_lang: {}".format(source_lang_name, target_lang_name, source_lang, target_lang))
    output_root = config["output_root"]
    is_trans = True
    is_chatgpt = True
    split_sentence = config["split_sentence"]
    response_trans = config["response_trans"]
    os.system("mkdir -p {}".format(output_root))

    app.run(debug=True)
