import asyncio

from aiohttp import web

# from settings import


class ApiRouter(web.UrlDispatcher):

    def add_route(self, method, path, handler, *, name=None, expect_handler=None):

        # add route with and without tailing slash
        paths = [path]
        if len(path) > 1 and path[-1] == '/':
            paths.append(path[:-1])
        elif len(path) > 1 and path[-1] != '/':
            paths.append(path + '/')

        for _path in paths:
            super().add_route('OPTIONS', _path, self.options_handler, name=name, expect_handler=expect_handler)
            res = super().add_route(method, _path, handler, name=name, expect_handler=expect_handler)
        return res

    def options_handler(self, request):
        return web.Response(text='OK', status=200)


async def init_app():
    app = web.Application(router=ApiRouter())
    return app


loop = asyncio.get_event_loop()
app = loop.run_until_complete(init_app())