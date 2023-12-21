from typing import List
from sqlalchemy import ForeignKey, create_engine, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        attributes = self.__table__.columns.keys()
        return f"{self.__class__.__name__}(" + ", ".join((f"{key}={getattr(self, key)!r}" for key in attributes)) + ")"


class Employee(Base):
    __tablename__ = "employee"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    guild_id: Mapped[int] = mapped_column(ForeignKey("guild.id"))
    guild: Mapped["Guild"] = relationship(back_populates="users")
    added: Mapped[datetime] = mapped_column(default=func.now())  # TODO: DateTime
    timelog: Mapped[List["TimeLog"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    warnings: Mapped[List["Warning"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    clock_start: Mapped[int] = mapped_column(nullable=True)  # if None, user isn't clocked in
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"), nullable=True)
    job: Mapped["Job"] = relationship(back_populates="employees")
    # Settings
    auto_clock_out: Mapped[bool] = mapped_column(default=True)  # only works if Server.auto_clock_out == 1


class Guild(Base):
    __tablename__ = "guild"
    id: Mapped[int] = mapped_column(primary_key=True)  # Discord Guild ID
    users: Mapped[List["Employee"]] = relationship(back_populates="guild", cascade="all, delete-orphan")
    # Settings
    language: Mapped[str] = mapped_column(String(2), default="en")  # de/en. Not going to support that many languages
    manager_role: Mapped[int] = mapped_column(nullable=True)  # if None, only admins can use the bot
    clocked_in_role: Mapped[int] = mapped_column(nullable=True)
    log_channel: Mapped[int] = mapped_column(nullable=True)  # no channel, no logs
    default_warn_period: Mapped[int] = mapped_column(default=604800)  # one week default, in seconds
    auto_clock_out: Mapped[int] = mapped_column(default=1)  # 0=disabled; 1=enabled; 2=force enabled
    auto_warn_auto_clock_out: Mapped[bool] = mapped_column(default=False)  # only works if auto_clock_out == 2
    default_clock_out_period: Mapped[int] = mapped_column(default=1800)  # 30 minutes
    inactive_notice_period: Mapped[int] = mapped_column(default=604800 * 2)  # internal warning for inactive users


class TimeLog(Base):
    __tablename__ = "timelog"
    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    employee: Mapped["Employee"] = relationship(back_populates="timelog")
    start: Mapped[int]
    end: Mapped[int] = mapped_column(nullable=True)


class Warning(Base):
    __tablename__ = "warning"
    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    employee: Mapped["Employee"] = relationship(back_populates="warnings")
    issuer: Mapped[int]  # just a Discord ID (I actually don't need a link to an employee here)
    reason: Mapped[str] = mapped_column(String(512), default="")
    issued_at: Mapped[int]
    duration: Mapped[int]


class Job(Base):
    __tablename__ = "job"
    id: Mapped[int] = mapped_column(primary_key=True)
    


class DatabaseDriver:
    def __init__(self):
        # connect to database
        self.engine = create_engine("sqlite:///database.db")  # TODO: Switch to PostgreSQL
        Base.metadata.create_all(self.engine)

    def session(self) -> Session:
        return Session(self.engine)


database = DatabaseDriver()
