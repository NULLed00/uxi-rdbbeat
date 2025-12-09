# Copyright (c) 2023 Hewlett Packard Enterprise Development LP
# MIT License

import json
from typing import Any

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from rdbbeat.data_models import Schedule, ScheduledTask
from rdbbeat.db.models import CrontabSchedule, PeriodicTask
from rdbbeat.exceptions import PeriodicTaskNotFound


def get_crontab_schedule(session: Session, schedule: Schedule) -> CrontabSchedule:  # noqa: D103
    crontab = (
        session.query(CrontabSchedule)
        .where(
            and_(
                CrontabSchedule.minute == schedule.minute,
                CrontabSchedule.hour == schedule.hour,
                CrontabSchedule.day_of_week == schedule.day_of_week,
                CrontabSchedule.day_of_month == schedule.day_of_month,
                CrontabSchedule.month_of_year == schedule.month_of_year,
                CrontabSchedule.timezone == schedule.timezone,
            )
        )
        .one_or_none()
    )
    return crontab or CrontabSchedule(**schedule.dict())


def schedule_task(
    session: Session,
    scheduled_task: ScheduledTask,
    celery_options: dict = None,
    **kwargs: Any,  # noqa: ANN401
) -> PeriodicTask:
    """Schedule a task by adding a periodic task entry."""
    crontab = get_crontab_schedule(session=session, schedule=scheduled_task.schedule)
    task = PeriodicTask(
        crontab=crontab,
        name=scheduled_task.name,
        task=scheduled_task.task,
        kwargs=json.dumps(kwargs),
    )

    task.celery_options=celery_options
    session.add(task)

    return task


def update_task_enabled_status(
    session: Session,
    enabled_status: bool,  # noqa: FBT001
    periodic_task_id: int,
) -> PeriodicTask:
    """Update task enabled status (if task is enabled or disabled)."""
    try:
        task = session.query(PeriodicTask).filter(PeriodicTask.id == periodic_task_id).one()
        task.enabled = enabled_status  # type: ignore [assignment]
        session.add(task)

    except NoResultFound as e:
        raise PeriodicTaskNotFound() from e  # noqa: RSE102

    return task


def update_task(
    session: Session,
    periodic_task_id: int,
    scheduled_task: ScheduledTask = None,
    celery_options: dict = {}
) -> PeriodicTask:
    """Update the details of a task including the crontab schedule"""  # noqa: D415
    try:
        task = session.query(PeriodicTask).filter(PeriodicTask.id == periodic_task_id).one()

        if scheduled_task:
            task.crontab = get_crontab_schedule(session, scheduled_task.schedule)
            task.name = scheduled_task.name  # type: ignore [assignment]
            task.task = scheduled_task.task  # type: ignore [assignment]

        if celery_options:
            task.update_celery_options(celery_options)

        session.add(task)

    except NoResultFound as e:
        raise PeriodicTaskNotFound() from e  # noqa: RSE102

    return task


def is_crontab_used(session: Session, crontab_schedule: CrontabSchedule) -> bool:  # noqa: D103
    schedules = session.query(PeriodicTask).filter_by(crontab=crontab_schedule).all()
    return True if schedules else False  # noqa: SIM210


def delete_task(session: Session, periodic_task_id: int) -> PeriodicTask:  # noqa: D103
    try:
        task = session.query(PeriodicTask).where(PeriodicTask.id == periodic_task_id).one()
        session.delete(task)
        session.flush()
        if not is_crontab_used(session, task.crontab):
            session.delete(task.crontab)
        return task  # noqa: TRY300
    except NoResultFound as e:
        raise PeriodicTaskNotFound() from e  # noqa: RSE102
