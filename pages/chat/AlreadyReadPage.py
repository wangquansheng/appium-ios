from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class AlreadyReadDynamic(BasePage):
    """已读动态页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.EditGroupPageActivity'

    __locators = {
        '已读动态': (MobileBy.IOS_PREDICATE, 'name == "已读动态"'),
        '已读': (MobileBy.XPATH, "//XCUIElementTypeStaticText[contains(@name,'已读')][1]"),
        '未读': (MobileBy.IOS_PREDICATE, 'name CONTAINS "未读"'),
        '': (MobileBy.ACCESSIBILITY_ID, ''),
        '': (MobileBy.ACCESSIBILITY_ID, ''),
    }


    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在已读动态"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["已读动态"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def select_one_contact_by_name(self, name):
        """通过名称选择一个联系人"""
        self.click_element((MobileBy.ACCESSIBILITY_ID, '%s' % name))

    @TestLogger.log("点击未读按钮")
    def click_not_read(self):
        """点击未读按钮"""
        self.click_element(self.__class__.__locators['未读'])

    @TestLogger.log("点击未读按钮")
    def click_not_read_contact_first(self):
        """点击未读联系人"""
        locator = (MobileBy.XPATH, '//XCUIElementTypeOther[@name="已读动态"]/XCUIElementTypeImage[1]')
        # els = self.get_elements(locator)
        # els[-1].click()
        self.click_element(locator)

