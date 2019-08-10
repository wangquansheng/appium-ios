from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec

from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage
import time
from pages.contacts.Contacts import ContactsPage


class AllMyTeamPage(BasePage):
    """全部团队"""

    __locators = {
        "返回": (MobileBy.ACCESSIBILITY_ID, 'back'),
        "搜索团队通讯录": (MobileBy.IOS_PREDICATE, 'value == "搜索团队通讯录"'),
        '标题': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="全部团队"]'),
        '输入关键字快速搜索': (MobileBy.XPATH, '//XCUIElementTypeSearchField[@name="输入关键字快速搜索"]'),
        "键盘": (MobileBy.XPATH, '//XCUIElementTypeButton[@name="Search"]'),
        'X': (MobileBy.XPATH, '//*[@name="cc contacts delete pressed"]'),
        '无搜索结果': (MobileBy.XPATH, '//*[@name="cc_conact_empty_member"]'),
        "": (MobileBy.ACCESSIBILITY_ID, ''),

    }

    @TestLogger.log()
    def click_back(self):
        """通讯录首页"""
        self.click_element(self.__locators['返回'])

    @TestLogger.log()
    def click_clear(self):
        """点击清除"""
        self.click_element(self.__locators['X'])

    @TestLogger.log()
    def click_search(self):
        """点击搜索"""
        self.click_element(self.__locators['搜索团队通讯录'])

    @TestLogger.log()
    def input_message(self, content):
        """输入搜索团队通讯录"""
        self.input_text(self.__locators['输入关键字快速搜索'], content)

    @TestLogger.log()
    def input_message_text(self, content):
        """输入搜索团队通讯录"""
        self.input_text(self.__locators['搜索团队通讯录'], content)

    @TestLogger.log()
    def is_element_present_title(self):
        """是否存在标题全部团队"""
        return self._is_element_present(self.__class__.__locators['标题'])

    @TestLogger.log()
    def is_element_present_default_prompt(self):
        """搜索框默认提示语修改为：输入关键字快速搜索"""
        return self._is_element_present(self.__class__.__locators['输入关键字快速搜索'])

    @TestLogger.log()
    def is_element_present_key(self):
        """是否显示键盘"""
        return self._is_element_present(self.__class__.__locators['键盘'])

    @TestLogger.log()
    def is_element_present_clear(self):
        """是否显示X按钮"""
        return self._is_element_present(self.__class__.__locators['X'])

    @TestLogger.log()
    def click_coordinate(self):
        """点击坐标"""
        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        x = 0.5 * width
        y = 0.5 * height
        self.driver.execute_script("mobile: tap", {"y": y, "x": x, "duration": 50})

    @TestLogger.log()
    def select_one_team_by_name(self, name):
        """选择一个团队"""
        self.click_element((MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="%s"]' % name))

