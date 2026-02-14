from anny.core.exceptions import AnnyError, APIError, AuthError


def test_anny_error_default_message():
    err = AnnyError()
    assert str(err) == "An error occurred"


def test_anny_error_custom_message():
    err = AnnyError("custom")
    assert str(err) == "custom"


def test_auth_error_is_anny_error():
    err = AuthError()
    assert isinstance(err, AnnyError)
    assert str(err) == "Authentication failed"


def test_api_error_is_anny_error():
    err = APIError(message="GA4 failed", service="ga4")
    assert isinstance(err, AnnyError)
    assert err.service == "ga4"
    assert str(err) == "GA4 failed"


def test_exception_hierarchy():
    with_catch = False
    try:
        raise APIError("test")
    except AnnyError:
        with_catch = True
    assert with_catch
