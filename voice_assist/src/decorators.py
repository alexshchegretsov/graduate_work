import logging

from exceptions import FilmNotFoundException
from helpers import make_response
from misc import Message, Request


def error_handler(coroutine):
    async def wrapper(request: Request):
        try:
            res = await coroutine(request)
        except FilmNotFoundException as ex:
            logging.exception(ex)
            return make_response(text=ex.message, state=request.state)
        except Exception as ex:
            logging.exception(ex)
            return make_response(text=Message.ON_ERROR_MESSAGE, state=request.state)
        return res

    return wrapper
