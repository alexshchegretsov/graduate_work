import json
from typing import Dict, List, Tuple

import aiohttp
from aiohttp.web import HTTPException

from exceptions import FilmNotFoundException
from settings import (ASYNC_API_URL, FOLDER_ID, STATE_RESPONSE_KEY,
                      TRANSLATE_API_KEY, TRANSLATE_URL)


async def translate(*args: Tuple[str], to_language: str = 'en') -> List[str]:
    headers = {'Authorization': 'Api-Key ' + TRANSLATE_API_KEY}
    body = {
        'folderId': FOLDER_ID,
        'texts': args,
        'targetLanguageCode': to_language
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=TRANSLATE_URL, headers=headers, data=json.dumps(body), raise_for_status=True) as resp:
            data = await resp.json()

    return [x.get('text', '') for x in data['translations']]


async def get_film_data(film_title: str) -> Dict:
    params = {'query': film_title}
    headers = {"Accept": 'application/json'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=ASYNC_API_URL, params=params, headers=headers) as resp:
            if not resp.ok:
                ex = FilmNotFoundException() if resp.status == 404 else HTTPException()
                raise ex

            return await resp.json()


def make_response(text, tts=None, state=None, scene_id=None):
    response = {
        'text': text,
        'tts': tts if tts is not None else text,
    }

    webhook_response = {
        'response': response,
        'version': '1.0',
        STATE_RESPONSE_KEY: {
            'scene': scene_id,
        },
    }
    if state is not None:
        webhook_response[STATE_RESPONSE_KEY].update(state)
    return webhook_response
