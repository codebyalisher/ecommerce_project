from django.test import TestCase

# Create your tests here.
import pytest
import requests
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
def test_fetch_products():
    client = Client()
    # Mock response from FastAPI
    response = client.get(reverse('fetch_products'))
    assert response.status_code == 200
    assert "products" in response.context

@pytest.mark.django_db
def test_fetch_products_error():
    # Mock a failed response
    client = Client()
    response = client.get(reverse('fetch_products'))
    assert response.status_code == 400
    assert "error" in response.json()
