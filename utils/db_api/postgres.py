import datetime
from typing import Union

import asyncpg
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password=config.PGPASSWORD,
            host=config.ip,
            database=config.DATABASE)
        self.pool = pool

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT NOT NULL PRIMARY KEY,
            completed_site_id INTEGER ARRAY DEFAULT ARRAY[]::integer[],
            completed_tiktok_id INTEGER ARRAY DEFAULT ARRAY[]::integer[],
            earnings INTEGER DEFAULT 0,
            registration_date DATE NOT NULL,
            attracted_users INTEGER DEFAULT 0,
            invited boolean DEFAULT FALSE
            );"""
        await self.pool.execute(sql)

    async def create_table_sites(self):
        sql = """
        CREATE TABLE IF NOT EXISTS sites (
            task_id SERIAL PRIMARY KEY,
            url VARCHAR(350),
            short_url VARCHAR(120),
            status BOOL NOT NULL,
            reward INTEGER DEFAULT 10,
            date DATE
            );"""
        await self.pool.execute(sql)

    async def create_table_tik_toks(self):
        sql = """
        CREATE TABLE IF NOT EXISTS tiktoks (
            task_id SERIAL PRIMARY KEY,
            url VARCHAR(350),
            short_url VARCHAR(120),
            status BOOL NOT NULL,
            reward INTEGER DEFAULT 10,
            date DATE
            );"""
        await self.pool.execute(sql)

    async def add_task_sites(self, url):
        date = datetime.date.today()
        sql = """
        INSERT INTO sites(url, status, date) VALUES($1, $2, $3)
        """
        await self.pool.execute(sql, url, True, date)

    async def add_task_tiktok(self, url):
        date = datetime.date.today()
        sql = """
        INSERT INTO tiktoks(url, status, date) VALUES($1, $2, $3)
        """
        await self.pool.execute(sql, url, True, date)

    async def get_active_sites(self):
        sql = """
        SELECT (task_id, short_url, reward) FROM sites WHERE status = TRUE
        """
        return await self.pool.fetch(sql)

    async def get_task_sites(self, task_id):
        sql = """
        SELECT (task_id, short_url, reward) FROM sites WHERE task_id = $1
        """
        return await self.pool.fetch(sql, task_id)

    async def get_active_tiktoks(self):
        sql = """
        SELECT (task_id, short_url, reward) FROM tiktoks WHERE status = TRUE
        """
        return await self.pool.fetch(sql)

    async def get_task_tiktok(self, task_id):
        sql = """
        SELECT (task_id, short_url, reward) FROM tiktoks WHERE task_id = $1
        """
        return await self.pool.fetch(sql, task_id)

    # user_work
    async def add_user(self, id: int, status: bool):
        date = datetime.date.today()
        sql = """
        INSERT INTO users(user_id, invited, registration_date) VALUES($1, $2, $3)
        """
        await self.pool.execute(sql, id, status, date)

    async def check_user(self, id: int):
        sql = f"""
        select count(*) from users where user_id=$1;
        """
        return await self.pool.fetch(sql, id)

    async def check_user_for_referal(self, id: int):
        sql = f"""
        select count(*) from users where user_id=$1 AND invited=FALSE;
        """
        return await self.pool.fetch(sql, id)

    async def get_user_info(self, user_id):
        sql = f"""
        SELECT * FROM users WHERE user_id=$1;
        """
        return await self.pool.fetch(sql, user_id)

    async def set_invited_true(self, user_id: int):
        sql = """UPDATE users SET invited=TRUE WHERE user_id=$1;"""
        return await self.pool.execute(sql, user_id)

    async def add_earnings_for_referrals(self, user_id: int, amount: int):
        sql = """UPDATE users SET earnings=earnings+$1, attracted_users=attracted_users+1 WHERE user_id=$2;"""
        return await self.pool.execute(sql, amount, user_id)

    async def add_earnings(self, user_id: int, amount: int):
        sql = """UPDATE users SET earnings=earnings+$1 WHERE user_id=$2;"""
        return await self.pool.execute(sql, amount, user_id)
