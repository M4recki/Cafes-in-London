# Test home page


def test_home_page(client):
    """Tests the home page route.

    This test function checks that the home page (/) returns a successful response (status code 200).

    Args:
        client (FlaskClient): The test client for the Flask app.
    """
    response = client.get("/")

    assert response.status_code == 200


# Test register page


def test_incorrect_registration(client, app):
    """Tests the registration page with an incomplete form.

    This test function submits a registration form with an empty password field and checks that the response contains the expected error message.

    Args:
        client (FlaskClient): The test client for the Flask app.
        app (Flask): The Flask app instance.
    """
    response = client.post(
        "/register", data={"name": "test", "email": "test@email.com", "password": ""}
    )

    assert b"This field is required." in response.data


# Test invalid route


def test_invalid_route(client):
    """Tests an invalid route.

    This test function checks that requesting an invalid route (/invalid) returns a 404 Not Found response.

    Args:
        client (FlaskClient): The test client for the Flask app.
    """
    response = client.get("/invalid")

    assert response.status_code == 404


# Test unauthorized path


def test_unauthorized_path(client):
    """Tests an unauthorized path.

    This test function checks that requesting the /add_cafe route (which requires admin authorization) without being logged in returns a 401 Unauthorized response.

    Args:
        client (FlaskClient): The test client for the Flask app.
    """
    response = client.get("/add_cafe")
    assert response.status_code == 401
