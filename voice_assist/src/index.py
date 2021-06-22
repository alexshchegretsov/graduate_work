import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from misc import Request
from scenes import SCENES, DEFAULT_SCENE
from settings import SENTRY_URL


sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)
sentry_sdk.init(dsn=SENTRY_URL, integrations=[sentry_logging])


async def handler(event, context):
    req = Request(event)
    current_scene_id = req.state.get('scene')
    if current_scene_id is None:
        return DEFAULT_SCENE().reply(req)    # new session welcoming

    current_scene = SCENES.get(current_scene_id, DEFAULT_SCENE)()
    return await current_scene.reply(req)
