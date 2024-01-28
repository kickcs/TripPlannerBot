from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import (Back, SwitchTo, Select, Group, Start, Button, Next, Column)
from aiogram_dialog.widgets.text import Const, Format, Jinja
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import ChatEvent

from aiogram.types import ContentType, Message, CallbackQuery
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram import F
from typing import Any

from db.requests import PlaceORM
from dialogs.common import MAIN_MENU_BUTTON
from . import states


async def admin_add_category_handler(message: Message, message_input: MessageInput,
                                     dialog_manager: DialogManager):
    if dialog_manager.is_preview():
        await dialog_manager.next()
        return
    dialog_manager.dialog_data['category'] = message.text
    await dialog_manager.next()


async def admin_add_subcategory_handler(message: Message, message_input: MessageInput,
                                        dialog_manager: DialogManager):
    if dialog_manager.is_preview():
        await dialog_manager.next()
        return
    dialog_manager.dialog_data['subcategory'] = message.text
    await dialog_manager.next()


async def admin_add_name_handler(message: Message, message_input: MessageInput,
                                 dialog_manager: DialogManager):
    if dialog_manager.is_preview():
        await dialog_manager.next()
        return
    dialog_manager.dialog_data['name'] = message.text
    await dialog_manager.next()


async def admin_add_description_handler(message: Message, message_input: MessageInput,
                                        dialog_manager: DialogManager):
    if dialog_manager.is_preview():
        await dialog_manager.next()
        return
    dialog_manager.dialog_data['desc'] = message.text
    await dialog_manager.next()
    print(dialog_manager.dialog_data)


async def on_input_photo(message: Message, widget: MessageInput,
                         dialog_manager: DialogManager):
    if dialog_manager.is_preview():
        await dialog_manager.next()
        return
    dialog_manager.dialog_data.setdefault("photos", []).append(
        (message.photo[-1].file_id, message.photo[-1].file_unique_id),
    )
    await dialog_manager.next()


async def on_click_admin_add_complete(callback: CallbackQuery, widget: Button,
                                      manager: DialogManager):
    await PlaceORM.create_place(
        category=manager.dialog_data["category"],
        subcategory=manager.dialog_data["subcategory"],
        name=manager.dialog_data["name"],
        desc=manager.dialog_data["desc"],
        address=None,
        image_id=manager.dialog_data["photos"][0][0] if manager.dialog_data["photos"] else None
    )
    await callback.answer("Запись добавлена")
    await manager.done()
    await manager.switch_to(states.Admin.ADMIN_MAIN)


async def getter(dialog_manager: DialogManager, **_kwargs):
    category = dialog_manager.dialog_data.get("category", "")
    subcategory = dialog_manager.dialog_data.get("subcategory", "")
    name = dialog_manager.dialog_data.get("name", "")
    desc = dialog_manager.dialog_data.get("desc", "")
    photos = dialog_manager.dialog_data.get("photos", [])
    if photos:
        photo = photos[-1]
        media = MediaAttachment(
            file_id=MediaId(*photo),
            type=ContentType.PHOTO,
        )
    else:
        media = MediaAttachment(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/800px"
                "-Image_not_available.png?20210219185637",
            type=ContentType.PHOTO,
        )
    return {
        "category": category,
        "subcategory": subcategory,
        "name": name,
        "desc": desc,
        'media': media,
    }


async def other_type_handler(message: Message, message_input: MessageInput,
                             manager: DialogManager):
    await message.answer('Ваше сообщение совсем не похоже на текстовое!\n'
                         'Пожалуйста, повторите попытку.')


async def admin_delete_getter(dialog_manager: DialogManager, **_kwargs):
    places = await PlaceORM.get_places_id_and_name()
    return {'places': places}


async def on_click_admin_delete(callback: CallbackQuery, widget: Any,
                                dialog_manager: DialogManager, selected_item: int):
    await PlaceORM.delete_place(selected_item)
    await callback.answer("Запись удалена")
    await dialog_manager.done()


admin_main_menu = Window(
    Const("Админ панель, здесь вы можете добавить, удалить и редактировать места"),
    Group(
        Start(text=Const("Добавить место"), id="add_place", state=states.Admin.ADMIN_ADD_CATEGORY),
        Start(text=Const("Удалить место"), id="delete_place", state=states.Admin.ADMIN_DELETE),
        Start(text=Const("Редактировать место"), id="edit_place", state=states.Admin.ADMIN_EDIT),
        MAIN_MENU_BUTTON
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
    Const('Добавьте фото места'),
    MessageInput(content_types=[ContentType.PHOTO], func=on_input_photo),
    Next(text=Const("Пропустить"), id="next"),
    Back(text=Const("Назад"), id="back"),
    state=states.Admin.ADMIN_ADD_IMAGE
)

admin_add_complete = Window(
    Jinja('''
Категория: {{ category }}
Подкатегория: {{ subcategory }}
Название: {{ name }}
Описание: {{ desc }}
'''),
    DynamicMedia(selector="media"),
    Button(text=Const("Завершить добавление"),
           id="add_complete",
           on_click=on_click_admin_add_complete),
    Back(text=Const("Назад"), id="back"),
    state=states.Admin.ADMIN_ADD_COMPLETE,
    getter=getter
)

admin_delete = Window(
    Const('Выберите место, которое хотите удалить'),
    Column(Select(
        Format('{item}'),
        id='places',
        item_id_getter=lambda item: item[0],
        items='places',
        on_click=on_click_admin_delete
    )),
    SwitchTo(text=Const("Назад"), id="back", state=states.Admin.ADMIN_MAIN),
    state=states.Admin.ADMIN_DELETE,
    getter=admin_delete_getter
)

admin_dialog = Dialog(
    admin_main_menu,
    admin_add_category,
    admin_add_subcategory,
    admin_add_name_place,
    admin_add_description,
    admin_add_image,
    admin_add_complete,
    admin_delete
)
