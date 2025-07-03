import os
import dotenv
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from huggingface_hub import InferenceClient
import secrets
import hashlib

dotenv.load_dotenv()

app = FastAPI(
    title="BrainstormityBrain API",
    description="Agentic AI system for brainstorming and reasoning",
    version="1.0.0"
)

# Security setup
security = HTTPBearer()

# API Keys - In production, store these in a database
VALID_API_KEYS = {
    # API key for your frontend team
    "bst_prod_eI6Nwd4-6uVOG2VcSk81EBCrjHMYeMB3": "frontend_client",
    # Add more API keys as needed
}

# Initialize client as None initially
client = None

def initialize_client():
    global client
    huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
    
    if not huggingface_api_key:
        print("Warning: HUGGINGFACE_API_KEY environment variable is not set")
        return False
    
    try:
        client = InferenceClient(
            provider="novita",
            api_key=huggingface_api_key,
        )
        return True
    except Exception as e:
        print(f"Error initializing client: {e}")
        return False

# Try to initialize client on startup
client_initialized = initialize_client()

# Authentication dependency
async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    api_key = credentials.credentials
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return VALID_API_KEYS[api_key]

class BrainstormRequest(BaseModel):
    query: str

class BrainstormResponse(BaseModel):
    response: str

# Public endpoints (no API key required)
@app.get("/")
async def root():
    return {"message": "BrainstormityBrain API is running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "client_initialized": client_initialized,
        "huggingface_api_key_present": bool(os.getenv("HUGGINGFACE_API_KEY"))
    }

# Protected endpoints (API key required)
@app.post("/brainstorm", response_model=BrainstormResponse)
async def brainstorm(request: BrainstormRequest, client_name: str = Depends(verify_api_key)):
    if not client_initialized or client is None:
        raise HTTPException(status_code=503, detail="Service not properly configured. Missing HUGGINGFACE_API_KEY.")
    
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
async def test_reasoning(client_name: str = Depends(verify_api_key)):
    if not client_initialized or client is None:
        raise HTTPException(status_code=503, detail="Service not properly configured. Missing HUGGINGFACE_API_KEY.")
    
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

# Endpoint to generate new API keys (protect this in production!)
@app.post("/admin/generate-api-key")
async def generate_api_key(client_name: str, admin_key: str = Header(...)):
    # In production, use a secure admin key
    if admin_key != os.getenv("ADMIN_API_KEY", "admin_secret_change_me"):
        raise HTTPException(status_code=403, detail="Forbidden")
    
    new_key = "bst_prod_" + secrets.token_urlsafe(32)
    VALID_API_KEYS[new_key] = client_name
    return {"api_key": new_key, "client_name": client_name}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
