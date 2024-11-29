from django.test import TestCase

# Create your tests here.
@pytest.mark.django_db
def test_admin_create_product():
    client = Client()
    client.login(username='admin', password='password')  # Replace with actual admin credentials
    response = client.post('/admin/products/create/', {
        'name': 'New Product', 'description': 'Description of new product', 'price': 100.0
    })
    assert response.status_code == 200
    assert 'Product created successfully' in response.content.decode()

@pytest.mark.django_db
def test_admin_delete_product():
    client = Client()
    client.login(username='admin', password='password')
    response = client.post('/admin/products/delete/1/')
    assert response.status_code == 200
    assert 'Product deleted successfully' in response.content.decode()
