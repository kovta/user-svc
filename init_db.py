from couchbase.cluster import Cluster
from couchbase.cluster import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.management.admin import Admin

from settings import BASE_DIR, get_config
from db import register_user
from model import CreateUser

adm = Admin('Administrator', 'password', host='couchbase', port=8091)

USER_CONFIG_PATH = BASE_DIR / 'config' / 'users.yaml'
USER_CONFIG = get_config(['-c', '../config/users.yaml'])


TEST_CONFIG_PATH = BASE_DIR / 'config' / 'users_test.yaml'
TEST_CONFIG = get_config(['-c', TEST_CONFIG_PATH.as_posix()])


def setup_db(conf):
    adm.bucket_create(conf['bucket'], bucket_type='couchbase', ram_quota=100)
    adm.wait_ready(conf['bucket'], timeout=30)


def teardown_db(conf):
    adm.bucket_remove(conf['bucket'])


def get_bucket(conf):
    cluster = Cluster("{host}:{port}".format(host=conf['host'], port=conf['port']),
                      options=ClusterOptions(PasswordAuthenticator(username=conf['user'], password=conf['password'])))
    return cluster.bucket(str(conf['bucket']))


def create_index(conf):
    manager = get_bucket(conf).bucket_manager()
    manager.n1ql_index_create_primary(ignore_exists=True)


def drop_index(conf):
    manager = get_bucket(conf).bucket_manager()
    manager.n1ql_index_remove_primary(ignore_exists=True)


def sample_data(conf):
    bucket = get_bucket(conf)
    bucket.on_connect()
    collection = bucket.default_collection()
    return [
        register_user(collection, CreateUser.Schema().loads({"name": "Rob", "email": "rob@rmail.com"})),
        register_user(collection, CreateUser.Schema().loads({"name": "Gregor", "email": "greg@gmail.com"}))
    ]


if __name__ == '__main__':
    config = USER_CONFIG['couchbase']
    setup_db(config)
    create_index(config)
    sample_data(config)
    # drop_tables()
    # teardown_db(USER_CONFIG['couchbase'])
