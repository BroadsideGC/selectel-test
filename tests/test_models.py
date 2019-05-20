import json
import time

from service.api.api import RESULT_OK


def get_all_servers(api_client, sort_by_date=False, include_deleted=False):
    rv = api_client.get('/api/v1/servers?sortByDate={}&includeDeleted={}'.format(sort_by_date, include_deleted))
    return rv


def create_server(api_client):
    rv = api_client.post('/api/v1/servers')
    return rv


def delete_server(api_client, server_id):
    rv = api_client.delete('/api/v1/servers/{}'.format(server_id))
    return rv


def get_server(api_client, server_id):
    rv = api_client.get('/api/v1/servers/{}'.format(server_id))
    return rv


def pay_server(api_client, server_id, expiration_date):
    req_data = {
        'action': 'pay',
        'expirationDate': expiration_date
    }
    rv = api_client.put('/api/v1/servers/{}'.format(server_id), json=req_data)
    return rv


def get_all_server_racks(api_client, sort_by_date=False, include_deleted=False):
    rv = api_client.get('/api/v1/serverRacks?sortByDate={}&includeDeleted={}'.format(sort_by_date, include_deleted))
    return rv


def create_server_rack(api_client, is_big=False):
    rv = api_client.post('/api/v1/serverRacks?isBig={}'.format(is_big))
    return rv


def delete_server_rack(api_client, server_rack_id):
    rv = api_client.delete('/api/v1/serverRacks/{}'.format(server_rack_id))
    return rv


def get_server_rack(api_client, server_rack_id):
    rv = api_client.get('/api/v1/serverRacks/{}'.format(server_rack_id))
    return rv


def add_server_to_rack(api_client, server_rack_id, server_id):
    req_data = {
        'action': 'add-server',
        'serverId': server_id
    }
    rv = api_client.put('/api/v1/serverRacks/{}'.format(server_rack_id), json=req_data)
    return rv


def remove_server_from_rack(api_client, server_rack_id, server_id):
    req_data = {
        'action': 'remove-server',
        'serverId': server_id
    }
    rv = api_client.put('/api/v1/serverRacks/{}'.format(server_rack_id), json=req_data)
    return rv


def test_empty_servers(api_client):
    """Start with a blank database."""
    rv = get_all_servers(api_client, include_deleted=True)
    assert rv.status_code == 200
    assert json.loads(rv.data) == {'result': []}


def test_empty_server_racks(api_client):
    """Start with a blank database."""
    rv = get_all_server_racks(api_client)
    assert rv.status_code == 200
    assert json.loads(rv.data) == {'result': []}


def test_wrong_url(api_client):
    rv = api_client.get('/api/v1/serverRacksssss')
    assert rv.status_code == 404


def test_create_server(api_client):
    rv = create_server(api_client)
    assert rv.status_code == 200
    assert 'id' in json.loads(rv.data)['result']


def test_create_delete_server(api_client):
    rv = create_server(api_client)
    assert rv.status_code == 200
    assert 'id' in json.loads(rv.data)['result']
    server_id = json.loads(rv.data)['result']['id']
    rv = delete_server(api_client, server_id)
    assert rv.status_code == 200
    assert json.loads(rv.data) == RESULT_OK


def test_one_deleted_server(api_client):
    rv = get_all_servers(api_client, include_deleted=True)
    data = json.loads(rv.data)
    servers = data['result']
    assert rv.status_code == 200
    assert data != {'result': []}
    assert len(servers) == 2
    assert servers[0].get('status') == 'Unpaid'
    assert servers[1].get('status') == 'Deleted'


def test_pay_server(api_client):
    rv = pay_server(api_client, 1, time.time() + 1e6)
    assert rv.status_code == 200
    assert json.loads(rv.data) == RESULT_OK

    rv = get_server(api_client, 1)
    assert rv.status_code == 200
    assert json.loads(rv.data).get('result').get('status') == 'Active'


def test_pay_non_existing_server(api_client):
    rv = pay_server(api_client, 1000, time.time() + 1e6)
    assert rv.status_code == 404
    assert b'Server not found' in rv.data


