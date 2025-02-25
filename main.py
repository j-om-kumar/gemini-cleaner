from fastapi import FastAPI, HTTPException
import google.generativeai as genai
from pydantic import BaseModel

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key="AIzaSyCZlCdqIUm1261juSIsoq1vS0TPAFSRhkE")

# Define model configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.6,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="""
        Clean and Enhance the code without changing logic. 
        Improve it by handling exceptions, optimizing performance, and making it more robust. 
        Maintain formatting and comments.

        Respond ONLY with the cleaned code, no explanations and nothing must be in the output only the code.
    """,
)

class Payload(BaseModel):
    code: str
    

@app.post("/clean_code/")
async def clean_code_generator(payload: Payload):
    code = payload.code
    print(code)
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(f"clean this code {code}")
        result = response.text
        cleaned_code = result[14:-4]  # Extract the cleaned code
        
        return {"cleaned_code": cleaned_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
