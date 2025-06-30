import os
import dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from huggingface_hub import InferenceClient

dotenv.load_dotenv()

app = FastAPI(
    title="BrainstormityBrain API",
    description="Agentic AI system for brainstorming and reasoning",
    version="1.0.0"
)

huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")

if not huggingface_api_key:
    raise ValueError("HUGGINGFACE_API_KEY environment variable is required")

client = InferenceClient(
    provider="novita",
    api_key=huggingface_api_key,
)

class BrainstormRequest(BaseModel):
    query: str

class BrainstormResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"message": "BrainstormityBrain API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/brainstorm", response_model=BrainstormResponse)
async def brainstorm(request: BrainstormRequest):
    try:
        response = client.chat.completions.create(
            model='deepseek-ai/DeepSeek-R1-0528-Qwen3-8B',
            messages=[
                {
                    "role": "user",
                    "content": request.query
                }
            ]
        )
        
        return BrainstormResponse(
            response=response.choices[0].message.content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing brainstorm request: {str(e)}")

@app.post("/test")
async def test_reasoning():
    try:
        response = client.chat.completions.create(
            model='deepseek-ai/DeepSeek-R1-0528-Qwen3-8B',
            messages=[
                {
                    "role": "user",
                    "content": "Are you a reasoning model?"
                }
            ]
        )
        
        return {
            "question": "Are you a reasoning model?",
            "response": response.choices[0].message.content,
            "model": 'deepseek-ai/DeepSeek-R1-0528-Qwen3-8B'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in test endpoint: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


