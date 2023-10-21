# Test example user

    
def test_login_client(new_user):
    assert new_user.name == "XXXXXXXX"
    assert new_user.email == "XXXXXXXXXXXXXX"
    assert new_user.password == "XXXXXXXXXXXXXX"
    

# Test login user

    
def test_login_user(client):
    response = client.post("login", data={"email": "julian@email.com", "password": "Julian123"})
    assert response.status_code == 200


# Test unauthorized path
def test_unauthorized_path(client):
    response = client.get("/add_cafe")
    assert response.status_code == 401