import logging
from aiohttp import web
from model import User
import db


LOGGER = logging.getLogger(__name__)


routes = web.RouteTableDef()


@routes.get('/')
async def health(request):
    return web.json_response({'name': 'user-service'})


@routes.get('/users')
async def get_users(request):
    LOGGER.info('### Retrieving all users ###')
    users = await db.read_users()
    return web.json_response(users)


@routes.get('/users/{user_id}')
async def get_users(request):
    user_id = request.match_info['user_id']
    LOGGER.info('### Retrieving user by id: {} ###'.format(user_id))
    user = await db.read_user(user_id)
    return web.json_response(user.to_dict())


@routes.post('/users')
async def create_user(request):
    LOGGER.info('### Create new user ###')
    body = await request.json()
    user = await db.register_user(User(id=None, name=body['name'], email=body['email']))
    return web.json_response(user.to_dict(), status=201)


@routes.put('/users/{user_id}')
async def update_user(request):
    user_id = request.match_info['user_id']
    LOGGER.info('### Update user by id: {} ###'.format(user_id))
    body = await request.json()
    user = await db.modify_user(User(id=body['id'], name=body['name'], email=body['email']))
    return web.json_response(user.to_dict(), status=202)


@routes.delete('/users/{user_id}')
async def delete_user(request):
    user_id = request.match_info['user_id']
    LOGGER.info('### Delete user by id: {} ###'.format(user_id))
    await db.drop_user(user_id)
    return web.json_response(None, status=204)


def create_app():
    app = web.Application()
    app.add_routes(routes)
    return app
