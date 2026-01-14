import pytest
import json
from app import app
from io import BytesIO

class TestAPI:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_4_missing_files(self, client):
        """Test 4: Brak plików w żądaniu"""
        response = client.post("/api/przetworz")
        data = json.loads(response.data)

        assert response.status_code == 400
        assert "Error" in data
        print("API odrzuca żądania bez plików")
    
    def test_5_successful_request(self, client):
        """Test 5: Pełne przetwarzanie"""
        with open("test_data/dataset/cut.jpg", "rb") as f1, \
             open("test_data/dataset/z2.jpg", "rb") as f2:

            data = {
                'obraz1': (BytesIO(f1.read()), 'cut.jpg'),
                'obraz2': (BytesIO(f2.read()), 'z2.jpg')
            }

            response = client.post('/api/przetworz',
                                   data = data,
                                   content_type = "multipart/form-data")

        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.data)
            assert "matches" in data
            assert "result"  in data