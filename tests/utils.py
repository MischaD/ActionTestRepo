from unittest.mock import MagicMock


def setup_authentication(test_client, username="oi", password="oi"):
    """setup get and post urls that automatically add authentication to test_client.
    Instead of using test_client.get(body, authentication_info) now use: test_client.get_authorized(body)
    """
    create_test_client_user(test_client, username="test_with_token", password="test_with_token")
    user = test_client.post("/token", data=dict(username=username, password=password)).json()
    headers = {"Authorization": f"{user['token_type']} {user['access_token']}"}

    post = test_client.post
    get = test_client.get

    def post_with_authorization(*args, **kwargs):
        return post(*args, headers=headers, **kwargs)

    def get_with_authorization(*args, **kwargs):
        return get(*args, headers=headers, **kwargs)

    test_client.post_authorized = post_with_authorization
    test_client.get_authorized = get_with_authorization


def create_test_client_user(test_client, username, password):
    test_client.post(f"/create_user/?username={username}&password={password}")


def mocked_json_response(method, *arg, **kwargs):
    mock = MagicMock()
    mock.json = lambda: {"resp": "42"}
    return mock
