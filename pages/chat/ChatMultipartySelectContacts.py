from appium.webdriver.common.mobileby import MobileBy
import re
import copy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time
from pages.message.Message import MessagePage
from pages.GroupChat import GroupChatPage

class ChatmultipartySelectContacts(BasePage):
    """多方通话 多方视频选择联系人页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '飞信电话': (MobileBy.ACCESSIBILITY_ID, '飞信电话'),
        '问号': (MobileBy.ACCESSIBILITY_ID, 'cc_call_groupcall_profile_ic_question'),
        '呼叫': (MobileBy.IOS_PREDICATE, 'name CONTAINS "呼叫"'),
        '搜索群成员': (MobileBy.IOS_PREDICATE, 'value == "搜索群成员"'),
        '可用时长': (MobileBy.ACCESSIBILITY_ID, '可用时长：立即查询>>'),
        '已选择联系人': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther'),

        '': (MobileBy.ACCESSIBILITY_ID, ''),
        '': (MobileBy.ACCESSIBILITY_ID, ''),

    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待选择联系人页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["搜索群成员"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在选择联系人页面"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["搜索群成员"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def select_one_contact_by_name(self, name):
        """通过名称选择一个联系人"""
        self.click_element((MobileBy.ACCESSIBILITY_ID, '%s' % name))

    @TestLogger.log()
    def click_call(self, element='呼叫'):
        """点击呼叫(如果有和飞信回拨 就挂断电话)"""
        self.click_element(self.__class__.__locators[element])
        time.sleep(2)
        if self.page_should_contain_text2('拒绝'):
            self.click_accessibility_id_attribute_by_name('拒绝')


    @TestLogger.log('判断页面存在元素')
    def is_exist_element(self, locator='呼叫'):
        return self._is_element_present(self.__locators[locator])















