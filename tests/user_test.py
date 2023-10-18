# Test example user

    
def test_login_client(new_user):
    assert new_user.name == "XXXXXXXX"
    assert new_user.email == "XXXXXXXXXXXXXX"
    assert new_user.password == "XXXXXXXXXXXXXX"
    

# Test login user

    
def test_login_user(client):
    with client:
        client.post("register", data={"name": "Julian", "email": "julian@email.com", "password": "Julian123"})
        client.post("login", data={"email": "julian@email.com", "password": "Julian123"})
        response = client.get("/logout")
        assert response.status_code == 200
        assert b"You have been logged out" in response.data
