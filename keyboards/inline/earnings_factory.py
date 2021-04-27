from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.mesages_config import INVITE_BUTTON, SITE_BUTTON, TIKTOK_BUTTON, NO_TASKS
from loader import db


async def inline_link_factory(user_id):
    db_data_sites = await db.get_active_sites()
    db_data_tiktok = await db.get_active_tiktoks()
    user_info = await db.get_user_info(user_id)
    id_list_sites = []
    id_list_tiktoks = []

    for i in db_data_sites:
        temp = i.get('row')
        id_list_sites.append(temp[0])

    for i in db_data_tiktok:
        temp = i.get('row')
        id_list_tiktoks.append(temp[0])

    completed_tasks_sites = user_info[0].get('completed_site_id')
    completed_tasks_tiktoks = user_info[0].get('completed_tiktok_id')

    task_id_site = 0
    task_id_tiktok = 0

    for i in id_list_sites:
        if i not in completed_tasks_sites:
            task_id_site = i

    for i in id_list_tiktoks:
        if i not in completed_tasks_tiktoks:
            task_id_tiktok = i

    if task_id_site == 0:
        site = InlineKeyboardButton(text=NO_TASKS, callback_data='none')
    else:
        active_task_record = await db.get_task_sites(task_id_site)
        url_sites = active_task_record[0].get('row')[1]
        site = InlineKeyboardButton(text=SITE_BUTTON, url=url_sites, callback_data='earn')

    if task_id_tiktok == 0:
        tiktok = InlineKeyboardButton(text=NO_TASKS, callback_data='none')
    else:
        active_task_record = await db.get_task_tiktok(task_id_tiktok)
        url_tiktok = active_task_record[0].get('row')[1]
        tiktok = InlineKeyboardButton(text=TIKTOK_BUTTON, url=url_tiktok, callback_data='earn')

    purchase = InlineKeyboardMarkup(row_width=1)
    referral = InlineKeyboardButton(text=INVITE_BUTTON, callback_data='referral')
    purchase.insert(referral)
    purchase.insert(tiktok)
    purchase.insert(site)
    return purchase
