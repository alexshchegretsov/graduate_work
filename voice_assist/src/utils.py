from typing import Dict

from decorators import error_handler
from helpers import get_film_data, make_response, translate
from misc import Film, Message, Request, Scene


def welcome_message() -> Dict:
    return make_response(Message.WELCOME_MESSAGE, state={Scene.WELCOME: True})


@error_handler
async def search_film(req: Request) -> Dict:
    movie_name = req.intents['search_film']['slots']['movie_name']['value']
    translated_name = await translate(movie_name)
    data = await get_film_data(translated_name[0])
    film = Film(**data)
    await film.translate_film()
    state = {
        Scene.FILM: {
            'data': film.dict()
        }
    }

    text = Message.ON_SUCCESS_MESSAGE_TEMPLATE.format(film.translated.title)
    return make_response(text=text, state=state)


@error_handler
async def get_description(req: Request) -> Dict:
    film = Film.parse_obj(req.state[Scene.FILM]['data'])
    text = Message.FIELD_INFO_IS_NOT_EXISTS_MESSAGE if not film.description else film.translated.description
    return make_response(text=text, state=req.state)


def fallback(req: Request) -> Dict:
    return make_response(text=Message.FALLBACK_MESSAGE, state=req.state)


def on_welcome_help_message(req: Request) -> Dict:
    return make_response(text=Message.ON_WELCOME_HELP_MESSAGE, state=req.state)


def on_film_help_message(req: Request) -> Dict:
    return make_response(text=Message.ON_FILM_HELP_MESSAGE, state=req.state)


def what_can_you_do_msg(req: Request) -> Dict:
    return make_response(text=Message.WHAT_CAN_YOU_DO_MESSAGE, state=req.state)