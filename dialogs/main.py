from aiogram_dialog import Dialog, Window, LaunchMode, DialogManager
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const, Jinja
from aiogram import F

from . import states


async def getter(dialog_manager: DialogManager, **_kwargs):
    tg_id = dialog_manager.middleware_data['event_from_user'].id
    TEXT = (
        'Этот бот поможет вам найти уникальные и увлекательные места для посещения в разных городах. Независимо от того, '
        'ищете ли вы кафе с уютной атмосферой, запоминающиеся достопримечательности или тихие парки для прогулок, '
        'здесь вы найдете что-то для себя.')
    return {'TEXT': TEXT}


main_dialog = Dialog(
    Window(
        Jinja('''
<b>🌍 Приветствую в нашем боте-каталоге интересных мест!</b> 

{{TEXT}}
'''),

        Start(
            text=Const("Admin Panel"),
            id="admin_panel",
            state=states.Admin.ADMIN_MAIN,
            #when='False'
        ),
        Start(
            text=Const("Places"),
            id="places",
            state=states.Places.PLACES_MAIN
        ),
        state=states.Main.MAIN,
        getter=getter
    ),
    launch_mode=LaunchMode.ROOT
)
