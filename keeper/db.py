from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        attributes = self.__table__.columns.keys()
        return f"{self.__class__.__name__}(" + ", ".join((f"{key}={getattr(self, key)!r}" for key in attributes)) + ")"


class Employee(Base):
    __tablename__ = "employee"
    id: Mapped[int] = mapped_column(primary_key=True)  # Discord ID
    server_id: Mapped[int] = mapped_column(ForeignKey("server.id"), primary_key=True)
    server: Mapped["Server"] = relationship(back_populates="users")
    timelog: Mapped[List["TimeLog"]] = relationship(back_populates="employee")
    cautions: Mapped[List["Caution"]] = relationship(back_populates="employee")
    issued_cautions: Mapped[List["Caution"]] = relationship(back_populates="issuer")
    clock_start: Mapped[int] = mapped_column(nullable=True)  # if None, user isn't clocked in
    # Settings
    auto_clock_out: Mapped[bool] = mapped_column(default=True)  # only works if Server.auto_clock_out == 1


class Server(Base):
    __tablename__ = "server"
    id: Mapped[int] = mapped_column(primary_key=True)  # Discord ID
    users: Mapped[List["Employee"]] = relationship(back_populates="server")
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
    end: Mapped[int]


class Caution(Base):
    __tablename__ = "caution"
    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    employee: Mapped["Employee"] = relationship(back_populates="cautions")
    issuer_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    issuer: Mapped["Employee"] = relationship(back_populates="issued_cautions")
    reason: Mapped[str] = mapped_column(String(512), default="")
    issued_at: Mapped[int]
    duration: Mapped[int]


class DatabaseDriver:
    def __init__(self):
        # connect to database
        self.engine = create_engine("sqlite:///database.db")  # TODO: Switch to PostgreSQL
        Base.metadata.create_all(self.engine)

    def session(self) -> Session:
        return Session(self.engine)


database = DatabaseDriver()
