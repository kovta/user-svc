import logging
from acouchbase.cluster import Cluster
from couchbase.cluster import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from model import User
import uuid


LOGGER = logging.getLogger(__name__)


async def init_cb(app):
    conf = app['config']['couchbase']
    cluster = Cluster("{host}:{port}".format(host=conf['host'], port=conf['port']),
                      options=ClusterOptions(PasswordAuthenticator(username=conf['user'], password=conf['password'])))
    bucket = cluster.bucket(str(conf['bucket']))
    bucket.on_connect()
    collection = bucket.default_collection()
    app['cb'] = cluster
    app['db'] = collection


async def close_cb(app):
    await app['cb'].cluster.disconnect()


async def read_users(cluster):
    it = cluster.query('select META().id, users.* from `users`;')
    rows = []
    async for row in it:
        rows.append(row)
    return rows


async def read_user(collection, user_id):
    get_result = await collection.get(user_id)
    return User(id=user_id, name=get_result.content['name'], email=get_result.content['email'])


async def register_user(collection, create_user):
    user_id = str(uuid.uuid4())
    await collection.upsert(user_id, dict(name=create_user.name, email=create_user.email))
    return User(id=user_id, name=create_user.name, email=create_user.email)


async def modify_user(collection, user):
    await read_user(collection, user.id)
    await collection.upsert(user.id, dict(name=user.name, email=user.email))
    return User(id=user.id, name=user.name, email=user.email)


async def drop_user(collection, user_id):
    await collection.remove(user_id)
