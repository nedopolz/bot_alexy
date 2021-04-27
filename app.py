from loader import db

async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)

    #from utils.notify_admins import on_startup_notify
    #await on_startup_notify(dp)
    await db.create()
    await db.create_table_users()
    await db.create_table_sites()
    await db.create_table_tik_toks()

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
