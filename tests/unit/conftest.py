from unittest import mock

import pytest
from my_fastapi_project.app import get_application


@pytest.fixture
def asgi_app():
    app = mock.Mock(spec=get_application())
    yield app
    del app
