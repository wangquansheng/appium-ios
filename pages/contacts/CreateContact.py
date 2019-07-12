from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.keyboard import Keyboard
import time

class CreateContactPage(Keyboard, BasePage):
    """新建联系人"""
    # ACTIVITY = 'com.cmicc.module_contact.activitys.NewContactActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '新建联系人': (MobileBy.ACCESSIBILITY_ID, '新建联系人'),
        '保存': (MobileBy.ACCESSIBILITY_ID, '保存'),
        '清除文本': (MobileBy.ACCESSIBILITY_ID, '清除文本'),

        '姓名': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="姓名"])[1]'),
        '输入姓名': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeTextField'),

        '电话': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="电话"])[1]'),
        '输入号码': (MobileBy.XPATH,'//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]/XCUIElementTypeTextField'),

        '公司': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="公司"])[1]'),
        '输入公司': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[3]/XCUIElementTypeTextField'),

        '职位':(MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="职位"])[1]'),
        '输入职位': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[4]/XCUIElementTypeTextField'),

        '邮箱': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="邮箱"])[1]'),
        '输入邮箱': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[5]/XCUIElementTypeTextField'),

        "确定": (MobileBy.ACCESSIBILITY_ID, '确定'),
        "删除联系人": (MobileBy.ACCESSIBILITY_ID, "删除联系人"),
        "确定删除": (MobileBy.ACCESSIBILITY_ID, '删除'),
        "取消删除": (MobileBy.ACCESSIBILITY_ID, '取消'),

    }

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击保存')
    def click_save(self):
        """点击保存"""
        self.click_element(self.__class__.__locators['保存'])


    @TestLogger.log('点击输入姓名')
    def click_input_name(self):
        """点击输入姓名"""
        self.click_element(self.__locators['输入姓名'])


    @TestLogger.log('输入姓名')
    def input_name(self, name):
        """输入姓名"""
        self.input_text(self.__locators['输入姓名'], name)

    @TestLogger.log('点击输入号码')
    def click_input_number(self):
        """点击输入号码"""
        self.click_element(self.__locators['输入号码'])


    @TestLogger.log('清除文本')
    def click_clear_text(self):
        """点击清除文本"""
        self.click_element(self.__locators['清除文本'])


    @TestLogger.log('输入号码')
    def input_number(self, number):
        """输入号码"""
        self.input_text(self.__class__.__locators['输入号码'], number)


    @TestLogger.log('获取联系人手机号码')
    def get_contant_number(self):
        """获取联系人手机号码"""
        return self.get_element(self.__locators['输入号码'])



    @TestLogger.log('点击输入公司')
    def click_input_company(self):
        """点击输入公司"""
        self.click_element(self.__locators['输入公司'])

    @TestLogger.log('输入公司')
    def input_company(self, name):
        self.input_text(self.__locators['输入公司'], name)


    @TestLogger.log('点击输入职位')
    def click_input_position(self):
        """点击输入职位"""
        self.click_element(self.__locators['输入职位'])


    @TestLogger.log('输入职位')
    def input_position(self, name):
        self.input_text(self.__locators['输入职位'], name)

    @TestLogger.log('点击输入邮箱')
    def click_input_email(self):
        """点击输入邮箱"""
        self.click_element(self.__locators['输入邮箱'])


    @TestLogger.log('输入邮箱')
    def input_email_address(self, name):
        self.input_text(self.__locators['输入邮箱'], name)

    @TestLogger.log('点击保存')
    def save_contact(self):
        self.click_element(self.__locators['保存'])

    @TestLogger.log('保存按钮是否可点击')
    def is_save_icon_is_clickable(self):
        """保存按钮是否可点击"""
        return self._is_clickable(self.__class__.__locators['保存'])


    @TestLogger.log("删除联系人")
    def change_delete_contact(self):
        time.sleep(1)
        self.click_element(self.__locators['删除联系人'])

    @TestLogger.log("确定删除")
    def click_sure_delete(self):
        """确定删除"""
        time.sleep(3)
        self.click_element(self.__class__.__locators['确定删除'])



    @TestLogger.log('创建联系人')
    def create_contact(self, name, number, company='', position='', email=''):
        if name:
            self.click_input_name()
            self.input_name(name)
        if number:
            self.click_input_number()
            self.input_number(number)
        if company:
            self.page_down()
            self.input_company(company)
        if position:
            self.page_down()
            self.input_position(position)
        if email:
            self.page_down()
            self.input_email_address(email)
        self.click_save()

    @TestLogger.log('等待页面加载')
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        self.wait_until(
            condition=lambda d: self._is_element_present(self.__locators['姓名'])
        )


