import pytest

def test_route_users(client, app):
    response = client.get(
        '%s/users/1/1' % pytest.BASE_API, 
        headers={
            'Authorization': 'Bearer %s' % pytest.OAUTH_TOKEN
        },
        data={})
    assert response.status_code == 200
    assert len(response.json) == 1
    assert 'username' in response.json[0]
    user_id = response.json[0]['id_user']
    print('  - user_id:%s' % user_id)
    
    response = client.get(
        '%s/users/%s' % (pytest.BASE_API, user_id), 
        headers={
            'Authorization': 'Bearer %s' % pytest.OAUTH_TOKEN
        },
        data={})
    assert response.status_code == 200
    assert 'username' in response.json
    print('  - username:%s' % response.json['username'])