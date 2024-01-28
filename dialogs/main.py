from aiogram_dialog import Dialog, Window, LaunchMode, DialogManager
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const
from aiogram import F

from . import states


async def getter(dialog_manager: DialogManager, **_kwargs):
    tg_id = dialog_manager.middleware_data['event_from_user'].id

    return {}


main_dialog = Dialog(
    Window(
        Const("Главное меню (в разработке)"),
        # Start(),
        Start(
            text=Const("Admin Panel"),
            id="admin_panel",
            state=states.Admin.ADMIN_MAIN,
            # when=
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
