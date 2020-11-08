import sys

from aiohttp import web
from app import setup_routes
from middlewares import setup_middlewares
from db import init_cb, close_cb
from settings import get_config
import logging


LOGGER = logging.getLogger(__name__)


async def init_app(config):
    app = web.Application()
    app['config'] = config

    app.on_startup.append(init_cb)
    app.on_cleanup.append(close_cb)
    setup_routes(app)
    setup_middlewares(app)

    return app


def main(argv):
    logging.basicConfig(level=logging.INFO)
    LOGGER.info('### Starting user service ###')

    config = get_config(argv)
    app = init_app(config)
    web.run_app(app,
                host=config['host'],
                port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
