import pytest

from aiohttp import web
from main import init_app
from settings import BASE_DIR, get_config
from init_db import (
    setup_db,
    teardown_db,
    create_index,
    sample_data,
    drop_index
)

TEST_CONFIG_PATH = BASE_DIR / 'config' / 'users_test.yaml'


@pytest.fixture
async def cli(loop, aiohttp_client, db):
    # config = get_config(['-c', TEST_CONFIG_PATH.as_posix()])
    # app = await init_app(config)
    app = web.Application(loop=loop)
    return await aiohttp_client(app)


@pytest.fixture(scope='module')
def db():
    config = get_config(['-c', TEST_CONFIG_PATH.as_posix()])
    cb_conf = config['couchbase']

    setup_db(cb_conf)
    yield
    teardown_db(cb_conf)


@pytest.fixture
def tables_and_data():
    config = get_config(['-c', TEST_CONFIG_PATH.as_posix()])
    cb_conf = config['couchbase']

    create_index(cb_conf)
    data = sample_data(cb_conf)
    yield data
    drop_index(cb_conf)
