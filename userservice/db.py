import logging
from acouchbase.cluster import Cluster
from couchbase.cluster import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from model import User
import uuid


LOGGER = logging.getLogger(__name__)


cluster = Cluster("http://couchbase:8091", options=ClusterOptions(PasswordAuthenticator(username='users', password='password')))
bucket = cluster.bucket('users')
bucket.on_connect()
collection = bucket.default_collection()


async def read_users():
    it = cluster.query('select META().id, users.* from `users`;')
    rows = []
    async for row in it:
        rows.append(row)
    return rows


async def read_user(user_id):
    get_result = await collection.get(user_id)
    return User(id=user_id, name=get_result.content['name'], email=get_result.content['email'])


async def register_user(user):
    user_id = str(uuid.uuid4())
    await collection.upsert(user_id, dict(name=user.name, email=user.email))
    return User(id=user_id, name=user.name, email=user.email)


async def modify_user(user):
    await read_user(user.id)
    await collection.upsert(user.id, dict(name=user.name, email=user.email))
    return User(id=user.id, name=user.name, email=user.email)


async def drop_user(user_id):
    await collection.remove(user_id)
