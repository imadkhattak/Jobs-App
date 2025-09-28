# src/LLM.py

import os
from groq import Groq
from dotenv import load_dotenv
from CV_Parser import extract_text
from langchain.prompts import PromptTemplate


load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_cv_info():

    cv_content = extract_text("../CVs/imad ud din khattak.pdf")

    template = """Here is the CV content: {cv_content}"""

    prompt = PromptTemplate(
        input_variables=["cv_content"],
        template=template,
    )

    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an AI assistant that extracts structured information from CVs.\
                              Return the output strictly as a JSON object with keys: role, skills, years_of_experience.\
                              also include what type of projects the person has worked on. """

            },
            {
                "role": "user",
                "content": prompt.format(cv_content=cv_content)
            }
        ],

        temperature=0.3,
        response_format={"type": "json_object"},

    )

    extracted_cv_content = chat_completion.choices[0].message.content
    return extracted_cv_content

if __name__ == "__main__":
    info = extract_cv_info()
    print(info)

