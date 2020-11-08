import logging
from aiohttp import web
from model import User, CreateUser, InvalidInputError
import db


LOGGER = logging.getLogger(__name__)
routes = web.RouteTableDef()


def setup_routes(app):
    app.add_routes(routes)


@routes.get('/')
async def health(request):
    return web.json_response({'name': 'user-service'})


@routes.get('/users')
async def get_users(request):
    LOGGER.info('### Retrieving all users ###')
    users = await db.read_users(request.app['cb'])
    return web.json_response(users)


@routes.get('/users/{user_id}')
async def get_user(request):
    user_id = request.match_info['user_id']
    LOGGER.info('### Retrieving user by id: {} ###'.format(user_id))
    user = await db.read_user(request.app['db'], user_id)
    return web.json_response(user.to_dict())


@routes.post('/users')
async def create_user(request):
    LOGGER.info('### Create new user ###')
    body = await request.text()
    user = await db.register_user(request.app['db'], CreateUser.Schema().loads(body))
    return web.json_response(user.to_dict(), status=201)


@routes.put('/users/{user_id}')
async def update_user(request):
    user_id = request.match_info['user_id']
    LOGGER.info('### Update user by id: {} ###'.format(user_id))
    body = await request.text()
    request_body =  User.Schema().loads(body)
    if request_body.id != user_id:
        raise InvalidInputError("Path id does not match request body")
    user = await db.modify_user(request.app['db'], User.Schema().loads(body))
    return web.json_response(user.to_dict(), status=202)


@routes.delete('/users/{user_id}')
async def delete_user(request):
    user_id = request.match_info['user_id']
    LOGGER.info('### Delete user by id: {} ###'.format(user_id))
    await db.drop_user(request.app['db'], user_id)
    return web.json_response(None, status=204)
