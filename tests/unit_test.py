# Test home page


def test_home_page(client):
    response = client.get("/")
    
    assert response.status_code == 200


# Test register page


def test_incorrect_registration(client, app):
    response = client.post(
        "/register", data={"name": "test", "email": "test@email.com", "password": ""}
    )

    assert b"This field is required." in response.data
