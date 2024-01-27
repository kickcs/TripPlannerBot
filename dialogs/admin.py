from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import (Back, SwitchTo, Select, Group, Start, Button)
from aiogram_dialog.widgets.text import Const, Format, Jinja
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import ChatEvent

from aiogram.types import ContentType, Message, CallbackQuery
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram import F
from typing import Any

from db.requests import PlaceORM
from . import states


async def admin_add_category_handler(message: Message, message_input: MessageInput,
                                     dialog_manager: DialogManager):
    if dialog_manager.is_preview():
        await dialog_manager.next()
        return
    dialog_manager.dialog_data['category'] = message_input.text
    await dialog_manager.next()


async def admin_add_subcategory_handler(message: Message, message_input: MessageInput,
                                        dialog_manager: DialogManager):
    if dialog_manager.is_preview():
        await dialog_manager.next()
        return
    dialog_manager.dialog_data['subcategory'] = message_input.text
    await dialog_manager.next()


async def admin_add_name_handler(message: Message, message_input: MessageInput,
                                 dialog_manager: DialogManager):
    if dialog_manager.is_preview():
        await dialog_manager.next()
        return
    dialog_manager.dialog_data['name'] = message_input.text
    await dialog_manager.next()


async def admin_add_description_handler(message: Message, message_input: MessageInput,
                                       dialog_manager: DialogManager):
    if dialog_manager.is_preview():
        await dialog_manager.next()
        return
    dialog_manager.dialog_data['decription'] = message_input.text
    await dialog_manager.next()


async def other_type_handler(message: Message, message_input: MessageInput,
                             manager: DialogManager):
    await message.answer('Ваше сообщение совсем не похоже на текстовое!\n'
                         'Пожалуйста, повторите попытку.')


admin_main_menu = Window(
    Const("Админ панель, здесь вы можете добавить, удалить и редактировать места"),
    Group(
        Start(text=Const("Добавить место"), id="add_place", state=states.Admin.ADMIN_ADD_CATEGORY),
        Start(text=Const("Удалить место"), id="delete_place", state=states.Admin.ADMIN_DELETE),
        Start(text=Const("Редактировать место"), id="edit_place", state=states.Admin.ADMIN_EDIT),
    ),
    state=states.Admin.ADMIN_MAIN
)

admin_add_category = Window(
    Const('Введите название категории'),
    MessageInput(admin_add_category_handler, content_types=[ContentType.TEXT]),
    MessageInput(other_type_handler),
    Back(text=Const("Назад"), id="back"),
    state=states.Admin.ADMIN_ADD_CATEGORY
)

admin_add_subcategory = Window(
    Const('Введите название подкатегории'),
    MessageInput(admin_add_subcategory_handler, content_types=[ContentType.TEXT]),
    MessageInput(other_type_handler),
    Back(text=Const("Назад"), id="back"),
    state=states.Admin.ADMIN_ADD_SUBCATEGORY
)

admin_add_name_place = Window(
    Const('Введите название места'),
    MessageInput(admin_add_name_handler, content_types=[ContentType.TEXT]),
    MessageInput(other_type_handler),
    Back(text=Const("Назад"), id="back"),
    state=states.Admin.ADMIN_ADD_NAME_PLACE
)

admin_add_description = Window(
    Const('Введите описание места'),
    MessageInput(admin_add_description_handler, content_types=[ContentType.TEXT]),
    MessageInput(other_type_handler),
    Back(text=Const("Назад"), id="back"),
    state=states.Admin.ADMIN_ADD_DESCRIPTION
)

admin_add_image = Window(
    Back(text=Const("Назад"), id="back"),
    state=states.Admin.ADMIN_ADD_IMAGE
)

admin_dialog = Dialog(
    admin_main_menu,
    admin_add_category,
    admin_add_subcategory,
    admin_add_name_place,
    admin_add_description,
    admin_add_image
)
