import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatGroupSMSExpensesPage(BasePage):
    """欢迎使用群短信页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {
        '以后再说': (MobileBy.XPATH, '//*[@name="以后再说"]'),
        '确定': (MobileBy.IOS_PREDICATE, 'name CONTAINS "确定"'),
        '欢迎使用群短信！': (MobileBy.XPATH, '//*[@name="欢迎使用群短信！"]'),
        "返回": (MobileBy.ACCESSIBILITY_ID, 'back'),
        '说点什么': (MobileBy.IOS_PREDICATE, 'value == "说点什么......"'),
        '收件人': (MobileBy.XPATH, '//*[@name="收件人："]'),
        '群成员列表': (MobileBy.XPATH, '(//XCUIElementTypeButton)[1]'),
        '搜索成员': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextField"'),
        '选择群成员_确定': (MobileBy.IOS_PREDICATE, 'name CONTAINS "确定"'),
        '全选': (MobileBy.XPATH, '//XCUIElementTypeTable/XCUIElementTypeButton'),
        '发送': (MobileBy.ACCESSIBILITY_ID, 'cc chat send normal'),
        '新建群发': (MobileBy.XPATH, '//*[@name="新建群发"]'),
        '选择第一个群成员': (MobileBy.XPATH, '(//XCUIElementTypeTable/XCUIElementTypeCell)[1]'),
        '选择第二个群成员': (MobileBy.XPATH, '(//XCUIElementTypeTable/XCUIElementTypeCell)[2]'),
        '发送给': (MobileBy.IOS_PREDICATE, 'name CONTAINS "发送给"'),
        '已选择人数和可选择的最高上限人数': (MobileBy.XPATH, '//XCUIElementTypeButton[@name="确定(1/500)"]'),
        '可重新选择联系人': (MobileBy.XPATH, '//XCUIElementTypeButton[@name="确定(2/500)"]'),

    }

    @TestLogger.log()
    def is_exist_group_message_tariff(self):
        """判断是否在资费介绍页"""
        return self._is_element_present(self.__class__.__locators["欢迎使用群短信！"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待群发信息编辑加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["说点什么"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_later(self):
        """点击以后再说"""
        self.click_element(self.__locators['以后再说'])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__locators['确定'])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__locators['返回'])

    @TestLogger.log()
    def click_input_box(self):
        """点击输入框"""
        self.click_element(self.__locators['说点什么'])

    @TestLogger.log()
    def input_message_text(self, content):
        """输入消息文本"""
        self.input_text(self.__locators['说点什么'], content)

    @TestLogger.log()
    def click_send(self):
        """点击发送"""
        self.click_element(self.__locators['发送'])

    @TestLogger.log()
    def is_on_message_edit_page(self):
        """判断是否在短信编辑页面"""
        return self._is_element_present(self.__class__.__locators["说点什么"])

    @TestLogger.log()
    def is_on_message_record_page(self):
        """判断是否在消息记录页面"""
        return self._is_element_present(self.__class__.__locators["新建群发"])

    @TestLogger.log()
    def click_build_new_group_send(self):
        """点击新建群发"""
        self.click_element(self.__locators['新建群发'])

    @TestLogger.log()
    def click_addressee(self):
        """点击收件人"""
        self.click_element(self.__locators['收件人'])

    @TestLogger.log()
    def click_receivcer_avatar(self):
        """点击群成员"""
        self.click_element(self.__locators['群成员列表'])

    @TestLogger.log()
    def click_first_contact(self):
        """点击选择第一个群成员"""
        self.click_element(self.__locators['选择第一个群成员'])

    @TestLogger.log()
    def is_exist_addressee(self):
        """判断是否存在群成员展示"""
        return self._is_element_present(self.__class__.__locators["发送给"])

    @TestLogger.log()
    def is_exist_select_and_all(self):
        """判断是否存在已选择人数和可选择的最高上限人数"""
        return self._is_element_present(self.__class__.__locators["已选择人数和可选择的最高上限人数"])

    @TestLogger.log()
    def is_exist_select_all(self):
        """判断是否存在全选"""
        return self._is_element_present(self.__class__.__locators["全选"])

    @TestLogger.log()
    def click_select_all(self):
        """点击全选"""
        self.click_element(self.__locators['全选'])

    @TestLogger.log()
    def input_search_message(self, content):
        """输入搜索成员信息"""
        self.input_text(self.__locators['搜索成员'], content)

    @TestLogger.log('查看是否显示XX联系人')
    def is_contact_in_list(self, name):
        time.sleep(2)
        locator = (MobileBy.IOS_PREDICATE, "name CONTAINS '%s'" % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def click_second_contact(self):
        """点击选择第二个群成员"""
        self.click_element(self.__locators['选择第二个群成员'])

    @TestLogger.log()
    def is_exist_renew_select(self):
        """判断是否可以重新选择联系人"""
        return self._is_element_present(self.__class__.__locators["可重新选择联系人"])

    @TestLogger.log()
    def is_select_all(self, number):
        """判断是否是否全选"""
        locator = (MobileBy.XPATH, "//*[@name='确定(%s/500)']" % number)
        return self._is_element_present(locator)
