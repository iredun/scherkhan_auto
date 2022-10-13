import json
from typing import Callable

import websocket
import logging

from scherkhan.models.websocket import parse_json_message


class WebSocketClient:
    __url = "wss://ws.mf-t.ru/state/"
    __user_token = None

    def __init__(
        self,
        user_token: str,
        on_message: Callable,
        on_error: Callable,
        on_close: Callable,
    ):
        """
        :param user_token: Токен пользователя
        :param on_message: Обработчик сообщений
        :param on_error: Обработчик ошибок
        :param on_close: Обработчик закрытия соединения
        """

        self.__user_token = user_token
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close
        self.ws = websocket.WebSocketApp(
            self.__url,
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_close=self.__on_close,
        )
        self.ws.on_open = self.__on_open

    def __on_open(self, ws: websocket.WebSocketApp):
        logging.info("WebSocket connection opened")
        logging.info("WebSocket send auth message")
        auth_message = {"type": "auth", "data": self.__user_token}
        self.ws.send(json.dumps(auth_message))

    def __on_message(self, ws, message: str):
        logging.info(f"WebSocket message received: {message}")
        message_model = parse_json_message(message)
        self.on_message(ws, message_model)

    def __on_error(self, ws: websocket.WebSocketApp, error):
        logging.error(f"WebSocket error: {error}")
        self.on_error(ws, error)

    def __on_close(self, ws: websocket.WebSocketApp, close_status_code, close_msg):
        logging.info(f"WebSocket connection closed: {close_status_code} {close_msg}")
        self.on_close(ws, close_status_code, close_msg)
