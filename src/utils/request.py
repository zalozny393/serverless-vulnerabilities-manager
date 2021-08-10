from typing import Callable

from src.models.user_model import UserModel
from src.services.user_service import UserService
from src.utils.http import response


def request(handler: Callable[[UserModel, dict], dict]) -> Callable:
    def wrapper(event, context):
        try:
            username = event['queryStringParameters']['username']
        except KeyError:
            return response('username is required', status=400)

        user_service = UserService()
        user = user_service.get_user(username)
        return handler(user, event)
    return wrapper
