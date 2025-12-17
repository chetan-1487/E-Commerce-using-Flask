from app.models.users.user import User
from app.extension import db, bcrypt


#--------------------signup-----------------

def test_signup_success(client):
    payload = {
        "username": "Chetan123",
        "email": "test@example.com",
        "password": "Password@123",
        "gender": "Male",
        "address": "Delhi",
        "mobile_no": "99999999",
        "role": ["user"]
    }

    response = client.post("/signup", json=payload)

    assert response.status_code == 200
    data = response.get_json()

    assert data["message"] == "User account created successfully."
    assert data["user"]["email"] == "test@example.com"

    user = User.query.filter_by(email="test@example.com").first()
    assert user is not None
    assert user.username == "Chetan123"


def test_signup_existing_user(client):
    
    user = User(
        username="OldUser",
        email="old@example.com",
        password=bcrypt.generate_password_hash("Password@123").decode("utf-8"),
        gender="Male",
        address="India",
        mobile_no="8888888888",
        role=["user"]
    )
    db.session.add(user)
    db.session.commit()

    response = client.post("/signup", json={
        "username": "Anything",
        "email": "old@example.com",
        "password": "Password@123",
        "gender": "Male",
        "address": "Delhi",
        "mobile_no": "1111111111",
        "role": ["user"]
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "user already exist."


def test_signup_invalid_username(client):
    response = client.post("/signup", json={
        "username": "!!!@@@#",          
        "email": "valid@example.com",
        "password": "Password@123",
        "gender": "Male",
        "address": "Delhi",
        "mobile_no": "9999999999",
        "role": ["user"]
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "username must be alphanumeric.."


def test_signup_invalid_password(client):
    response = client.post("/signup", json={
        "username": "ValidUser123",
        "email": "valid@pass.com",
        "password": "weakpass",         
        "gender": "Male",
        "address": "Delhi",
        "mobile_no": "99999999",
        "role": ["user"]
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "password must have one lowercase, one uppercase, one digit, one special_character, length of 8"


def test_login_success(client):
    payload={
        "email":"test@example.com",
        "password":"Password@123"
    }

    response = client.post("/login", json=payload)
    assert response.status == 200
    data = response.get_json()

#-------------------login-------------------

def create_test_user():
    hashed = bcrypt.generate_password_hash("password123").decode("utf-8")
    user = User(
        username="tester",
        email="test@example.com",
        password=hashed,
        gender="Male",
        address="India",
        mobile_no="9999999999",
        role="user"
    )
    db.session.add(user)
    db.session.commit()
    return user

def test_login_success(client):
    create_test_user()

    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.get_json()

    assert data["message"] == "Login successful"
    assert "access_token" in data["tokens"]
    assert "refresh_token" in data["tokens"]

    # cookies must be set
    cookies = response.headers.getlist("Set-Cookie")
    assert any("access_token_cookie" in c for c in cookies)
    assert any("refresh_token_cookie" in c for c in cookies)

def test_login_user_not_exist(client):

    response = client.post("/login", json={
        "email": "wrong@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "user not exist"

def test_login_wrong_password(client):
    create_test_user()

    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "email and password is incorrect."
