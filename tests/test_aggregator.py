import pytest
from aggregator import create_app

@pytest.fixture
def app():    
    return create_app()

@pytest.fixture
def client(app):    
    return app.test_client()

@pytest.mark.parametrize(
    "strategy, expect",
    [
        ("mean", '{"deductible":200,"oop_max":4000,"stop_loss":8000}\n'),
        ("median", '{"deductible":200,"oop_max":4000,"stop_loss":8000}\n'),
        ("min", '{"deductible":100,"oop_max":3000,"stop_loss":7000}\n'),
        ("max", '{"deductible":300,"oop_max":5000,"stop_loss":9000}\n')
    ]
)

def test_happy_path(strategy, expect, client, httpx_mock):
    httpx_mock.add_response(url="http://api1:5000/member_id=1", text='{"deductible":100,"oop_max":5000,"stop_loss":8000}')
    httpx_mock.add_response(url="http://api2:5000/member_id=1", text='{"deductible":200,"oop_max":4000,"stop_loss":9000}')
    httpx_mock.add_response(url="http://api3:5000/member_id=1", text='{"deductible":300,"oop_max":3000,"stop_loss":7000}')
    response = client.get(f"/member_id=1&strategy={strategy}")
    assert response.status_code == 200  # nosec B101
    assert expect == response.text  # nosec B101

def test_bad_strategy(client):
    response = client.get("/member_id=1&strategy=foo")
    assert response.status_code == 400  # nosec B101
    assert "foo is unsupported!" == response.text  # nosec B101

def test_no_upstream(client, httpx_mock):
    httpx_mock.add_response()
    response = client.get("/member_id=1&strategy=mean")
    assert response.status_code == 500  # nosec B101
    assert "Something's wrong" in response.text # nosec B101

def test_no_upstream_debug(app, client, httpx_mock):
    app.debug = True
    httpx_mock.add_response()
    response = client.get("/member_id=1&strategy=mean")
    assert response.status_code == 500  # nosec B101
    assert "Something's wrong:" in response.text  # nosec B101
