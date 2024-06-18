from generator import *

if __name__ == '__main__':
    prompts_dict = {
        "a": ["promptA0", "promptA1"],
        "b": ["promptB0", "promptB1"],
        "c": ["promptC0", "promptC1"],
        "d": ["promptD0", "promptD1"],
        "e": ["promptE0", "promptE1"],
    }
    prompts = PromptGenerator.generate(prompts_dict, [["c","e"],["a","b","d"]])
    print(prompts)
    print(PromptGenerator.get("c#0_e#0", prompts_dict))