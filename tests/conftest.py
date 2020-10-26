import pytest
from flask import Flask
from app.factory import create_app
from app.config import config
from unittest.mock import MagicMock


@pytest.fixture
def mocked_blockchain_apis(mocker):
    """Mocks the return values inside app/blueprints/gateway/__init__.py to make it look like both backends are running.
    Note that the functions of the backends still have to be mocked."""
    apis = [{"api": "bitshares"}, {"api": "bitcoin"}]
    def side_effect():
        return apis.pop(0)
    mock = mocker.patch('requests.get')
    magic_mock = MagicMock()
    mock.return_value = magic_mock
    magic_mock.status_code = 200
    magic_mock.json = side_effect


@pytest.fixture
def client(mocked_blockchain_apis):
    app = Flask(__name__, template_folder="../app/templates")
    app.config.update(config)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
    app = create_app(app)
    return app.test_client()
