from pydantic import BaseModel, Field, ValidationError
from typing import Literal, List
import time

class Passenger(BaseModel):
    passengerId: str = Field(..., min_length=1, max_length=5)
    name: str = Field(..., min_length=1, max_length=20)
    age: int = Field(..., ge=0)
    gender: Literal["Male","Female","Others"] = Field(...)
    classType: str = Field(..., min_length=1, max_length=30)
    coachNumber: str | None = Field(default=None, min_length=1, max_length=5)
    seatNumber: int | None = Field(default=None, ge=1, le=100)

class Reservation(BaseModel):

    reservationDate: str = Field(default_factory = (lambda : time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())))
    travelDate: str = Field(...)
    sourceStation: str = Field(..., min_length=1, max_length=30)
    destinationStation: str = Field(..., min_length=1, max_length=30)
    paymentMethod: str = Field(..., min_length=1, max_length=20)
    totalFare: float = Field(..., ge=0)
    status: Literal["NotConfirmed","Confirmed"] | None = Field(...)
    trainId: str = Field(..., min_length=1, max_length=10)
    passengers: List[Passenger] = Field(...)
