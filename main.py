from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()

# Создаем объект для рендеринга шаблонов
templates = Jinja2Templates(directory="templates")

# Храним сообщения в памяти
messages = []
counter = 1

# Отправка сообщений через WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            global counter
            message = {"id": counter, "content": message_data['content']}
            counter += 1
            messages.append(message)
            await websocket.send_text(json.dumps(messages))  # Отправка всех сообщений обратно
    except WebSocketDisconnect:
        pass

# Отправка HTML страницы
@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
