from pydantic import BaseModel

from scherkhan.models.device import Device


class Car(BaseModel):
    id: int
    name: str
    owner: dict
    share_id: int
    registration_id: str
    registration_certificate_id: str
    vin: str
    is_vin_editable: bool
    photo: str = None
    fuel_type: str
    fuel_tank_capacity: int
    fuel_percent_a: int
    fuel_percent_b: int
    body_style: int
    body_color: int
    role: int
    access_share: bool
    access_state: bool
    access_report: bool
    access_command: bool
    access_history: bool
    access_settings: bool
    access_firmware: bool
    access_location: bool
    access_notification: bool
    device: Device

    def __repr__(self):
        return f"{self.name} - {self.registration_id}"
