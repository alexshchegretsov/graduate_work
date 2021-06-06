import json
from typing import List, Tuple

import aiohttp

from settings import TRANSLATE_URL, IAM_TOKEN, FOLDER_ID


async def translate(*args: Tuple[str], to_language: str = 'en') -> List[str]:
    headers = {'Authorization': 'Bearer ' + IAM_TOKEN}
    body = {
        'folderId': FOLDER_ID,
        'texts': args,
        'targetLanguageCode': to_language
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=TRANSLATE_URL, headers=headers, data=json.dumps(body)) as resp:
            data = await resp.json()

    return [x['text'] for x in data['translations']]
