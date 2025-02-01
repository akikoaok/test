from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()

# Шаблоны HTML
templates = Jinja2Templates(directory="templates")

# Отправка HTML страницы
@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Обработчик WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    messages = []  # Локальный список сообщений для каждого клиента
    counter = 1    # Локальный счетчик для каждого клиента
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message = {"id": counter, "content": message_data["content"]}
            counter += 1
            messages.append(message)
            await websocket.send_text(json.dumps(messages))  # Отправляем клиенту только его историю
    except WebSocketDisconnect:
        pass

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
