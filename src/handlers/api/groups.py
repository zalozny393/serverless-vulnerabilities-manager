from src.models.user_model import UserModel
from src.utils.debugger import init_debug_mode
from src.utils.http import response
from src.utils.request import request

init_debug_mode()


@request
def get_groups(user: UserModel, _):
    return response(user.groups)
