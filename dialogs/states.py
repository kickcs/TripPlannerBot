from aiogram.fsm.state import State, StatesGroup


class Main(StatesGroup):
    MAIN = State()


class Admin(StatesGroup):
    ADMIN_MAIN = State()
    ADMIN_ADD_CATEGORY = State()
    ADMIN_ADD_SUBCATEGORY = State()
    ADMIN_ADD_NAME_PLACE = State()
    ADMIN_ADD_DESCRIPTION = State()
    ADMIN_ADD_ADDRESS = State()
    ADMIN_ADD_IMAGE = State()
    ADMIN_ADD_COMPLETE = State()
    ADMIN_DELETE = State()
    ADMIN_EDIT = State()


class Profile(StatesGroup):
    PROFILE_MAIN = State()
