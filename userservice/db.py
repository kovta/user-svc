from acouchbase.cluster import Cluster
from couchbase.cluster import ClusterOptions
from couchbase.auth import PasswordAuthenticator


cluster = Cluster("http://couchbase:8091", options=ClusterOptions(PasswordAuthenticator(username='users', password='password')))
bucket = cluster.bucket('users')
bucket.on_connect()
collection = bucket.default_collection()


async def read_users():
    upsert_result = await collection.upsert("doc1", dict(name="Ted", age=80))
    get_result = await collection.get("doc1")
    return get_result.content

