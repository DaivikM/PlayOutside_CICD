from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Literal

# Input schema
class WeatherInput(BaseModel):
    Outlook: Annotated[
        Literal["Sunny", "Overcast", "Rain"],
        Field(description="Weather outlook", examples=["Sunny"])
    ]
    Temperature: Annotated[
        Literal["Hot", "Mild", "Cool"],
        Field(description="Temperature level", examples=["Mild"])
    ]
    Humidity: Annotated[
        Literal["High", "Normal"],
        Field(description="Humidity level", examples=["Normal"])
    ]
    Windy: Annotated[
        Literal["Weak", "Strong"],
        Field(description="Windy condition", examples=["Weak"])
    ]

    @model_validator(mode="before")
    @classmethod
    def normalize_case(cls, data: dict):
        """Convert all string inputs to Capitalized form to match Literal values."""
        if isinstance(data, dict):
            return {k: v.capitalize() if isinstance(v, str) else v for k, v in data.items()}
        return data

    class Config:
        schema_extra = {
            "example": {
                "Outlook": "sunny",
                "Temperature": "cool",
                "Humidity": "normal",
                "Windy": "weak"
            }
        }