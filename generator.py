import pandas as pd
import os
from functools import reduce

class PromptGenerator():

    @staticmethod
    def generate(
        prompts_dict: dict,
        prompt_keys: list[list[str]]
    ):
        """- prompts_dict: dict of prompts to be generated
        - prompt_keys: list of prompt keys to be generated 
        e.g. [[c,e],] generates [(c#0_e#0, promptC0+promptE0), (c#0_e#1, promptC0+promptE1), ..]
        - returns: list of tuples of (prompt_id, prompt_text).
        """

        def check_key(key):
            if key not in prompts_dict:
                raise ValueError(f"Key {key} not in prompts_dict")
            if any(char.isdigit() for char in key):
                raise ValueError(f"Key {key} contains numbers, which is not allowed")
            if any(char == "_" for char in key):
                raise ValueError(f"Key {key} contains underscores, which is not allowed")
            if any(char == "#" for char in key):
                raise ValueError(f"Key {key} contains underscores, which is not allowed")

        def add_prompts(key, prev_prompts):
            return [
            (f"{p_key}_{key}#{x_i}", p_p + ' ' + x_p)
            for p_key, p_p in prev_prompts
            for x_i, x_p in enumerate(prompts_dict[key])
            ]
        

        final_prompts = []

        for keys in prompt_keys:

            if len(keys) < 1:
                raise ValueError("Prompt keys must be at least 1")
            check_key(keys[0])
            acc_prompts = [(f"{keys[0]}#{i}", p) for i,p in enumerate(prompts_dict[keys[0]])]

            for key in keys[1:]:
                check_key(key)
                acc_prompts = add_prompts(key, acc_prompts)

            final_prompts += acc_prompts
        return final_prompts

    @staticmethod
    def get(
        prompt_id: str,
        prompts_dict: dict
    ):
        """- prompt_id: string of prompt_id to get
        - prompts_dict: 
        - returns: prompt
        """
        prompt = ""
        keys = prompt_id.split("_")
        for _key in keys:
            n = int(_key.split("#")[1])
            key = _key.split("#")[0]
            if key not in prompts_dict:
                raise ValueError(f"Key {key} not in prompts_dict")
            if n >= len(prompts_dict[key]):
                raise ValueError(f"Index {n} out of range for key {key}")

            if prompt != "":
                prompt += " " + prompts_dict[key][n]
            else:
                prompt += prompts_dict[key][n]

        return prompt
    

class DataGenerator():

    @staticmethod
    def generate():

        return