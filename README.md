# nlp-synt-data [![PyPi version](https://img.shields.io/pypi/v/nlp-synt-data.svg)](https://pypi.python.org/pypi/nlp-synt-data/) [![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/) ![t](https://img.shields.io/badge/status-maintained-yellow.svg) [![](https://img.shields.io/github/license/tommasoromano/nlp-synt-data.svg)](https://github.com/tommasoromano/nlp-synt-data/blob/master/LICENSE.md)

Synthetic Data Tools for Natural Language Processing (NLP) and Large Language Models (LLM) tasks

- generate prompts (and prompt ids)
- generate synthetic data (and data ids)
- retrieve prompts and data from ids (to reduce generated dataset size)

## Installation

```
pip install nlp-synt-data
```

## Quickstart

An example of this library with `ollama`

```python
from nlp_synt_data import *
import ollama

# generate prompts
prompts_dict = {
    "a": ["promptA0", "promptA1"],
    "b": ["promptB0", "promptB1"],
    "c": ["promptC0", "promptC1"],
    "d": ["promptD0", "promptD1"],
    "e": ["promptE0", "promptE1"],
}
prompts = PromptGenerator.generate(prompts_dict, [["c","e"],["a","b","d"]])

# generate texts
texts_with_keys = [
    ("[PERSON]","label0"),
    ("[PERSON] is working as a [JOB] in [POS]","label1"),
    ]
substitutions = {
    "JOB": [("job0","labeljob0"), ("job1","labeljob1")],
    "PERSON": [("person0","labelperson0"), ("person1","labelperson1")],
    "POS": [("pos0","labelpos0"), ("pos1","labelpos1")]
}
texts = DataGenerator.generate(texts_with_keys, substitutions)

# generate responses
model_func = lambda prompt, text: ollama.chat(model='llama3:instruct', messages=[
                { 'role': 'system', 'content': prompt, },
                { 'role': 'user', 'content': text, },
            ])['message']['content']
ResponseGenerator.generate("results.csv", texts, prompts, model_func)
```

results.csv

| prompt_id | text_id                  | text_labels                                          | response |
| --------- | ------------------------ | ---------------------------------------------------- | -------- |
| c#0_e#0   | t#0_PERSON#0             | ['label0', 'labelperson0']                           | response |
| c#0_e#0   | t#0_PERSON#1             | ['label0', 'labelperson1']                           | response |
| c#0_e#0   | t#1_JOB#0_PERSON#0_POS#0 | ['label1', 'labeljob0', 'labelperson0', 'labelpos0'] | response |
| c#0_e#0   | t#1_JOB#0_PERSON#0_POS#1 | ['label1', 'labeljob0', 'labelperson0', 'labelpos1'] | response |
| c#0_e#0   | t#1_JOB#0_PERSON#1_POS#0 | ['label1', 'labeljob0', 'labelperson1', 'labelpos0'] | response |
| c#0_e#0   | t#1_JOB#0_PERSON#1_POS#1 | ['label1', 'labeljob0', 'labelperson1', 'labelpos1'] | response |
| c#0_e#0   | t#1_JOB#1_PERSON#0_POS#0 | ['label1', 'labeljob1', 'labelperson0', 'labelpos0'] | response |
| c#0_e#0   | t#1_JOB#1_PERSON#0_POS#1 | ['label1', 'labeljob1', 'labelperson0', 'labelpos1'] | response |
| c#0_e#0   | t#1_JOB#1_PERSON#1_POS#0 | ['label1', 'labeljob1', 'labelperson1', 'labelpos0'] | response |
| c#0_e#0   | t#1_JOB#1_PERSON#1_POS#1 | ['label1', 'labeljob1', 'labelperson1', 'labelpos1'] | response |
| ...       | ...                      | ...                                                  | ...      |
