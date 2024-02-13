from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Back, SwitchTo, Select, Group, Start, Button, Next, Column, NumberedPager, StubScroll
from aiogram_dialog.widgets.text import Const, Format, Jinja
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from aiogram.types import ContentType, Message, CallbackQuery
from typing import Any

from db.requests import PlaceORM
from dialogs.common import MAIN_MENU_BUTTON
from . import states

ID_STUB_SCROLL = "stub_scroll"

async def places_category_getter(dialog_manager: DialogManager, **_kwargs):
    categories = await PlaceORM.get_category_places()
    return {'categories': categories}

async def places_subcategory_getter(dialog_manager: DialogManager, **_kwargs):
    subcategories = await PlaceORM.get_subcategory_places(dialog_manager.dialog_data['category'])
    return {'subcategories': subcategories}

async def on_category_selected(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, selected_item: str):
    dialog_manager.dialog_data['category'] = selected_item
    await dialog_manager.next()

async def on_subcategory_selected(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, selected_item: str):
    dialog_manager.dialog_data['subcategory'] = selected_item
    await dialog_manager.next()

async def on_back_selected(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.find(ID_STUB_SCROLL).set_page(0)

async def places_getter(dialog_manager: DialogManager, **_kwargs):
    subcategory = dialog_manager.dialog_data['subcategory']
    places = await PlaceORM.get_places_with_ordinal_ids(subcategory)
    if not places:
        return {'pages': 0, 'current_page': 0, 'places': None, 'photo': None}

    current_page = await dialog_manager.find(ID_STUB_SCROLL).get_page()
    if current_page >= len(places):
        current_page = len(places) - 1

    place_info = places[current_page]
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(place_info[3]))
    return {
        'pages': len(places),
        'current_page': current_page + 1,
        'places': place_info,
        'photo': image
    }

places_main_menu = Window(
    Const(text='Выбор Города TODO'),
    Next(text=Const('Ташкент'), id='places_next'),
    MAIN_MENU_BUTTON,
    state=states.Places.PLACES_MAIN
)

places_category_menu = Window(
    Const(text='<b>📚 Выберите категорию:</b>'),
    Column(Select(
        Format('{item}'),
        id='category',
        item_id_getter=lambda item: item,
        items='categories',
        on_click=on_category_selected
    )),
    Back(text=Const('Назад'), id='places_back'),
    MAIN_MENU_BUTTON,
    getter=places_category_getter,
    state=states.Places.PLACES_CATEGORY
)

places_subcategory_menu = Window(
    Const(text='<b>🔍 Выберите подкатегорию:</b>'),
    Column(Select(
        Format('{item}'),
        id='subcategory',
        item_id_getter=lambda item: item,
        items='subcategories',
        on_click=on_subcategory_selected
    )),
    Back(text=Const('Назад'), id='places_back'),
    MAIN_MENU_BUTTON,
    getter=places_subcategory_getter,
    state=states.Places.PLACES_SUBCATEGORY
)

places_menu = Window(
    DynamicMedia('photo'),
    Jinja('''
<b>🌟 {{ places.name }} 🌟</b>

<i>📝 Описание: {{ places.description }}</i>
    '''),
    StubScroll(id=ID_STUB_SCROLL, pages='pages'),
    NumberedPager(scroll=ID_STUB_SCROLL),
    Back(text=Const('Назад'), id='places_back', on_click=on_back_selected),
    MAIN_MENU_BUTTON,
    getter=places_getter,
    preview_data=places_getter,
    state=states.Places.PLACES_PLACE
)

places_dialog = Dialog(
    places_main_menu,
    places_category_menu,
    places_subcategory_menu,
    places_menu,
)
