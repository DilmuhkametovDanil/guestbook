import pytest
from app import app
from database import init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

# Задание 1. Тестирование доступности главной страницы (Статус 200)
def test_main_page_status_code(client):
    response = client.get('/')
    assert response.status_code == 200

# Задание 2. Тестирование защищенных страниц и редиректов (Статус 302)
def test_admin_pages_redirect(client):
    response = client.get('/delete/1')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
