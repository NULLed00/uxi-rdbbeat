# Copyright (c) 2023 Hewlett Packard Enterprise Development LP
# MIT License

from pydantic import BaseModel, validator


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
    def validate(v, _min, _max, error_message, _type):
        if v == "*":
            return v

        elif v.startswith('*/'):
            Schedule.check_data_range(v.strip('*/'), _min, _max, error_message)

        elif not v.isdigit():
            raise ValueError(f"{_type}: '{v}' is not a valid int")  # noqa: EM102, TRY003

        else:
            Schedule.check_data_range(v, _min, _max, error_message)

        return v

    @validator("minute")
    def minute_validation(cls, v: str) -> str:  # noqa: D102, N805
        return cls.validate(v, 0, 60, "Minute value must range between 0 and 59", "Minute")

    @validator("hour")
    def hour_validation(cls, v: str) -> str:  # noqa: D102, N805
        return cls.validate(v, 0, 24, "Hour value must range between 0 and 23", "Hour")


    @validator("day_of_week")
    def day_of_week_validation(cls, v: str) -> str:  # noqa: D102, N805
        return cls.validate(v, 0, 7, "Day of the week value must range between 0 and 6", "Day of week")


    @validator("day_of_month")
    def day_of_month_validation(cls, v: str) -> str:  # noqa: D102, N805
        return cls.validate(v, 0, 32, "Day of the month value must range between 1 and 31", "Day of the month")

    @validator("month_of_year")
    def month_of_year_validation(cls, v: str) -> str:  # noqa: D102, N805
        return cls.validate(v, 0, 13, "Month of year value must range between 0 and 12", "Month of the year")


class ScheduledTask(BaseModel):
    name: str
    task: str
    schedule: Schedule
