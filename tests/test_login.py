import pytest
import allure


@allure.story('Login Feature')
@allure.title('Login with wrong login/password failed')
def test_login_failure(login_page):
    login_page.navigate()
    login_page.login('invalid_user', 'invalid_password')
    assert login_page.get_error_message() == 'Invalid credentials. Please try again.'


@pytest.mark.parametrize('username, password', [
    ('user', 'user'),
    ('admin', 'admin')
])
@allure.feature('Login')
@allure.story('Login with valid credentials')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Different type of users login with valid credentials')
def test_login_success(login_page,dashboard_page, username, password):
    with allure.step('Open login page'):
        login_page.navigate()
    with allure.step('Enter credentials'):
        login_page.login(username, password)
    with allure.step('User sees the Welcome msg with name'):
        dashboard_page.assert_welcome_message(f"Welcome {username}")
