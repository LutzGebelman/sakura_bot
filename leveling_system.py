from discord.member import User
import sqlite3
class LevelingSystem():
    def __init__(self) -> None:
        self.sqlcon = sqlite3.connect("lvltable.db")
        self.cursor = self.sqlcon.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS leveling(
                userid VARCHAR(255) PRIMARY KEY,
                userxp INT,
                userlvl INT
            );''')
        self.sqlcon.commit()

    def __del__(self):
        self.sqlcon.close()

    async def update_level(self, user: User):
        lvl_end = 0
        with self.sqlcon:
            ans = self._get_level(user)
            if ans == []:
                self.cursor.execute(
                f'''
                INSERT INTO leveling(userid, userxp, userlvl)
                VALUES(
                    '{user.id}',
                    0,
                    0
                );
                ''')
        data = self._get_level(user)

        if  data[0][1] % 20 == 0:
            await self.level_up(user)
            return True
        return False

    async def add_xp(self, user: User) -> None:
        data = self._get_level(user)
        self._put_data(user, data[0][1] + 1, data[0][2])

    async def level_up(self, user: User) -> None:
        data = self._get_level(user)
        self._put_data(user, data[0][1], data[0][2] + 1)
    
    async def level_down(self, user: User) -> None:
        data = self._get_level(user)
        self._put_data(user, data[0][1], data[0][2] - 1)

    def _get_level(self, user: User) -> int:
        self.cursor.execute(
        f'''
        SELECT * FROM leveling
        WHERE userid LIKE "{user.id}";
        ''')
        return self.cursor.fetchall()

    def _put_data(self, user: User, xp: int, lvl: int):
        self.cursor.execute(
            f'''
            UPDATE leveling
            SET userxp = {xp}, userlvl = {lvl}
            WHERE userid = {user.id};
            '''
        )