from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger

class NewMessagePage(BasePage):
    """群发信使->新建短信页面"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '发送': (MobileBy.ACCESSIBILITY_ID, "发送"),
        '+号图标': (MobileBy.XPATH, '(//XCUIElementTypeLink)[2]'),
        '否': (MobileBy.ACCESSIBILITY_ID, "否"),
        '关闭': (MobileBy.ACCESSIBILITY_ID, "cc h5 ic close")
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待群发信使->新建短信页面加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["发送"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_add_icon(self):
        """点击+号"""
        self.click_element(self.__class__.__locators["+号图标"])

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def is_exist_text(self, text):
        """是否存在文本"""
        return self.is_text_present(text)

    @TestLogger.log()
    def click_no(self):
        """点击否"""
        if self._is_element_present(self.__class__.__locators["否"]):
            self.click_element(self.__class__.__locators["否"])
