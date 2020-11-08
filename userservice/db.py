from acouchbase.cluster import Cluster
from couchbase.cluster import ClusterOptions
from couchbase.auth import PasswordAuthenticator
import uuid


cluster = Cluster("http://couchbase:8091", options=ClusterOptions(PasswordAuthenticator(username='users', password='password')))
bucket = cluster.bucket('users')
bucket.on_connect()
collection = bucket.default_collection()


async def read_user_test():
    id = uuid.uuid4()
    upsert_result = await collection.upsert(str(id), dict(name="Ted", email=80))
    get_result = await collection.get(str(id))
    return get_result.content


async def read_users():
    it = cluster.query('select META().id, users.* from `users`;')
    rows = []
    async for row in it:
        rows.append(row)
    return rows


async def read_user(id):
    get_result = await collection.get(id)
    return get_result.content


async def write_user(user):
    write_result = await collection.upsert(str(uuid.uuid4()), dict(name=user.name, email=user.email))
    return write_result.content


async def drop_user(user):
    write_result = await collection.remove(user.id)
    return write_result.content