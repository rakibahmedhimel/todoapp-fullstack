from .utils import *
from ..routers.todos import get_current_user, get_db

app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todos")  
    assert response.status_code == 200
    assert response.json() == [{
        "id": test_todo.id,
        "title": test_todo.title,
        "description": test_todo.description,
        "priority": test_todo.priority,
        "complete": test_todo.complete,
        "owner_id": test_todo.owner_id
    }]

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")  
    assert response.status_code == 200
    assert response.json() == {
        "id": test_todo.id,
        "title": test_todo.title,
        "description": test_todo.description,
        "priority": test_todo.priority,
        "complete": test_todo.complete,
        "owner_id": test_todo.owner_id
    }

def test_read_one_authenticated_not_found():
    response = client.get("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail' : 'Task Not Found'}

def test_create_todo(test_todo):
    request_todo = {
        'title': 'New Title!',
        'description': 'New description',
        'priority': 5,
        'complete': False,
    }
    response = client.post('/todos/todo', json=request_todo)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_todo.get('title')
    assert model.description == request_todo.get('description')
    assert model.priority == request_todo.get('priority')
    assert model.complete == request_todo.get('complete')

def test_update_todo(test_todo):
    request_data = {
        'title': 'New Title again!',
        'description': 'New description again',
        'priority': 3,
        'complete': False,
    }
    response = client.put("/todos/update_todo/1", json=request_data)
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'New Title again!'


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'New Title again!',
        'description': 'New description again',
        'priority': 3,
        'complete': False,
    }
    response = client.put("/todos/update_todo/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_delete_todo(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None



def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task Not Found'}