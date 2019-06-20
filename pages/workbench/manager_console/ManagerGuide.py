import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ManagerGuidePage(BasePage):
    """管理员指引首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '管理员指引': (MobileBy.IOS_PREDICATE, 'name=="管理员指引"'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '关闭': (MobileBy.ID, 'cc h5 ic close')
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待管理员指引首页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["管理员指引"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def click_guide_by_name(self, name):
        """点击指引/文本"""
        self.click_name_attribute_by_name(name)

    @TestLogger.log()
    def wait_for_guide_page_load(self, name):
        """等待指引页加载"""
        try:
            self.wait_until(
                timeout=20,
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present(name)
            )
        except:
            raise AssertionError("指引页加载失败")
        return self

