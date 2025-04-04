from playwright.sync_api import Playwright, sync_playwright, expect, Page, Route
import pytest
import os

@pytest.fixture
def browser_fixture():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        page.close()
        browser.close()

#size of the browser
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }

#set up cookies
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": {
            "cookies": [
                {
                    "name": "stepik",
                    "value": "sd4fFfv!x_cfcstepik",
                    "url": "https://www.wikipedia.org/"  # put needed URL
                },
            ]
        },
    }


def test_add_todo(page):
    page.goto("https://demo.playwright.dev/todomvc/#/")
    page.get_by_placeholder("What needs to be done?").click()
    page.get_by_placeholder("What needs to be done?").fill("Создать первый сценарий playwright")
    page.get_by_placeholder("What needs to be done?").press("Enter")

def test_loc(page):
    page.goto('https://zimaev.github.io/text_input/')
    page.get_by_label("Email address").fill("qa@example.com")
    page.get_by_title("username").fill("Anton")
    page.get_by_placeholder('password').fill("secret")
    page.get_by_role('checkbox').click()

def test_locator_and(page):
    page.goto("https://zimaev.github.io/locatorand/")
    selector = page.get_by_role("button", name="Sing up").and_(page.get_by_title("Sing up today"))
    selector.click()

def test_checkbox(page):
    page.goto('https://zimaev.github.io/checks-radios/')
    checkboxes = page.locator("input")
    for checkbox in checkboxes.all():
        checkbox.check()

def test_login(page):
    page.goto('https://www.wikipedia.org/')
    page.locator("#searchInput").fill("playwright software")
    page.locator("#searchInput").clear()
    page.locator("#searchInput").type("playwright software")
    page.locator("#searchInput").clear()
    page.locator("#searchInput").press_sequentially("world", delay=100)
    #functional keys
    page.locator("#searchInput").press('Delete')

#select single option
def test_select(page):
    page.goto('https://zimaev.github.io/select/')
    page.select_option('#floatingSelect', value="3")
    page.select_option('#floatingSelect', index=1)
    page.select_option('#floatingSelect', label="Нашел и завел bug")

#select multiple options
def test_select_multiple(page):
    page.goto('https://zimaev.github.io/select/')
    page.select_option('#skills', value=["playwright", "python"])

#drag and drop
def test_drag_and_drop(page):
    page.goto('https://zimaev.github.io/draganddrop/')
    page.drag_and_drop("#drag", "#drop")

def test_dialogs(page):
    page.goto("https://zimaev.github.io/dialog/")
    page.get_by_text("Диалог Alert").click()
    page.get_by_text("Диалог Confirmation").click()
    page.get_by_text("Диалог Prompt").click()

def test_dialogs_confirm(page):
    page.goto("https://zimaev.github.io/dialog/")
    page.on("dialog", lambda dialog: dialog.accept()) #press OK
    page.get_by_text("Диалог Confirmation").click()

def test_dialogs_dismiss(page):
    page.goto("https://zimaev.github.io/dialog/")
    page.on("dialog", lambda dialog: dialog.dismiss()) # press Cancel
    page.get_by_text("Диалог Confirmation").click()

def test_upload_file(page):
    page.goto('https://zimaev.github.io/upload/')
    page.set_input_files("#formFile", "hello.txt")
    page.locator("#file-submit").click()

def test_upload_file2(page):
    page.goto('https://zimaev.github.io/upload/')
    page.on("filechooser", lambda file_chooser: file_chooser.set_files("hello.txt"))
    page.locator("#formFile").click()

def test_upload_file3(page):
    page.goto('https://zimaev.github.io/upload/')
    with page.expect_file_chooser() as fc_info:
        page.locator("#formFile").click()
    file_chooser = fc_info.value
    file_chooser.set_files("hello.txt")

def test_download(page):
    page.goto("https://demoqa.com/upload-download")

    with page.expect_download() as download_info:
        page.locator("a:has-text(\"Download\")").click()

    download = download_info.value
    file_name = download.suggested_filename
    destination_folder_path = "./data/"
    download.save_as(os.path.join("/Users/juliacardenas/Downloads", 'Hello.txt'))

#return an array of values for all matching elements.
def test_get_text(page):
    page.goto('https://zimaev.github.io/table/')
    row = page.locator("tr")
    print(row.all_inner_texts()) #innerText can read styles and does not return the content of hidden elements
    print(row.all_text_contents()) #textContent gets the content of all elements, including <script> and <style>
    # element = page.locator('a:has-text("script")')
    # print(element.inner_html()) # HTML-code of the element/s

def test_screenshot(page):
    page.goto("https://demoqa.com/upload-download")
    page.screenshot(path="full_page.png", full_page=True) #format .png
    page.screenshot(path="example.jpeg", type="jpeg") #format .jpeg
    page.screenshot(path="example.jpeg", type="jpeg", quality=80)  # number can be from 0 to 100
    page.screenshot(path="clipped_image.png", clip={"x": 50, "y": 0, "width": 400, "height": 300}) # area for screenshot
    page.screenshot(path="transparent_background.png", omit_background=True) #Allows you to remove the background of an image


def test_new_tab(page):
    page.goto("https://zimaev.github.io/tabs/")
    with page.context.expect_page() as tab:
        page.get_by_text("Переход к Dashboard").click()

    new_tab = tab.value
    assert new_tab.url == "https://zimaev.github.io/tabs/dashboard/index.html?"
    sign_out = new_tab.locator('.nav-link', has_text='Sign out')
    assert sign_out.is_visible()

def test_verify_task_form(page):
    page.goto("https://demo.playwright.dev/todomvc/#/")
    expect(page).to_have_url("https://demo.playwright.dev/todomvc/#/")
    input_field = page.get_by_placeholder("What needs to be done?")
    expect(input_field).to_be_empty()
    input_field.fill("Finish course  playwright")
    input_field.press('Enter')
    page.pause()
    input_field.fill("Add to the resume playwright skills")
    input_field.press('Enter')
    todo_item = page.get_by_test_id('todo-item')
    expect(todo_item).to_have_count(2)
    todo_item.get_by_role('checkbox').nth(0).click()
    expect(todo_item.nth(0)).to_have_class('completed')

# Monitoring network requests
def test_listen_network(page):
    page.on("request", lambda request: print(">>", request.method, request.url))
    page.on("response", lambda response: print("<<", response.status, response.url))
    page.goto('https://osinit.ru/')


def test_network(page):
    page.route("**/register", lambda route: route.continue_(post_data='{"email": "user","password": "secret"}'))
    page.goto('https://reqres.in/')
    page.get_by_text(' Register - successful ').click()

def test_mock_tags(page):
    page.route("**/api/tags", lambda route: route.fulfill(path="data.json"))
    page.goto('https://demo.realworld.io/')

def test_intercepted(page):
    def handle_route(route: Route):
        response = route.fetch()
        json = response.json()
        json["tags"] = ["open", "solutions"]
        route.fulfill(json=json)

    page.route("**/api/tags", handle_route)

    page.goto("https://demo.realworld.io/")
    sidebar = page.locator('css=div.sidebar')
    expect(sidebar.get_by_role('link')).to_contain_text(["open", "solutions"])
