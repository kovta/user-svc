import requests
import json

API_BASE = 'http://localhost:8083/users'


def get_user_list():
    headers = {'Content-Type': 'application/json'}
    resp = requests.get(API_BASE, headers=headers)

    resp_body = resp.json()
    users = []
    for item in resp_body:
        user = {'id': item['id'], 'name': item['name'], 'email': item['email']}
        users.append(user)

    return users


def drop_users(id_list):
    for user_id in id_list:
        headers = {'Content-Type': 'application/json'}
        resp = requests.delete("{base}/{path}".format(base=API_BASE, path=user_id), headers=headers)
        if resp.status_code != 204:
            return False
    return True


def test_users_list():
    headers = {'Content-Type': 'application/json'}
    resp = requests.get(API_BASE, headers=headers)

    resp_body = resp.json()
    users = []
    for item in resp_body:
        user = {"id": item['id'], 'name': item['name'], 'email': item['email']}
        users.append(user)

    assert resp.status_code == 200
    assert len(users) == 0


def test_user_create():
    payload = {'name': 'greg', 'email': 'greg@gmail.com'}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(API_BASE, headers=headers, data=json.dumps(payload, indent=4))
    resp_body = resp.json()
    user_id = resp_body['id']

    user_resp = requests.get("{base}/{path}".format(base=API_BASE, path=user_id), headers=headers)

    assert user_resp.status_code == 200
    assert resp.status_code == 201
    assert drop_users([user_id]) is True


def test_invalid_user_create():
    payload = {'name': 'greg', 'email': 'random_email'}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(API_BASE, headers=headers, data=json.dumps(payload, indent=4))
    assert resp.status_code == 422


def test_invalid_user_create_payload():
    payload = {'test': 'test'}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(API_BASE, headers=headers, data=json.dumps(payload, indent=4))
    assert resp.status_code == 422


def test_user_update():
    payload = {'name': 'greg', 'email': 'greg@gmail.com'}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(API_BASE, headers=headers, data=json.dumps(payload, indent=4))
    resp_body = resp.json()
    user_id = resp_body['id']

    new_name = 'will'
    update_payload = {'id': user_id, 'name': new_name, 'email': 'greg@gmail.com'}
    update_resp = requests.put("{base}/{path}".format(base=API_BASE, path=user_id),
                               headers=headers, data=json.dumps(update_payload, indent=4))
    user_resp = requests.get("{base}/{path}".format(base=API_BASE, path=user_id), headers=headers)

    assert resp.status_code == 201
    assert update_resp.status_code == 202
    assert user_resp.status_code == 200
    assert update_resp.json()['name'] == new_name
    assert drop_users([user_id]) is True


def test_user_delete():
    payload = {'name': 'greg', 'email': 'greg@gmail.com'}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(API_BASE, headers=headers, data=json.dumps(payload, indent=4))
    resp_body = resp.json()
    user_id = resp_body['id']

    drop_users([user_id])
    user_resp = requests.get("{base}/{path}".format(base=API_BASE, path=user_id), headers=headers)

    assert resp.status_code == 201
    assert user_resp.status_code == 404
