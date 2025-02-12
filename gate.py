from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn
from google import genai


GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Класс для работы с моделью
class Gemini:
    def __init__(self, api_key, fake: bool = False):
        self.fake = fake
        if not fake:
            self.client = genai.Client(api_key=api_key)
            self.chat = self.client.aio.chats.create(model="gemini-2.0-flash")
    
    def reset(self):
        if not self.fake:
            self.chat = self.client.aio.chats.create(model="gemini-2.0-flash")
    
    async def get_gemini_response(self, prompt: str):
        if self.fake:
            return "I don't think so..."
        else:
            response = await self.chat.send_message(prompt)
            return response.text


gemini = Gemini(GEMINI_API_KEY, fake=True)
app = FastAPI()

# Определяем модель входящих данных
class RequestModel(BaseModel):
    role: str
    request: str
    new: bool

class ResponseModel(BaseModel):
    response: str

@app.post("/request-llm", response_model=ResponseModel)
async def request_llm(request_json: RequestModel) -> ResponseModel:
    if request_json.new:
        gemini.reset()
    
    # запрашиваем модель
    response = await gemini.get_gemini_response(request_json.request)
    return ResponseModel(response=response)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)
