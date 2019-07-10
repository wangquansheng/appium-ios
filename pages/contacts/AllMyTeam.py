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
        "": (MobileBy.ACCESSIBILITY_ID, ''),
        "": (MobileBy.ACCESSIBILITY_ID, ''),

    }

    @TestLogger.log()
    def click_back(self):
        """切换到标签页：我"""
        self.click_element(self.__locators['返回'])
