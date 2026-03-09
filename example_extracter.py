import os
from openai import OpenAI
import json

os.environ["GEMINI_API_KEY"]=""


prompt1 = """
    You are an expert in summarization.
    
    ### CONTEXT:
    {text}
    
    
    ### TASK:
    Summarize the above text in 5 bullet points.
"""


prompt="""
    You are generating structured training data for a LangExtract task.

    Step 1:
    Analyze the following original task prompt and determine appropriate attributes that describe the expected output quality or characteristics.

    Step 2:
    Generate exactly 3 examples derived from the given context.

    Each example must contain:
    - text: the original context
    - extraction_text: the expected output for the task
    - attributes: a dictionary of key–value pairs describing relevant attributes for this task

    Output must be valid JSON.
    Do not include variable names.
    Do not include markdown.
    Return only a JSON array.

    Rules:
    - Attribute names must be meaningful and aligned with the task.
    - Attribute values must be concise (1–3 words).
    - extraction_text must logically match the original task.
    - Output must be valid Python.
    - Do NOT include explanations.
    - Do NOT include markdown.
    - Output only the Python variable assignment.

    Output format:
    [
        {{
            "text": "...",
            "extraction_text": "...",
            "attributes": {{
                "attribute_name_1": "value",
                "attribute_name_2": "value"
            }}
        }},
        {{
            "text": "...",
            "extraction_text": "...",
            "attributes": {{
                "attribute_name_1": "value",
                "attribute_name_2": "value"
            }}
        }},
        {{
            "text": "...",
            "extraction_text": "...",
            "attributes": {{
                "attribute_name_1": "value",
                "attribute_name_2": "value"
            }}
        }}
    ]


    Original Task Prompt:
    -------------------------
    {original_prompt}
    -------------------------

    Context:
    -------------------------
    {long_text}
    -------------------------


"""

class param_ext:
    def __init__(self,prompt):
        self.prompt=prompt
    def generate(self,data):
        #model
        client=OpenAI(base_url='https://generativelanguage.googleapis.com/v1beta/openai/', api_key=os.environ["GEMINI_API_KEY"])
        #modelfeed
        op=client.chat.completions.create(
            model='gemini-2.5-flash',
            messages=[{
                "role":'user',
                'content': self.prompt.format(original_prompt=prompt1.format(text=data),long_text=data)
            }
            ]
        )
        return op.choices[0].message.content

def chunk_code(code, chunk_size=1000):
    return [code[i:i+chunk_size] for i in range(0, len(code), chunk_size)]

long_text=open('./rag/LangEXT/1.txt','r').read()
text=chunk_code(long_text)
print(len(text))


obj=param_ext(prompt)
res=obj.generate(text[0])
print(res)


data=json.loads(res)

# print(data)
print(type(data))

t1=data[0]['attributes']
t2=data[1]['extraction_text']
t3=data[2]['extraction_text']

print('-*-*'*20)
print(t1)
print('-*-*'*20)
print(t2)
print('-*-*'*20)
print(t3)



# op=json.loads(res)  
# print(op)