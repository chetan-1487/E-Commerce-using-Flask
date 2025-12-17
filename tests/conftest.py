import pytest
from app.main import createApp
from app.extension import db

@pytest.fixture
def client():
    app = createApp(testing=True)

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:chetan@localhost:5432/test"
    app.config["WTF_CSRF_ENABLED"] = False

    ctx = app.app_context()
    ctx.push()

    db.drop_all()
    db.create_all()

    yield app.test_client()

    db.session.remove()
    db.drop_all()
    ctx.pop()
