from typing import Callable

import requests
import logging
import os

from requests import HTTPError

from scherkhan import WebSocketClient
from scherkhan.models.car import Car
from scherkhan.models.enums import CarCommand
from scherkhan.models.user import User
from scherkhan.models.websocket import CmdMessageData

logging.basicConfig(level=logging.INFO)


class ApiClient:
    __token_file_path = "token.dat"
    __user_token = None

    __session = requests.Session()

    __api_url = "https://api.mf-t.ru/v3/"
    __auth_api_url = "https://auth.mf-t.ru/v1/"

    user: User = None

    def __init__(self, email: str, password: str, token_file_path: str = None):
        if token_file_path:
            self.__token_file_path = token_file_path

        self.__session.headers.update(
            {
                "origin": "https://mf-t.ru",
                "referer": "https://mf-t.ru/",
            }
        )

        self.__email = email
        self.__password = password
        try:
            self.__restore_token()
            self.__auth()
            self.__get_user()
        except HTTPError as e:
            logging.error(f"Auth error: {e}")
            self.__delete_token()
            raise e

    def __store_token(self):
        with open(self.__token_file_path, "w") as f:
            f.write(self.__user_token)
            self.__session.headers.update(
                {"Authorization": f"Token {self.__user_token}"}
            )

    def __restore_token(self):
        if os.path.exists(self.__token_file_path):
            with open(self.__token_file_path, "r") as f:
                self.__user_token = f.read()
                self.__session.headers.update(
                    {"Authorization": f"Token {self.__user_token}"}
                )

    def __delete_token(self):
        if os.path.exists(self.__token_file_path):
            os.remove(self.__token_file_path)
            self.__session.headers.pop("Authorization")

    def __auth(self):
        if self.__user_token:
            logging.info("Auth with token")
            return

        logging.info("Authenticating...")
        response = self.__session.post(
            f"{self.__auth_api_url}login/",
            json={
                "email": self.__email,
                "password": self.__password,
            },
        )
        response.raise_for_status()
        self.__user_token = response.json()["key"]
        logging.info("User token received")

        self.__store_token()
        logging.info("Authenticating success")

    def __get_user(self):
        logging.info("Getting user info...")
        response = self.__session.get(f"{self.__auth_api_url}user/")
        response.raise_for_status()
        self.user = User(**response.json())
        logging.info(f"User info received {self.user}")

    def get_cars(self):
        logging.info("Getting cars...")
        response = self.__session.get(f"{self.__api_url}cars/")
        response.raise_for_status()
        data = response.json()
        car_list = [Car(**car) for car in data]
        logging.info(f"Cars received {car_list}")
        return car_list

    def send_car_command(self, car: Car, command: CarCommand) -> CmdMessageData:
        logging.info(f"Sending command {command} to car {car}")
        response = self.__session.post(
            f"{self.__api_url}cars/{car.id}/command/",
            json={
                "car_id": car.id,
                "cmd": command.name,
            },
        )
        response.raise_for_status()
        logging.info(f"Command {command} to car {car} sent")
        return CmdMessageData(**response.json())

    def get_state_websocket(
        self, on_message: Callable, on_error: Callable, on_close: Callable
    ):
        return WebSocketClient(self.__user_token, on_message, on_error, on_close)
