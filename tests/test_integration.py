"""Requires a running database server"""

async def test_index(cli, tables_and_data):
    response = await cli.get('/')
    assert response.status == 200
    assert '{\'name\': \'user-service\'}' in await response.text()


async def test_results(cli, tables_and_data):
    response = await cli.get('/users')
    assert response.status == 200
    assert '[]' in await response.text()


async def test_404_status(cli, tables_and_data):
    response = await cli.get('/no-such-route')
    assert response.status == 404
