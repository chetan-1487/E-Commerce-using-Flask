def test_signup_success(client, db_session):
    response = client.post("/signup", data={
        "username": "Chetan123",
        "email": "test1@test.com",
        "password": "Test@123",
        "gender": "M",
        "address": "pune",
        "mobile_no": "9999999",
        "role": ["admin"]
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Account created successfully!" in response.data


def test_signup_duplicate_email(client, create_test_user):
    response = client.post("/signup", data={
        "username": "Chetan123",
        "email": "test1@test.com",   # already exists
        "password": "Test@123",
        "gender": "M",
        "address": "pune",
        "mobile_no": "9999999",
        "role": ["admin"]
    })

    assert b"user already exist" in response.data

def test_login_success(client, create_test_user):
    response = client.post("/login", data={
        "email": "test1@test.com",
        "password": "Test@123"
    })

    # Should redirect to /all
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/all")

def test_login_wrong_password(client, create_test_user):
    resp = client.post("/login", data={
        "email": "test@test.com",
        "password": "Wrong123"
    })

    assert b"Incorrect email or password" in resp.data

# def test_login_user_not_exist(client):
#     resp = client.post("/login", data={
#         "email": "no@test.com",
#         "password": "Test@123"
#     })

#     assert resp.status_code == 302
#     assert resp.headers["Location"].endswith("/signup")

# def test_logout(client):
#     resp = client.get("/logout")
#     assert resp.status_code == 302
#     assert resp.headers["Location"].endswith("/login")

#     # cookie should be deleted
#     assert "access_token_cookie=;" in resp.headers.get("Set-Cookie")

# def test_forgot_password_success(client, create_test_user):
#     resp = client.post("/forgot-password", data={
#         "email": "test@test.com",
#         "current_password": "Test@123",
#         "new_password": "NewPass@123",
#         "confirm_password": "NewPass@123"
#     }, follow_redirects=True)

#     assert b"new password generated successfully.." in resp.data

# def test_forgot_wrong_old_password(client, create_test_user):
#     resp = client.post("/forgot-password", data={
#         "email": "test@test.com",
#         "current_password": "WrongPass",
#         "new_password": "New@1234",
#         "confirm_password": "New@1234"
#     })

#     assert b"signup" in resp.data or b"doesnot exist" not in resp.data

# def test_all_users_authorized(auth_client):
#     resp = auth_client.get("/all")
#     assert resp.status_code == 200


# from flask_jwt_extended import create_access_token

# def test_all_users_unauthorized(client, create_test_user):
#     # Create non-admin token
#     token = create_access_token(
#         identity=str(create_test_user.id),
#         additional_claims={"email": "test@test.com", "roles": "user"}
#     )
#     client.set_cookie("access_token_cookie", token)

#     resp = client.get("/all", follow_redirects=True)

#     assert b"Permission denied. only admin can access" in resp.data


# def test_refresh_token(auth_client):
#     resp = auth_client.get("/refresh-token")

#     assert resp.status_code == 200
#     assert b"all" in resp.data or resp.status_code == 302