def test_pay_activated_server(api_client):
    rv = pay_server(api_client, 1, time.time() + 1e6)
    assert rv.status_code == 200
    assert json.loads(rv.data) == RESULT_OK


def test_pay_deleted_server(api_client):
    rv = pay_server(api_client, 2, time.time() + 1e6)
    assert rv.status_code == 410
    assert b'Server deleted' in rv.data


def test_create_server_rack(api_client):
    rv = create_server_rack(api_client)
    assert rv.status_code == 200
    assert 'result' in json.loads(rv.data)
    rv = get_server_rack(api_client, 1)
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert 'result' in data
    assert data['result']['size'] == 10


def test_create_big_server_rack(api_client):
    rv = create_server_rack(api_client, is_big=True)
    assert rv.status_code == 200
    assert 'result' in json.loads(rv.data)
    print(rv.data)
    rv = get_server_rack(api_client, 2)
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert 'result' in data
    assert data['result']['size'] == 20


def test_second_server_rack(api_client):
    rv = create_server_rack(api_client)
    assert rv.status_code == 200
    assert 'result' in json.loads(rv.data)


def test_create_delete_server_rack(api_client):
    rv = create_server_rack(api_client)
    assert rv.status_code == 200
    assert 'id' in json.loads(rv.data)['result']
    server_rack_id = json.loads(rv.data)['result']['id']
    rv = delete_server_rack(api_client, server_rack_id)
    assert rv.status_code == 200
    assert json.loads(rv.data) == RESULT_OK


def test_add_server_to_rack(api_client):
    rv = add_server_to_rack(api_client, 1, 1)
    assert rv.status_code == 200
    assert json.loads(rv.data) == RESULT_OK


def test_add_server_that_already_in_rack_to_rack(api_client):
    rv = add_server_to_rack(api_client, 1, 1)
    assert rv.status_code == 200
    assert json.loads(rv.data) == RESULT_OK


def test_add_server_that_already_in_rack_to_other_rack(api_client):
    rv = add_server_to_rack(api_client, 2, 1)
    assert rv.status_code == 422
    assert b'Server belong to other server rack or doesn`t exist' in rv.data


def test_remove_server_from_rack(api_client):
    rv = remove_server_from_rack(api_client, 1, 1)
    assert rv.status_code == 200
    assert json.loads(rv.data) == RESULT_OK


def test_remove_server_that_doesnt_belong_to_rack(api_client):
    rv = remove_server_from_rack(api_client, 2, 1)
    assert rv.status_code == 422
    assert b'Server doesn`t belong to server rack' in rv.data


def test_remove_server_that_already_removed(api_client):
    rv = remove_server_from_rack(api_client, 1, 1)
    assert rv.status_code == 200
    assert json.loads(rv.data) == RESULT_OK


def test_create_20_servers(api_client):
    for i in range(20):
        rv = create_server(api_client)
        assert rv.status_code == 200
        assert 'id' in json.loads(rv.data)['result']


def test_create_5_server_racks(api_client):
    for i in range(20):
        rv = create_server_rack(api_client)
        assert rv.status_code == 200
        assert 'id' in json.loads(rv.data)['result']


def test_fill_server_rack(api_client):
    for i in range(5, 15):
        rv = add_server_to_rack(api_client, 3, i)
        assert rv.status_code == 200
        assert json.loads(rv.data) == RESULT_OK


def test_add_to_filled_server_rack(api_client):
    rv = add_server_to_rack(api_client, 3, 16)
    assert rv.status_code == 422
    assert b'Server rack capacity already reached' in rv.data


def test_illegal_action_with_server_rack(api_client):
    req_data = {
        'action': 'aaaaaaaaaaaaaa'
    }
    rv = api_client.put('/api/v1/serverRacks/{}'.format(3), json=req_data)
    assert rv.status_code == 400
    assert b'Invalid action with server rack' in rv.data


def test_include_deleted_racks(api_client):
    rv = get_all_server_racks(api_client)
    assert rv.status_code == 200
    len1 = len(json.loads(rv.data)['result'])
    rv = get_all_server_racks(api_client, include_deleted=True)
    assert rv.status_code == 200
    len2 = len(json.loads(rv.data)['result'])
    assert len1 < len2
