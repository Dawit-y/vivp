from rest_framework.test import APIClient
from rest_framework import status
import pytest

client = APIClient()

@pytest.mark.django_db
class TestCreateCollection:
    def test_applicant_create(self):
        #AAA = Arrange, act, assert
        response = client.post("/applicants/", {
   
            "first_name": "Test",
            "last_name": "Tester",
            "email": "test@tester.com",
            "age": 20,
            "gender": "female",
            "phone_number": "+251955356443",
            "avatar": "http://127.0.0.1:8000/media/avatars/images_15.jpeg",
            "resume": "http://127.0.0.1:8000/media/resumes/gitignore_for_django_DqmR7r0.txt",
            "portfolio_link": "https://www.kidistyimer.com",
            "date_joined": "26 Feb 2024",
            "is_active": True
        })
        assert response.status_code == status.HTTP_201_CREATED