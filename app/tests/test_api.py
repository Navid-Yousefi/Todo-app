def test_register_user_200(anon_client):
    payload = {
        'username': 'naviddev',
        'email': 'naviddev@gmail.com',
        'password': 'naviddev',
        'password_confirm': 'naviddev'
    }
    response = anon_client.post('/users/register', json=payload)
    assert response.status_code == 201


def test_login_response_401(anon_client):
    payload = {
        'username': 'string11',
        'password': 'string11'
    }
    response = anon_client.post('/users/login', json=payload)
    assert response.status_code == 401


def test_login_response_200(anon_client):
    payload = {
        'username': 'naviddev',
        'password': 'naviddev'
    }
    response = anon_client.post('/users/login', json=payload)
    assert response.status_code == 200
