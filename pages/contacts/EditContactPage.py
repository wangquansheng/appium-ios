from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class EditContactPage(BasePage):
    """编辑联系人页"""

    ACTIVITY = 'com.cmicc.module_contact.activitys.NewOrEditContactActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        "确定": (MobileBy.ACCESSIBILITY_ID, '确定'),
        "删除联系人": (MobileBy.ACCESSIBILITY_ID, "删除联系人"),
        "确定删除": (MobileBy.ACCESSIBILITY_ID, '删除'),
        "取消删除": (MobileBy.ACCESSIBILITY_ID, '取消'),
        '清除文本': (MobileBy.ACCESSIBILITY_ID, '清除文本'),

        '姓名': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="姓名"])[1]'),
        '已输入姓名': (MobileBy.XPATH,
                  '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeTextField'),

        '电话': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="电话"])[1]'),
        '电话号码': (MobileBy.XPATH,
                 '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]/XCUIElementTypeTextField'),

        '公司': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="公司"])[1]'),
        '输入公司': (MobileBy.XPATH,
                 '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[3]/XCUIElementTypeTextField'),

        '职位': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="职位"])[1]'),
        '输入职位': (MobileBy.XPATH,
                 '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[4]/XCUIElementTypeTextField'),

        '邮箱': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="邮箱"])[1]'),
        '输入邮箱': (MobileBy.XPATH,
                 '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[5]/XCUIElementTypeTextField'),

    }

    @TestLogger.log("当前页面是否在新建联系人页")
    def is_on_this_page(self):
        bol = self.wait_until(
            condition=lambda d: self.is_text_present('编辑联系人')
        )
        return bol

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击确定')
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log('清除文本')
    def click_clear_text(self):
        """点击清除文本"""
        self.click_element(self.__locators['清除文本'])


    @TestLogger.log("更改手机号码")
    def change_mobile_number(self,text='13800138005'):
        self.click_element(self.__locators['电话号码'])
        self.click_clear_text()
        self.input_text(self.__locators['电话号码'],text)


    @TestLogger.log("更改姓名")
    def change_contact_name(self,name='we'):
        self.click_element(self.__locators['已输入姓名'])
        self.click_clear_text()
        self.input_text(self.__locators['已输入姓名'],name)

    @TestLogger.log('点击已输入的姓名')
    def click_contact_name(self):
        """点击已输入的姓名"""
        self.click_element(self.__locators['已输入姓名'])

    @TestLogger.log('点击已输入号码')
    def click_contact_number(self):
        """点击已输入的号码"""
        self.click_element(self.__class__.__locators['电话号码'])

    @TestLogger.log('输入姓名')
    def input_name(self, name):
        """输入姓名"""
        self.input_text(self.__locators['已输入姓名'], name)


    @TestLogger.log('输入号码')
    def input_number(self, number):
        """输入号码"""
        self.input_text(self.__class__.__locators['电话号码'], number)

    @TestLogger.log('输入号码')
    def get_phone_number(self):
        """获取号码"""
        el = self.get_element(self.__class__.__locators['电话号码'])
        return el.text



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

    @TestLogger.log('确定按钮是否可点击')
    def is_sure_icon_is_clickable(self):
        """确定按钮是否可点击"""
        return self._is_clickable(self.__class__.__locators['确定'])

    @TestLogger.log('删除联系人')
    def click_delete_contact(self):
        """点击删除联系人"""
        self.click_element(self.__locators['删除联系人'])

    @TestLogger.log('取消删除联系人')
    def click_not_delete(self):
        """取消删除联系人"""
        self.click_element(self.__locators['取消删除'])

    @TestLogger.log('确定删除联系人')
    def click_sure_delete(self):
        """确定删除联系人"""
        self.click_element(self.__locators['确定删除'])

