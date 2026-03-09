import langextract as lx
import textwrap
import os
import json
from openai import OpenAI
import sys

os.environ.setdefault("OPENAI_API_KEY","")
os.environ.setdefault("GEMINI_API_KEY","")
os.environ.setdefault("LANGEXTRACT_API_KEY","")
os.environ.setdefault("HF_TOKEN","")

def chunk_code(code, chunk_size=2000):
    return [code[i:i+chunk_size] for i in range(0, len(code), chunk_size)]

file=open('./rag/LangEXT/1.txt','r').read()

file=chunk_code(file)
print(len(file))

# import sys
# sys.exit(0)



client = OpenAI(base_url='https://router.huggingface.co/v1', api_key=os.environ.get("HF_TOKEN"))

prompt1 = """
    You are an expert in summarization.
    
    ### CONTEXT:
    {text}
    
    
    ### TASK:
    Summarize the above text in 3 bullet points.
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

    Return valid JSON array.
    No variable names.

    Rules:
    - Attribute names must be meaningful and aligned with the task.
    - Attribute values must be concise (1–3 words).
    - Attribute values key must be same on all three examples.
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
            model='models/gemini-2.5-flash',
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

obj=param_ext(prompt)
res=obj.generate(text[0])
# print(res)

data=json.loads(res)

# print(data[0])
# print(type(data[0]))

t1=data[0]['attributes']
# t2=data[1]['extraction_text']
# t3=data[2]['extraction_text']

# print('-*-*'*20)
# print(t1)
# print(type(t1))
# print('-*-*'*20)
# print(t2)
# print('-*-*'*20)
# print(t3)


# import sys
# sys.exit(0)


class lang_ex:
    def __init__(self,prompt,data,examples,model="gemini-2.5-flash"):
        self.prompt=prompt
        self.data=data
        self.examples=examples
        self.model=model
        
    def extraction(self):
        res=lx.extract(
            text_or_documents=self.data,
            prompt_description=self.prompt,
            examples=self.examples,
            model_id=self.model
        )
        return res

class fxn:
    def __init__(self,code):
        self.code=code
    
    def validation(self):
        prompt=textwrap.dedent("""
        You are an expert in summarization.

        ### CONTEXT:
        {text}
        
        
        ### TASK:
        Summarize the above text in 3 bullet points.
                            """
        )
        
        # data=self.code
        # print(type(data[0]))

        examples=[
            lx.data.ExampleData(
                text=data[0]['text'],
                extractions=[
                    lx.data.Extraction(
                        extraction_class='summarization',
                        extraction_text=data[0]['extraction_text'],
                        attributes=data[0]['attributes']
                    )
                ] 
            ),lx.data.ExampleData(
                text=data[1]['text'],
                extractions=[
                    lx.data.Extraction(
                        extraction_class="summarization",
                        extraction_text=data[1]['extraction_text'],
                        attributes=data[1]['attributes']
                    )
                ]
            ),
            lx.data.ExampleData(
                text=data[2]['text'],
                extractions=[
                    lx.data.Extraction(
                        extraction_class="summarization",
                        extraction_text=data[2]['extraction_text'],
                        attributes=data[2]['attributes']
                    )
                ]
            ),
        ]
        
        res=lang_ex(prompt.format(text=file[0]),self.code,examples)
        return res.extraction()        
        
   

test1=fxn(file[4])
result=test1.validation()

print("-----"*20)
print("-----"*20)
print(file[4])
print("-----"*20)
print("-----"*20)
print(result.extractions[0].extraction_text)