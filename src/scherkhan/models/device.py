from datetime import datetime

from pydantic import BaseModel


class Device(BaseModel):
    serial: str
    model: int
    type: int
    created: datetime
    is_autostart_available: bool
    pin: str
    pin: str
    msisdn: str
    operator: int
    currency: str
    tehsupport: str
    emergency: str
    is_mark_available: bool
    has_internet_connection: bool
    branding_id: int = None
