import pytest
from aggregator.index import app 

@pytest.fixture()
def client():
    return app.test_client()

def setup_mock(requests_mock):
    requests_mock.get('http://api1:5000/member_id=1', text='{"deductible":100,"oop_max":5000,"stop_loss":8000}')
    requests_mock.get('http://api2:5000/member_id=1', text='{"deductible":200,"oop_max":4000,"stop_loss":6000}')
    requests_mock.get('http://api3:5000/member_id=1', text='{"deductible":300,"oop_max":3000,"stop_loss":7000}')

def test_happy_path_min(client, requests_mock):
    setup_mock(requests_mock)
    response = client.get("/member_id=1&strategy=min")
    assert response.status_code == 200
    assert '{"deductible":100,"oop_max":3000,"stop_loss":6000}\n' == response.text

def test_happy_path_mean(client, requests_mock):
    setup_mock(requests_mock)    
    response = client.get("/member_id=1&strategy=mean")
    assert response.status_code == 200
    assert '{"deductible":200,"oop_max":4000,"stop_loss":7000}\n' == response.text

def test_no_upstream(client, requests_mock):
    response = client.get("/member_id=1&strategy=mean")
    assert response.status_code == 500
    assert "Something's wrong" in response.text

def test_bad_strategy(client):
    response = client.get("/member_id=1&strategy=foo")
    assert response.status_code == 400
    assert "foo is unsupported!" == response.text
