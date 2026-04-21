# Copyright (c) 2023 Hewlett Packard Enterprise Development LP
# MIT License

from pydantic import BaseModel, field_validator
from celery.schedules import crontab_parser, ParseException


class Schedule(BaseModel):
    minute: str = "*"
    hour: str = "*"
    day_of_week: str = "*"
    day_of_month: str = "*"
    month_of_year: str = "*"
    timezone: str = "UTC"

    @staticmethod
    def check_data_range(v, _min, _max, error_message):
        assert int(v) >= _min and int(v) < _max, error_message  # noqa: PLR2004, PT018, S101

    @staticmethod
    def validate(value, _min, _max, error_message, _type):

        try:

            crontab_parser(_max, _min).parse(value)
            return value

        except (ValueError, ParseException) as error:
            raise ValueError(error_message) from error


    @field_validator("minute")
    def minute_validation(cls, v: str) -> str:  # noqa: D102, N805
        return cls.validate(v, 0, 60, "Minute value must range between 0 and 59", "Minute")


    @field_validator("hour")
    def hour_validation(cls, v: str) -> str:  # noqa: D102, N805
        return cls.validate(v, 0, 24, "Hour value must range between 0 and 23", "Hour")


    @field_validator("day_of_week")
    def day_of_week_validation(cls, v: str) -> str:  # noqa: D102, N805
        return cls.validate(v, 0, 7, "Day of the week value must range between 0 and 6", "Day of week")


    @field_validator("day_of_month")
    def day_of_month_validation(cls, v: str) -> str:  # noqa: D102, N805
        return cls.validate(v, 0, 32, "Day of the month value must range between 1 and 31", "Day of the month")

    @field_validator("month_of_year")
    def month_of_year_validation(cls, v: str) -> str:  # noqa: D102, N805
        return cls.validate(v, 0, 13, "Month of year value must range between 0 and 12", "Month of the year")


class ScheduledTask(BaseModel):
    name: str
    task: str
    schedule: Schedule
