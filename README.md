# nlp-synt-data [![PyPi version](https://img.shields.io/pypi/v/nlp-synt-data.svg)](https://pypi.python.org/pypi/nlp-synt-data/) [![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/) ![t](https://img.shields.io/badge/status-maintained-yellow.svg) [![](https://img.shields.io/github/license/tommasoromano/nlp-synt-data.svg)](https://github.com/tommasoromano/nlp-synt-data/blob/master/LICENSE.md)

Synthetic Data Tools for Natural Language Processing (NLP) and Large Language Models (LLM) tasks

- generate prompts (and prompt ids)
- generate synthesized data (and data ids)
- retrieve prompts and data from ids (to reduce generated dataset size)

## Installation

```
pip install nlp-synt-data
```

## PromptGenerator

### generate

```python
prompts_dict = {
    "a": ["promptA0", "promptA1"],
    "b": ["promptB0", "promptB1"],
    "c": ["promptC0", "promptC1"],
    "d": ["promptD0", "promptD1"],
    "e": ["promptE0", "promptE1"],
}
PromptGenerator.generate(prompts_dict, [["c","e"],["a","b","d"]])
```

```
[('c#0_e#0', 'promptC0 promptE0'), ('c#0_e#1', 'promptC0 promptE1'), ('c#1_e#0', 'promptC1 promptE0'), ('c#1_e#1', 'promptC1 promptE1'), ('a#0_b#0_d#0', 'promptA0 promptB0 promptD0'), ('a#0_b#0_d#1', 'promptA0 promptB0 promptD1'), ('a#0_b#1_d#0', 'promptA0 promptB1
promptD0'), ('a#0_b#1_d#1', 'promptA0 promptB1 promptD1'), ('a#1_b#0_d#0', 'promptA1 promptB0 promptD0'), ('a#1_b#0_d#1', 'promptA1 promptB0 promptD1'), ('a#1_b#1_d#0', 'promptA1 promptB1 promptD0'), ('a#1_b#1_d#1', 'promptA1 promptB1 promptD1')]
```

### get

```python
PromptGenerator.get("c#0_e#0", prompts_dict)
```

```
promptC0 promptE0
```

## DataGenerator

### generate

```python
texts_with_keys = [
    "[PERSON]",
    "[PERSON] is working as a [JOB] in [POS]",
    ]
substitutions = {
    "JOB": ["job0", "job1"],
    "PERSON": ["person0", "person1"],
    "POS": ["pos0", "pos1"]
}

DataGenerator.generate(texts_with_keys, substitutions)
```

```
[('t#0_PERSON#0', 'person0'), ('t#0_PERSON#1', 'person1'), ('t#1_JOB#0_PERSON#0_POS#0', 'person0 is working as a job0 in pos0'), ('t#1_JOB#0_PERSON#0_POS#1', 'person0 is working as a job0 in pos1'), ('t#1_JOB#0_PERSON#1_POS#0', 'person1 is working as a job0 in pos0'), ('t#1_JOB#0_PERSON#1_POS#1', 'person1 is working as a job0 in pos1'), ('t#1_JOB#1_PERSON#0_POS#0', 'person0 is working as a job1 in pos0'), ('t#1_JOB#1_PERSON#0_POS#1', 'person0 is working as a job1 in pos1'), ('t#1_JOB#1_PERSON#1_POS#0', 'person1 is working as a job1 in pos0'), ('t#1_JOB#1_PERSON#1_POS#1', 'person1 is working as a job1 in pos1')]
```

### get

```python
DataGenerator.get("t#1_JOB#0_PERSON#0_POS#0", texts_with_keys, substitutions)
```

```
{'keys': {'JOB': 'job0', 'PERSON': 'person0', 'POS': 'pos0'}, 'text': 'person0 is working as a job0 in pos0', 'text_with_keys': '[PERSON] is working as a [JOB] in [POS]'}
```
