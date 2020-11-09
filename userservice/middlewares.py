import logging
from aiohttp import web
from aiohttp_cors import setup, ResourceOptions
from json.decoder import JSONDecodeError
from aiohttp.web_exceptions import HTTPNotFound
from marshmallow.exceptions import ValidationError
from model import InvalidInputError
from couchbase.exceptions import DocumentNotFoundException

LOGGER = logging.getLogger(__name__)


def setup_cors(app):
    cors = setup(app, defaults={
        "*": ResourceOptions(
            allow_credentials=True,
            allow_methods=["GET", "Post", "PUT", "DELETE"],
            expose_headers="*",
            allow_headers="*",
        )
    })
    for route in list(app.router.routes()):
        cors.add(route)


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        400: handle_400,
        404: handle_404,
        422: handle_422,
        500: handle_500
    })
    app.middlewares.append(error_middleware)


def create_error_middleware(overrides):

    @web.middleware
    async def error_middleware(request, handler):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)
            raise
        except JSONDecodeError as ex:
            LOGGER.error(ex)
            return await overrides[400](request)
        except HTTPNotFound as ex:
            LOGGER.error(ex)
            return await overrides[404](request)
        except (ValidationError, InvalidInputError) as ex:
            LOGGER.error(ex)
            return await overrides[422](request)
        except DocumentNotFoundException as ex:
            LOGGER.error("User with id: {} does not exist".format(request.match_info['user_id']))
            return await overrides[404](request)
        except Exception as ex:
            LOGGER.error(fullname(ex))
            LOGGER.error(ex)
            return await overrides[500](request)

    return error_middleware


async def handle_400(request):
    return web.json_response({'400': 'Bad request'}, status=400)


async def handle_404(request):
    return web.json_response({'404': 'Not found'}, status=404)


async def handle_422(request):
    return web.json_response({'422': 'Unprocessable Entity'}, status=422)


async def handle_500(request):
    return web.json_response({'500': 'Unexpected Error'}, status=500)


def fullname(o):
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__
    else:
        return module + '.' + o.__class__.__name__
