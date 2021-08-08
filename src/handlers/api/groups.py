from src.services.user_service import UserService
from src.utils.debugger import init_debug_mode
from src.utils.http import response

init_debug_mode()


def get_groups(event, _):
    try:
        username = event['queryStringParameters'].get('username')
    except AttributeError:
        return response('username is required', status=400)

    user_service = UserService()
    groups = user_service.get_user_groups(username=username)
    return response(groups)
