import pytest
from project import create_app, db
from project.models import User




# Pytest fixture to create a app


@pytest.fixture()
def app():
    app = create_app(database_uri="sqlite://")
    
    with app.app_context():
        db.create_all() 
      
    yield app
    

# Pytest fixture to create a client


@pytest.fixture()
def client(app):
    return app.test_client()


# Pytest fixture to create a user


@pytest.fixture()
def new_user():
    user = User(name="XXXXXXXX",  email="XXXXXXXXXXXXXX", password="XXXXXXXXXXXXXX")
    return user