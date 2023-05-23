# Multilingual Evaluation


In the following human evaluation, we have selected 4 questions, covering three major tasks: text generation, code generation, and summarization. 
For direct answers in the target language, we provide translated English explanations. 
All raw text for the evaluation can be found in [the link below](./multilingual).

Additionally, all conclusions below come from developer's human evaluation and are highly subjective. 
Furthermore, the quality of the translation can also affect the judgment of the output result's quality.
We look forward to native speakers of the evaluated languages providing more extensive and professional evaluations using our tool.

## Situation 1
Languages that perform better when asked directly in the target language rather than after translation into English:

| Language | Comments                                                                     |
|----------|------------------------------------------------------------------------------|
| greek    | The direct asking in the target language is more detailed in text generation.|
| javanese | The direct asking in the target language is more detailed in text generation.|

## Situation 2
Languages that perform worse when asked directly in the target language rather than after translation into English:

| Language | Comments                                                                                                                                                                  |
|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| albanian | The text generated from asking in English is more detailed, while the summary is more concise.                                                                            |
| arabic   | Direct asking in the target language may not accurately understand the command.                                                                                           |
| armenian | Direct asking in the target language may not accurately understand the command in text generation task.                                                                   |
| assamese | The text generated from asking in English is more detailed, while the summary is more concise.                                                                            |
| basque | The text generated from asking in English is more detailed.                                                                                                               |
| bengali | The summary generated from asking in English is more concise.                                                                                                             |
| bosnian | The code generated from asking in English is better.                                                                                                                      |
| breton | The summary generated from asking in English is more concise.                                                                                                             |
| croatian | The summary generated from asking in English is more concise.                                                                                                             |
| czech   | Direct asking in the target language may not accurately understand the command in code generation task.                                                                   |
| estonian | Direct asking in the target language may not accurately understand the command in text generation task.                                                                   |
| faroese | Direct asking in the target language may not accurately understand the command in text generation and code generation task.                                               |
| finnish | Direct asking in the target language may not accurately understand the command in text generation task.                                                                   |
| georgian | Direct asking in the target language may not accurately understand the command in text generation task.                                                                   |
| gujarati | Direct asking in the target language may not accurately understand the command in code generation task, lack detail in text generation, and are not concise in summaries. |
| hebrew | The text generated from asking in English is more detailed.                                                                                                               |
| hungarian | Direct asking in the target language may not accurately understand the command in text generation task.                                                                   |
| japanese | Direct asking in the target language may not accurately understand the command in text generation task.                                                                   |
| kannada | The text generated from asking in English is more detailed, while the summary is more concise.                                                                            |
| korean | Direct asking in the target language may not accurately understand the command in text generation task.                                                                   |
| latvian | Direct asking in the target language may not accurately understand the command in code generation task, and are not concise in summaries.                                 |
| maltese | Direct asking in the target language may not accurately understand the command in code generation task, and are not concise in summaries.                                 |
| marathi | The text generated and code generated from asking in English are more detailed.                                                                                           |
| nepali | Direct asking in the target language fails to answer questions correctly in both text generation and code generation.                                                     |
| portuguese | The summary generated from asking in English is more concise.                                                                                                             |
| punjabi | Direct asking in the target language may not accurately understand the command in code generation task.                                                                   |
| russian | Direct asking in the target language may not accurately understand the command in text generation task.                                                                   |
| sanskrit | Direct asking in the target language may not accurately understand the command in code generation task.                                                                   |
| sundanese | Direct asking in the target language may not accurately understand the command in summarization task.                                                                     |
| telugu | The text generated from asking in English are more detailed.                                                                                                              |
| thai | Direct asking in the target language may not accurately understand the command in text generation and code generation tasks.                                              |
| turkmen | Direct asking in the target language may not accurately understand the command in code generation task.                                                                   |
| urdu | Direct asking in the target language fails to answer questions correctly in both text generation and code generation.                                                     |
| uzbek | Direct asking in the target language fails to answer questions correctly in code generation.                                                                              |
| welsh | The text and code generated from asking in English are more detailed.                                                                                                     |
| yiddish | Direct asking in the target language fails to answer questions correctly in text generation.                                                                              |



## Situation 3
Languages that perform similarly when asked directly in the target language and after translation into English:

| Language | Comments                                      |
|----------|-----------------------------------------------|
| afrikaans | The performance is good for both two methods. |
| azerbaijani | The performance is good for both two methods. |
| bashkir | In our example, asking directly in the target language yields better code generation results, but poorer text generation capabilities. |
| belarusian | The performance is good for both two methods. |
| bulgarian | The performance is good for both two methods. |
| catalan | The performance is good for both two methods. |
| danish | The performance is good for both two methods. |
| dutsch | The performance is good for both two methods. |
| french | The performance is good for both two methods. |
| galician | The performance is good for both two methods. |
| german | The performance is good for both two methods. |
| hindi | The performance is good for both two methods. |
| icelandic | The performance is good for both two methods. |
| indonesian | The performance is good for both two methods. |
| italian | The performance is good for both two methods. |
| kazakh | The performance is good for both two methods. |
| latin | In our example, asking directly in the target language cannot correctly understand the question in code generation and summary. Asking directly in English cannot correctly understand the question in text generation. |
| lithuanian | The performance is good for both two methods. |
| luxembourgish | The performance is good for both two methods. |
| macedonian | The performance is good for both two methods. |
| malay | The performance is good for both two methods. |
| norwegian | The performance is good for both two methods. |
| nynorsk | The performance is good for both two methods. |
| occitan | The performance is good for both two methods. |
| persian | The performance is good for both two methods. |
| polish | The performance is good for both two methods. |
| romanian | The performance is good for both two methods. |
| serbian | The performance is good for both two methods. |
| slovak | The performance is good for both two methods. |
| slovenian | The performance is good for both two methods. |
| somali | The performance is good for both two methods. |
| spanish | The performance is good for both two methods. |
| swahili | The performance is good for both two methods. |
| swedish | The performance is good for both two methods. |
| tagalog | The performance is good for both two methods. |
| tajik | The performance is good for both two methods. |
| turkish | The performance is good for both two methods. |
| ukrainian | The performance is good for both two methods. |
| vietnamese | The performance is good for both two methods. |

## Conclusion

In the vast majority of cases, if you have a good translation model, 
asking after translating the question into English often yields results that are not inferior to, and even surpass, 
asking directly in the target language. 
This is primarily reflected in ChatGPT's superior understanding of English questions and its ability to generate more detailed content. 
However, the difference in performance is not significant for high resource languages or certain languages that are close to English. 
Moreover, for low resource languages, translating into English may be limited by the translation tool's support for that language, 
leading to substantial translation errors that result in responses that miss the point of the original question.


