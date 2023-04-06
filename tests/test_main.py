import requests

api_url = "http://localhost:8000"


def test_healthCheck():
    response = requests.get(f'{api_url}/__health_check')
    assert response.status_code == 200



