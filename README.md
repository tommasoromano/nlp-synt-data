nlp-synt-data

# Synthesized Data for Natural Language Processing

## Synthesized Data

### PromptGenerator

#### generate

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

#### get

```python
PromptGenerator.get("c#0_e#0", prompts_dict)
```

```
promptC0 promptE0
```
