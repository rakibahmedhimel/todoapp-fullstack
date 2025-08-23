from .utils import *
from fastapi import status
from ..routers.admin import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get('/admin/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": test_todo.id,
        "title": test_todo.title,
        "description": test_todo.description,
        "priority": test_todo.priority,
        "complete": test_todo.complete,
        "owner_id": test_todo.owner_id
    }]

def delete_todo_admin_authenticated(test_todo):
    response = client.delete('/admin/todos/1')
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def delete_todo_not_found_admin(test_todo):
    response = client.delete('/admin/todos/999')
    assert response.status_code == 404
    assert response.json() == {'detail' : 'Not Found'}