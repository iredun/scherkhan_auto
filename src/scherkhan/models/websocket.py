import json
from datetime import datetime

from pydantic import BaseModel

from scherkhan.models.enums import WebsocketMessageType


class BaseMessage(BaseModel):
    """Base message model."""

    type: WebsocketMessageType
    car_id: int
    data: dict


class CmdMessageData(BaseModel):
    """Cmd message data model."""

    cmd: str
    hash: int
    data: dict = None
    state: str


class CmdMessage(BaseMessage):
    """Cmd message model."""

    type: WebsocketMessageType = WebsocketMessageType.cmd
    data: CmdMessageData


class RouteMessageData(BaseModel):
    """Route message data model."""

    type: int
    dt_start: datetime
    distance: int
    points: str
    coord_src: int
    is_abs: bool


class RouteMessage(BaseMessage):
    """Route message model."""

    type: WebsocketMessageType = WebsocketMessageType.route
    data: RouteMessageData


class BatteryVoltage(BaseModel):
    """Battery voltage model."""

    value: float
    percent: int


class EngineReason(BaseModel):
    """Engine reason model."""

    id: int
    value: str


class Engine(BaseModel):
    """Engine model."""

    state_id: int
    remote_start_time: datetime = None
    rpm: int = None
    temperature: int
    is_running: bool
    reason: dict


class StateMessageData(BaseModel):
    """State message data model."""

    cabin_temperature: int = None
    coolant_temperature: int = None
    battery_voltage: BatteryVoltage
    speed: int = None
    odometer: int
    fuel: str = None
    gsm_rssi: int
    lat: float
    lng: float
    coord_src: int
    course: str = None
    is_online: bool
    data_lag: int
    last_connected: datetime
    msg: str = None
    satellites_number: int = None
    is_in_evacuation: bool = None
    is_mark_near: bool = None
    is_mark_immobilizer: bool = None
    is_in_route: bool
    is_ignition_on: bool
    is_pre_heater_on: bool
    is_lights_on: bool
    is_l_turn_signal: bool
    is_r_turn_signal: bool
    is_trunk_open: bool
    is_hood_open: bool
    is_driver_door_closed: bool
    is_brake_pressed: bool
    is_fl_door_open: bool
    is_fr_door_open: bool
    is_rl_door_open: bool
    is_rr_door_open: bool
    is_locked: bool
    state: str
    sim_balance: float
    sim_balance_updated: datetime
    sim_currency: str
    is_settings_synchronized: bool
    fines: int
    engine: Engine


class StateMessage(BaseMessage):
    """State message model."""

    type: WebsocketMessageType = WebsocketMessageType.state
    data: StateMessageData


def parse_json_message(json_data: str):
    """Parse message."""
    message = json.loads(json_data)
    if message["type"] == WebsocketMessageType.state.value:
        return StateMessage(**message)
    elif message["type"] == WebsocketMessageType.route.value:
        return RouteMessage(**message)
    elif message["type"] == WebsocketMessageType.route.value:
        return RouteMessage(**message)
