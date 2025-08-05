from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow all origins (for dev; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-description/")
def generate_description(product_name: str = Form(...), category: str = Form(...)):
    prompt = f"Write a compelling eCommerce product description for '{product_name}' in the '{category}' category."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        description = response.choices[0].message["content"].strip()
        return {"success": True, "description": description}
    except Exception as e:
        return {"success": False, "error": str(e)}
