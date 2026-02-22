from fastapi import FastAPI, Depends, HTTPException, Header
import ollama
import os
from dotenv import load_dotenv
from fastapi.responses import FileResponse


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
load_dotenv()

API_KEY_CREDITS = {os.getenv("API_KEY"): 5}
print(API_KEY_CREDITS)
app = FastAPI()

def verify_api_key(x_api_key: str = Header(None)):
    credits = API_KEY_CREDITS.get(x_api_key, 0)
    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API Key, or no credits")

    return x_api_key

@app.post("/generate")
def generate(prompt: str, x_api_key: str = Depends(verify_api_key)):
    API_KEY_CREDITS[x_api_key] -= 1
    response = ollama.chat(model="starcoder2:3b", messages=[{"role": "user", "content": prompt}])
    return {"response": response["message"]["content"]}


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Endpoint para baixar arquivos da pasta uploads"""
    filename.replace("%", " ")
    print("Download filename: ", filename)

    file_path = os.path.join(UPLOAD_DIR, filename)

    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
    return {"error": "Arquivo não encontrado"}

# if __name__ == "__main__":
#     import uvicorn

#     port = int(os.getenv("SERVER_PORT", 3000))
#     host = os.getenv("SERVER_HOST", "0.0.0.0")

#     uvicorn.run(app, host=host, port=port)