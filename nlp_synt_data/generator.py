from itertools import combinations
import pandas as pd
import os

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
    def generate(
        texts_with_keys: list[tuple[str,str]],
        substitutions: dict[str,list[tuple[str,str]]],
    ):
        """- texts_with_keys: list of (text with keys, label)
        - substitutions: dict of list of (substitution, label)
        - returns: list of tuple (text_id, text, list of labels)"""

        final_texts = []

        if "t" in substitutions:
            raise ValueError("Key 't' is reserved for text id")
        if any([any(char.isdigit() for char in key) for key in substitutions]):
            raise ValueError("Keys cannot contain numbers")
        if any([any(char == '_' for char in key) for key in substitutions]):
            raise ValueError("Keys cannot contain underscores")
        if any([any(char == '#' for char in key) for key in substitutions]):
            raise ValueError("Keys cannot contain #")
        
        def add_text(key, prev_prompts):
            return [
            (f"{p_key}_{key}#{x_i}", p_p.replace(f"[{key}]", x_p), p_ls+[x_l])
            for p_key, p_p, p_ls in prev_prompts
            for x_i, (x_p, x_l) in enumerate(substitutions[key])
            ]
        
        final_texts = []

        for it, (text, label) in enumerate(texts_with_keys):
            _real_keys = [key for key in substitutions if key in text]
            acc_texts = [(f"t#{it}", text, [label])]
            for key in _real_keys:
                acc_texts = add_text(key, acc_texts)
            final_texts += acc_texts

        return final_texts
    
    @staticmethod
    def get(
        text_id: str,
        texts_with_keys: list[tuple[str,str]],
        substitutions: dict[str,list[tuple[str,str]]],
    ):
        
        keys = text_id.split("_")
        if keys[0][:2] != "t#":
            raise ValueError("Invalid text id")
        
        res = {
            'keys': {},
        }
        res['text_with_keys'] = texts_with_keys[int(keys[0].split("#")[1])]
        text = res['text_with_keys'][0]
        for _key in keys[1:]:
            n = int(_key.split("#")[1])
            key = _key.split("#")[0]
            if key not in substitutions:
                raise ValueError(f"Key {key} not in substitutions")
            if n >= len(substitutions[key]):
                raise ValueError(f"Index {n} out of range for key {key}")
            
            res["keys"][key] = substitutions[key][n]
            text = text.replace(f"[{key}]", substitutions[key][n][0])
        res["text"] = (text, res["text_with_keys"][1])
        return res
    
class ResponseGenerator():

    @staticmethod
    def generate(
        file_path: str,
        texts: list[tuple[str, str, str]],
        prompts: list[tuple[str, str]],
        model_func: callable,
        save_every: int = 50,
        make_labels: bool = True,
        verbose: bool = True,
    ):
        """- data_path_name: name of the data file to save/load
        - texts: list of tuples (text_id, text)
        - prompts: list of tuples (prompt_id, prompt)
        - model_func: function that takes (prompt, text) and returns response
        """

        try:
            res_df = pd.read_csv(file_path)
            verbose and print(f"Loaded {len(res_df)} rows.")
            make_labels = 'text_labels' in res_df.columns
        except: 
            if not make_labels:
                res_df = pd.DataFrame({'prompt_id':[], 'text_id':[], 'response':[]})
            else:
                res_df = pd.DataFrame({'prompt_id':[], 'text_id':[], 'text_labels':[], 'response':[]})
            verbose and print("Created new dataframe.")

        for prompt_id, prompt in prompts:
            for text_id, text, labels in texts:

                if len(res_df) > 0 and res_df[(res_df['prompt_id'] == prompt_id) & (res_df['text_id'] == text_id)].shape[0] > 0:
                    continue

                res = model_func(prompt, text)
                if make_labels:
                    res_df.loc[len(res_df)] = [prompt_id, text_id, str(labels), res]
                else:
                    res_df.loc[len(res_df)] = [prompt_id, text_id, res]

                if len(res_df) % save_every == 0:
                    verbose and print(f"Processed {len(res_df)} rows.")
                    res_df.to_csv(file_path, index=False)

class Utils():

    @staticmethod
    def list_to_dict(ls: list[tuple[str,str]]):
        """- ls: list of (text, label)
        - return: dict of label: text"""
        return {l:list(map(lambda x: x[0], filter(lambda x: x[1] == l, ls)))  for l in set([l for t,l in ls])}