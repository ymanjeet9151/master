from __future__ import absolute_import, unicode_literals
from .keywords import PageObjectLibraryKeywords
from .pageobject import PageObject
from .version import __version__


class PageObjectLibrary(PageObjectLibraryKeywords):
    """
    *PageObjectLibrary* is a lightweight library which supports using
    the page object pattern with
    [http://robotframework.org/SeleniumLibrary/doc/SeleniumLibrary.html|SeleniumLibrary].
    This library does not replace SeleniumLibrary; rather, it
    provides a framework around which to use SeleniumLibrary and the
    lower-level [http://selenium-python.readthedocs.org/|Python
    bindings to Selenium]

    This library provides the following keywords:

    | =Keyword Name=             | =Synopsis= |
    | Go to page                 | Goes to the given page in the browser |
    | The current page should be | Assert that the given page is displayed in the browser |

    PageObjectLibrary provides a PageObject class which should be used
    as the base class for other page objects. By inheriting from this
    class your keywords have access to the following pre-defined
    attributes and methods:

    | =Attribute/method=  | =Description=                             |
    | ``self.se2lib``  | A reference to the SeleniumLibrary instance     |
    | ``self.browser`` | A reference to the currently open browser        |
    | ``self.locator`` | A wrapper around the ``_locators`` dictionary        |
    | ``self.logger``  | A reference to the ``robot.api.logger`` instance     |
    | ``self._wait_for_page_refresh()`` | a context manager for doing work that causes a page refresh   |

    = Using SeleniumLibrary Keywords =

    Within your keywords you have access to the full power of
    SeleniumLibrary. You can use ``self.se2lib`` to access the
    library keywords. The following example shows how to call the
    ``Capture Page Screenshot`` keyword:

    | self.se2lib.capture_page_screenshot()

    = Using Selenium Methods =

    The attribute ``self.browser`` is a reference to a Selenium
    webdriver object. With this reference you can call any of the
    standard Selenium methods provided by the Selenium library. The
    following example shows how to find all link elements on a page:

    | elements = self.browser,find_elements_by_tag_name("a")

    = Creating Page Object Classes =

    Page objects should inherit from PageObjectLibrary.PageObject. At a minimum,
    the class should define the following attributes:

    = Page Objects are Normal Robot Libraries =

    All rules that apply to keyword libraries applies to page objects. For
    example, the libraries must be on ``PYTHONPATH``. You may also want to define
    ``ROBOT_LIBRARY_SCOPE``. Also, the filename and the classname must be identical (minus
    the ``.py`` suffix on the file).

    = Locators =

    When writing multiple keywords for a page, you often use the same locators in
    many places. PageObject allows you to define your locators in a dictionary,
    but them use them with a more convenient dot notation.

    To define locators, create a dictionary named ``_locators``. You can then access
    the locators via dot notation within your keywords as ``self.locator.<name>``. The
    ``_locators`` dictionary may have nested dictionaries.

    = Waiting for a Page to be Ready =

    One difficulty with writing Selenium tests is knowing when a page has refreshed.
    PageObject provides a context manager named ``_wait_for_page_refresh()`` which can
    be used to wrap a command that should result in a page refresh. It will get a
    reference to the DOM, run the body of the context manager, and then wait for the
    DOM to change before returning.

    = Example Page Object Definition =

    | from PageObjectLibrary import PageObject
    | from robot.libraries.BuiltIn import BuiltIn
    |
    | class LoginPage(PageObject):
    |    |
    |    _locators = {
    |        "username": "id=id_username",
    |        "password": "id=id_password",
    |        "submit_button": "id=id_submit",
    |    }
    |
    |    def login_as_a_normal_user(self):
    |        username = BuiltIn().get_variable_value("${USERNAME}"}
    |        password = BuiltIn().get_variable_value("${PASSWORD}"}
    |        self.se2lib.input_text(self.locator.username, username)
    |        self.se2lib.input_text(self.locator.password, password)
    |
    |        with self._wait_for_page_refresh():
    |            self.click_the_submit_button()

    = Using the Page Object in a Test =

    To use the above page object in a test, you must make sure that
    Robot can import it, just like with any other keyword
    library. When you use the keyword `Go to page`, the keyword will
    automatically load the keyword library and put it at the front of
    the Robot Framework library search order (see
    [http://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Set%20Library%20Search%20Order|Set Library Search Order])

    In the following example it is assumed there is a second page
    object named ``DashboardPage`` which the browser is expected to go to
    if login is successful.

    | ``*** Settings ***``
    | Library           PageObjectLibrary
    | Library           SeleniumLibrary
    | Suite Setup       Open browser        http://www.example.com
    | Suite Teardown    Close all browsers
    |
    | ``*** Test Cases ***``
    | Log in to the application
    |     Go to page                   LoginPage
    |     Log in as a normal user
    |     The current page should be   DashboardPage

    """
    # scope limited to test_suite of robot framework, can be set to global in case required
    ROBOT_LIBRARY_SCOPE = "TEST SUITE"
