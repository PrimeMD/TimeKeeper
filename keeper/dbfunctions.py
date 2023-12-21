from keeper.db import *
from typing import Union, List
from sqlalchemy import select


class DBFunctions:
    def __init__(self):
        self.session = database.session()

    def __del__(self):
        self.session.close()

    def get_employee(self, user_id: Union[int, List[int]], guild_id: int):
        stmt = select(Employee).where(Employee.guild_id.is_(guild_id))
        if type(user_id) is list:
            stmt = stmt.where(Employee.user_id.in_(user_id))
            return self.session.scalars(stmt)
        else:
            stmt = stmt.where(Employee.user_id.is_(user_id))
            return self.session.scalar(stmt)

    def get_guild(self, guild_id: int):
        stmt = select(Guild).where(Guild.id.is_(guild_id))
        guild = self.session.scalar(stmt)
        if not guild:
            return self.add_guild(guild_id)

    def add_guild(self, guild_id: int):
        guild = Guild(id=guild_id)
        self.session.add(guild)
        self.session.commit()
        return guild

    def add_employee(self, user_id: int, guild_id: int):
        employee = Employee(user_id=user_id, guild=self.get_guild(guild_id))
        self.session.add(employee)
        self.session.commit()


dbfunctions = DBFunctions()
