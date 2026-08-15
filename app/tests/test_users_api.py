def test_register_user_201(anon_client):
    payload = {
        'username': 'naviddev',
        'email': 'naviddev@gmail.com',
        'password': 'naviddev',
        'password_confirm': 'naviddev'
    }
    response = anon_client.post('/users/register', json=payload)
    assert response.status_code == 201


def test_login_invalid_data_response_401(anon_client):
    payload = {
        'username': 'string11',
        'password': 'string1'
    }
    response = anon_client.post('/users/login', json=payload)
    assert response.status_code == 401

    payload = {
        'username': 'string1',
        'password': 'string111'
    }
    assert response.status_code == 401


def test_login_response_200(anon_client):
    payload = {
        'username': 'navid',
        'password': '12345678'
    }
    response = anon_client.post('/users/login', json=payload)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()






