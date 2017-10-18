import numpy as np
import pytest


def pytest_addoption(parser):
    parser.addoption("--cmdopt", action="store", default="test", help="option: 'test' or \
    'generate'. Only use 'generate' if you've changed the tests and need to update the expected \
    output!")


@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")


@pytest.fixture(scope="module")
def data_gen():
    np.random.seed(111)
    data1 = np.random.normal(size=1000)
    data2 = np.random.normal(2, 1, size=1000)
    weights = np.random.uniform(1, 2, size=1000)
    return data1, data2, weights
