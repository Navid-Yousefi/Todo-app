from tests.test_api import app


client = TestClient(app)

# def test_register_user_200():
#     payload = {
#         'username': 
#     }


def test_login_response_401():
    payload = {
        'username': 'string11',
        'password': 'string11'
    }
    response = client.post('/users/login', json=payload)
    assert response.status_code == 401


def test_login_response_200():
    payload = {
        'username': 'string1',
        'password': 'string1'
    }
    response = client.post('/users/login', json=payload)
    assert response.status_code == 200
