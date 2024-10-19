from uuid import UUID

from fastapi import HTTPException, WebSocket
from app.services.sessions.init import backend

# Ваш бэкенд сессий
async def ws_cookie(websocket: WebSocket):
    # Получите куки из заголовков WebSocket
    cookie_header = websocket.headers.get("cookie")
    # Обработайте куки и верните необходимые данные
    # Например, вы можете использовать библиотеку для парсинга куки
    return parse_cookies(cookie_header)


async def verify_session(websocket: WebSocket):
    cookie_header = websocket.headers.get("cookie")
    if cookie_header:
        session_id = extract_session_id(cookie_header)
        session_data = await backend.read(session_id)
        if not session_data:
            raise HTTPException(status_code=403, detail="Invalid session")
        return session_data
    raise HTTPException(status_code=403, detail="No session found")


def extract_session_id(cookie_header: str):
    # Реализуйте логику для извлечения session_id из cookie_header
    cookies = parse_cookies(cookie_header)
    return cookies.get("session_id")


def parse_cookies(cookie_header: str):
    # Ваша логика для парсинга куки
    cookies = {}
    if cookie_header:
        for cookie in cookie_header.split(";"):
            key, value = cookie.strip().split("=", 1)
            cookies[key] = value
    return cookies
