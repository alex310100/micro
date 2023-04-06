import requests

api_url = 'http://localhost:8000'


class TestDocuments():
    def test_get_empty_docs(self):
        response = requests.get(f'{api_url}/v1/docs')
        assert response.status_code == 200
        assert len(response.json()) == 2
