import aiohttp

from utils import translate


async def index(request):
    data = await request.json()

    response = {
        'version': data['version'],
        'session': data['session'],
        'response': {
            'end_session': False
        }
    }

    if data['session']['new']:
        response['response']['text'] = 'Привет! Я умею определять режиссёра по названию фильма'
    else:
        command = data['request']['command'].lower()

        if command == 'помощь':
            response['response']['text'] = 'Задайте вопрос вида: кто режиссёр фильма "Звёздные войны"?'
        elif command.startswith('что ты умеешь'):
            response['response']['text'] = 'умею определять режиссёра по названию фильма'
        elif command.startswith('кто режиссёр фильма'):
            _, f_name = command.split('кто режиссёр фильма')
            f_name = f_name.strip()
            translated_data = await translate(f_name)
            f_name_translated = translated_data[0]

            async with aiohttp.ClientSession() as session:
                async with session.get(url=f'http://localhost:8000/api/v1/film/search?query={f_name_translated}') as resp:
                    data = await resp.json()

                f_data = data[0]
                f_uuid = f_data.get('uuid')
                async with session.get(url=f'http://localhost:8000/api/v1/film/{f_uuid}') as resp:
                    data = await resp.json()

            directors = data.get('directors')
            directors = [x['full_name'] for x in directors]
            ru_directors = await translate(*directors, to_language='ru')
            print(ru_directors)
        else:
            response['response']['text'] = 'Переформулируйте запрос'

    return response
