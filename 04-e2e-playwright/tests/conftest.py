import pytest


BASE_URL = "https://automationintesting.online"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL
