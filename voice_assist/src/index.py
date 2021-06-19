import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from misc import FilmSceneIntents, Request, Scene, WelcomeSceneIntents
from settings import SENTRY_URL
from utils import (fallback, get_description, on_film_help_message,
                   on_welcome_help_message, search_film, welcome_message,
                   what_can_you_do_msg)

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)
sentry_sdk.init(dsn=SENTRY_URL, integrations=[sentry_logging])


async def handler(event, context):
    req = Request(event)
    state = req.state

    if req['session']['new']:
        return welcome_message()

    elif state.get(Scene.WELCOME):

        if WelcomeSceneIntents.HELP in req.intents:
            return on_welcome_help_message(req)
        elif WelcomeSceneIntents.WHAT_CAN_YOU_DO in req.intents:
            return what_can_you_do_msg(req)
        elif WelcomeSceneIntents.SEARCH_FILM in req.intents:
            return await search_film(req)

    elif state.get(Scene.FILM):

        if FilmSceneIntents.HELP in req.intents:
            return on_film_help_message(req)
        elif FilmSceneIntents.WHAT_CAN_YOU_DO in req.intents:
            return what_can_you_do_msg(req)
        elif FilmSceneIntents.GET_DESCRIPTION in req.intents:
            return await get_description(req)
        elif FilmSceneIntents.SEARCH_FILM in req.intents:
            return await search_film(req)

    return fallback(req)
