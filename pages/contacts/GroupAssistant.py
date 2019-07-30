import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupAssistantPage(BasePage):
    """群发助手"""

    __locators = {
        '以后再说': (MobileBy.XPATH, '//*[@name="以后再说"]'),
        '确定': (MobileBy.IOS_PREDICATE, 'name CONTAINS "确定"'),
        '欢迎使用群发助手': (MobileBy.XPATH, '//*[@name="欢迎使用群发助手"]'),
        "返回": (MobileBy.ACCESSIBILITY_ID, 'back'),
        '发送短信': (MobileBy.IOS_PREDICATE, 'value == "发送短信..."'),
        '收件人': (MobileBy.XPATH, '//*[@name="收件人："]'),
        '群成员列表': (MobileBy.XPATH, '(//XCUIElementTypeButton)[1]'),
        '搜索': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextField"'),
        '选择群成员_确定': (MobileBy.IOS_PREDICATE, 'name CONTAINS "确定"'),
        '全选': (MobileBy.XPATH, '//XCUIElementTypeTable/XCUIElementTypeButton'),
        '发送': (MobileBy.ACCESSIBILITY_ID, 'cc chat send normal'),
        '新建群发': (MobileBy.XPATH, '//*[@name="新建群发"]'),

    }

    @TestLogger.log()
    def is_on_group_assistant_tariff(self):
        """判断是否在资费介绍页"""
        return self._is_element_present(self.__class__.__locators["欢迎使用群发助手"])

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
        self.click_element(self.__locators['发送短信'])

    @TestLogger.log()
    def input_message_text(self, content):
        """输入消息文本"""
        self.input_text(self.__locators['发送短信'], content)

    @TestLogger.log()
    def click_send(self):
        """点击发送"""
        self.click_element(self.__locators['发送'])

    @TestLogger.log()
    def is_on_message_edit_page(self):
        """判断是否在短信编辑页面"""
        return self._is_element_present(self.__class__.__locators["发送短信"])

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
    def input_search_message(self, content):
        """输入搜索成员信息"""
        self.input_text(self.__locators['搜索'], content)

    @TestLogger.log('查看是否显示XX联系人')
    def is_contact_in_list(self, name):
        time.sleep(2)
        locator = (MobileBy.IOS_PREDICATE, "name CONTAINS '%s'" % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def select_contacts_by_name(self, name):
        """根据名字选择一个联系人"""
        locator = (MobileBy.ACCESSIBILITY_ID, '%s' % name)
        self.click_element(locator,max_try=10)

    @TestLogger.log()
    def is_text_contain_present(self, text):
        """指定文本是否存在匹配结果"""
        return self._is_element_present(
            (MobileBy.XPATH, '//XCUIElementTypeOther[@name="手机联系人"]/following-sibling::XCUIElementTypeCell[*]/XCUIElementTypeStaticText[@name="%s"]' % text))



