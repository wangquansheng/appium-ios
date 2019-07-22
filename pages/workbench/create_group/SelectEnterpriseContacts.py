from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SelectEnterpriseContactsPage(BasePage):
    """创建群->选择联系人 页面"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterPriseContactSelectActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back'),
        '确定': (MobileBy.IOS_PREDICATE, 'name contains "确定"'),
        '选择联系人': (MobileBy.ACCESSIBILITY_ID, '选择联系人'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待创建群->选择联系人 页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择联系人"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_contacts_by_name(self, name):
        """选择指定联系人"""
        self.click_accessibility_id_attribute_by_name(name)

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])
