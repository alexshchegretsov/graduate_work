import logging
from typing import Dict, List, Optional, Callable

from pydantic import BaseModel

from helpers import translate
from settings import STATE_REQUEST_KEY


class Request:
    def __init__(self, request_body: Dict):
        self.request_body = request_body

    def __getitem__(self, key):
        return self.request_body[key]

    @property
    def intents(self):
        _intents = {}
        try:
            _intents = self.request_body['request']['nlu']['intents']
        except KeyError as ex:
            logging.exception(ex)
        return _intents

    @property
    def state(self):
        _state = {}
        try:
            _state = self.request_body['state'][STATE_REQUEST_KEY]
        except KeyError as ex:
            logging.exception(ex)
        return _state

    @property
    def is_session_new(self):
        return self.request_body['session']['new']


class FilmPerson(BaseModel):
    uuid: str
    full_name: str


class Genre(BaseModel):
    uuid: str
    name: str


class TranslatedFilm(BaseModel):
    title: str
    imdb_rating: float
    description: str
    genres: str
    actors: str
    writers: str
    directors: str


class Film(BaseModel):
    uuid: str
    title: str
    imdb_rating: float
    description: str
    genres: List[Genre]
    actors: List[FilmPerson]
    writers: List[FilmPerson]
    directors: List[FilmPerson]
    translated: Optional[TranslatedFilm]
    is_translated: bool = False

    async def translate_film(self) -> None:
        if not self.is_translated:
            data_to_translate = self._to_translate()
            print('to trans', data_to_translate)
            data = await translate(data_to_translate, to_language='ru')
            self.translated = TranslatedFilm(**dict(zip(TranslatedFilm.__fields__.keys(), data)))
            self.is_translated = True

    def _to_translate(self) -> List[str]:
        genres = ', '.join(x.name for x in self.genres)
        actors = ', '.join(x.full_name for x in self.actors)
        writers = ', '.join(x.full_name for x in self.writers)
        directors = ', '.join(x.full_name for x in self.directors)
        return [self.title, str(self.imdb_rating), self.description, genres, actors, writers, directors]



class Intents:
    WHAT_CAN_YOU_DO = 'what_can_you_do'
    HELP = 'YANDEX.HELP'
    SEARCH_FILM = 'search_film'
    GET_DESCRIPTION = 'get_description'

    __slots__ = []


class Message:
    ON_ERROR_MESSAGE = 'Что-то пошло не так, попробуйте ещё раз.'
    WELCOME_MESSAGE = """
    Быстрая справка по фильмам из кинотеатра.
    Что бы узнать доступные команды - используй команду -  Помощь
    """
    FALLBACK_MESSAGE = 'Извините, я вас не поняла. Пожалуйста, переформулируйте запрос.'
    ON_WELCOME_HELP_MESSAGE = """
    Что бы узнать описание навыка - используйте команду - Что ты умеешь?
    Что бы найти фильм - используйте команду - "Найди фильм".
    Что бы выйти - используйте команду - Хватит.
    """
    ON_FILM_HELP_MESSAGE = """
    Что бы получить описание найденного фильма - используйте команду - "Дай описание".
    Что бы выйти - используйте команду - Хватит.
    """
    WHAT_CAN_YOU_DO_MESSAGE = 'Мой навык в том, что бы искать фильмы и предоставлять информацию о них.'
    FIELD_INFO_IS_NOT_EXISTS_MESSAGE = 'К сожалению информация по этому полю отсутствует'
    NOT_FOUND_MESSAGE_TEMPLATE = 'По запросу {} - ничего не найдено, переформулируйте запрос.'
    ON_SUCCESS_MESSAGE_TEMPLATE = 'Найден фильм - {}'

    __slots__ = []


class Command:
    def __init__(self, phrase: str, func: Callable):
        self.phrase = phrase
        self.func = func

    async def __call__(self, *args, **kwargs):
        return await self.func(*args, **kwargs)

