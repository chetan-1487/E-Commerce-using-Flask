import pytest
from app.main import createApp
from app.extension import db, bcrypt
from flask_jwt_extended import create_access_token
from app.models.users.user import User


@pytest.fixture(scope="session")
def app():
    app = createApp(test_config=True)

    # Testing overrides
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:chetan@localhost:5432/test"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


# Create a test user
@pytest.fixture()
def create_test_user(db_session):
    pwd = bcrypt.generate_password_hash("Test@123").decode("utf-8")
    user = User(
        "testuser", "test@test.com", pwd,
        "male", "pune", "9999999999", "admin"
    )
    db_session.add(user)
    db_session.commit()
    return user


# Create JWT token cookie for authenticated requests
@pytest.fixture()
def auth_client(client, create_test_user):
    token = create_access_token(
        identity=str(create_test_user.id),
        additional_claims={"email": create_test_user.email, "roles": create_test_user.role}
    )
    client.set_cookie("access_token_cookie", token)
    return client
