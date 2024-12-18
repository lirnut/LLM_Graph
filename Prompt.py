import openai
import requests
from io import BytesIO
from PIL import Image
import json
import argparse
from langchain.prompts import PromptTemplate
from openai import OpenAI
import os
import mimetypes

format_exn = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "GIF": ".gif",
    "BMP": ".bmp",
    "TIFF": ".tif",
    "WebP": ".webp",
    "HEIF": ".heif",
    "ICO": ".ico",
    "SVG": ".svg",
    "RAW": ".raw",  
}

class Processer:
    def __init__(self):
        return None

    def arg_load(self):
        parser = argparse.ArgumentParser(description='Argument for this Prompt Model.')

        parser.add_argument('--prompt_json',
            default = "./prompt.json", 
            type = str,
            help ='The Location of prompt .json file.')
        parser.add_argument('--llm',
            default = "gpt-4", 
            type = str,
            help ='The Model of LLM.')
        parser.add_argument('--img_model',
            default = 'dall-e-3 ', 
            type = str,
            help ='Text to Image Model.')
        parser.add_argument('--max_tokens',
            default = 1000, 
            type = int,
            help = 'The Max number of LLM generates.')    
        parser.add_argument('--temperature',
            default = 0.7, 
            type = float,
            help = 'The temperature of LLM.')    
        parser.add_argument('--img_sz',
            default = "1024x1024", 
            type = str,
            help = 'The size of generated image.') 
        parser.add_argument('--img_format',
            default = "JPEG", 
            type = str,
            help = 'The format of generated image.') 
        parser.add_argument('--img_n',
            default = 2, 
            type = int,
            help = 'The number of generated image.') 
        parser.add_argument('--save_path',
            default = './', 
            type = str,
            help = 'The number of generated image.') 
        parser.add_argument('--prompt_task',
            default = '这是我的思路和具体实现，接下来请给出一个与之匹配的例子', 
            type = str,
            help = 'Your requirement for llm prompt generating.') 
        parser.add_argument('--img_task',
            default = '这是我的思路和具体实现，接下来请给出与之匹配的example', 
            type = str,
            help = 'Your requirement for image generating.') 
        
        self.args = parser.parse_args()


    def gen_img_prompt(self):
        try:
            response = openai.chat.completions.create(
                model = self.args.llm,  
                max_tokens = self.args.max_tokens,  
                temperature = self.args.temperature,  
                messages = [
                    {'role': 'system', 'content': self.args.prompt_task}, 
                    {'role': 'user', 'content': self.prompt}, 
                ]
            )
            self.img_prompt = response.choices[0].message.content
            print(f"{self.args.llm} Prompt: {self.img_prompt}")
            return self.img_prompt
        
        except Exception as e:
            print(f"Generating Prompt Runtime ERROR: {e}")
            return None


    def gen_img(self):
        try:
            response = openai.images.generate(
                n = self.args.img_n,             
                size = self.args.img_sz,
                prompt = self.args.img_task + '\n' + self.img_prompt,         
            )
            cnt = 1
            for img in response.data:
                image_url = img.url
                print(f"Generated Image URL: {image_url}")
                img_response = requests.get(image_url)
                img = Image.open(BytesIO(img_response.content))
                img.save(
                    os.path.join(self.args.save_path, 
                        "{:03d}".format(cnt) + format_exn[self.args.img_format]),
                    format = self.args.img_format)
                print("{:03d}".format(cnt) + format_exn[self.args.img_format] + " Saved!")
                cnt += 1
            return response.data
        
        except Exception as e:
            print(f"Generating Imgage Runtime ERROR: {e}")
            return None
    

    def json_load(self):
        try:
            with open(self.args.prompt_json, 'r', encoding='utf-8') as f:
                self.raw_prompt = json.load(f)
            return self.raw_prompt    
        
        except Exception as e:
            print(f".json loading ERROR: {e}")
            return None        
    

    def gen_llm_prompt(self):
        self.prompt = ""
        for prompt_entry in self.raw_prompt:
            self.prompt += "Mind:" + prompt_entry["PromptMind"] + "\n"
            prompt_template = prompt_entry['PromptTemplate']['template']
            input_variables = prompt_entry['PromptTemplate']['input_variables']
            template = PromptTemplate(input_variables=input_variables, template=prompt_template)
            for example in prompt_entry['Example']:
                self.prompt += "Example:" + template.format(**dict(zip(input_variables, example))) + '\n'
            self.prompt += '\n'
        return self.prompt
    
    
if __name__ == "__main__":
    pro = Processer()
    pro.arg_load()
    pro.json_load()
    pro.gen_llm_prompt()
    print(pro.args.prompt_task + '\n' + pro.prompt)
    pro.gen_img_prompt()
    pro.gen_img()