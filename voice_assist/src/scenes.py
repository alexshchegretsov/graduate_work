import inspect
import sys
from typing import List, Dict

from decorators import error_handler
from helpers import translate, get_film_data
from misc import Request, Message, Command, Intents, Film
from settings import STATE_RESPONSE_KEY

__all__ = ['SCENES', 'DEFAULT_SCENE']


class Scene:
    commands: List[Command]

    @classmethod
    def id(cls):
        return cls.__name__

    @error_handler
    async def reply(self, request: Request):
        for command in self.commands:
            if command.phrase in request.intents:
                return await command(request)
        return self.fallback(request)

    def fallback(self, request: Request):
        return self.make_response(text=Message.FALLBACK_MESSAGE, state=request.state)

    def what_can_you_do(self, request: Request):
        return self.make_response(text=Message.WHAT_CAN_YOU_DO_MESSAGE, state=request.state)

    async def _on_search(self, request: Request, scene_id: str):
        movie_name = request.intents['search_film']['slots']['movie_name']['value']
        translated_name = await translate(movie_name)
        data = await get_film_data(translated_name[0])
        film = Film(**data)
        await film.translate_film()
        state = {
            'scene': scene_id,
            'data': film.dict()
        }

        text = Message.ON_SUCCESS_MESSAGE_TEMPLATE.format(film.translated.title)
        return self.make_response(text=text, state=state)

    def make_response(self, text, tts=None, state=None, scene_id=None):
        response = {
            'text': text,
            'tts': tts if tts is not None else text,
        }

        webhook_response = {
            'response': response,
            'version': '1.0',
            STATE_RESPONSE_KEY: {
                'scene': scene_id or self.id(),
            },
        }
        if state is not None:
            webhook_response[STATE_RESPONSE_KEY].update(state)
        return webhook_response


class WelcomeScene(Scene):

    def __init__(self):
        self.commands = [
            Command(phrase=Intents.HELP, func=self.on_help),
            Command(phrase=Intents.WHAT_CAN_YOU_DO, func=self.what_can_you_do),
            Command(phrase=Intents.SEARCH_FILM, func=self.on_search)
        ]

    async def on_search(self, request: Request):
        new_scene_id = FilmScene.id()
        return await self._on_search(request, new_scene_id)

    def on_help(self, request: Request):
        return self.make_response(text=Message.ON_WELCOME_HELP_MESSAGE, state=request.state)

    def welcome_message(self):
        return self.make_response(text=Message.WELCOME_MESSAGE)

    async def reply(self, request: Request):
        if request.is_session_new:
            return self.welcome_message()

        return await super().reply(request)


class FilmScene(Scene):

    def __init__(self):
        self.commands = [
            Command(phrase=Intents.HELP, func=self.on_help),
            Command(phrase=Intents.WHAT_CAN_YOU_DO, func=self.what_can_you_do),
            Command(phrase=Intents.SEARCH_FILM, func=self.on_search),
            Command(phrase=Intents.GET_DESCRIPTION, func=self.get_description)
        ]

    async def on_search(self, request: Request):
        new_scene_id = self.id()
        return await self._on_search(request, new_scene_id)

    def on_help(self, request: Request):
        return self.make_response(text=Message.ON_FILM_HELP_MESSAGE, state=request.state)

    async def get_description(self, request: Request):
        film = Film.parse_obj(request.state['data'])
        text = Message.FIELD_INFO_IS_NOT_EXISTS_MESSAGE if not film.description else film.translated.description
        return self.make_response(text=text, state=request.state)


def _list_scenes():
    current_module = sys.modules[__name__]
    scenes = []
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, Scene):
            scenes.append(obj)
    return scenes


SCENES = {
    scene.id(): scene for scene in _list_scenes()
}

DEFAULT_SCENE = WelcomeScene
