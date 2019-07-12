from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SelectCompanyContactsPage(BasePage):
    """群发信使-》短信群发页面-》新建短信收件人选择页面"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterPriseContactSelectActivity'

    __locators = {
        '新建短信': (MobileBy.XPATH, '//*[@text="新建短信"]'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back'),
        '搜索框': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextField"'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '搜索框左边头像': (MobileBy.ID, 'com.chinasofti.rcs:id/avator'),
        '全选复选框': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_check_all'),
        '联系人号码': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="团队联系人"]/../XCUIElementTypeCell[1]/XCUIElementTypeStaticText[1]'),
        '联系人名': (MobileBy.XPATH, '//XCUIElementTypeOther[@name="团队联系人"]/../XCUIElementTypeCell[1]/XCUIElementTypeStaticText[1]'),
        '联系人头像': (MobileBy.IOS_PREDICATE, 'name=="cc_chat_personal_default"'),
        '已选人名': (MobileBy.ID, 'com.chinasofti.rcs:id/image_text'),
        '已选头像': (MobileBy.ID, 'com.chinasofti.rcs:id/avator'),
        '确定按钮': (MobileBy.IOS_PREDICATE, 'name CONTAINS "确定"'),
        '企业层级': (MobileBy.XPATH, "//XCUIElementTypeScrollView/XCUIElementTypeButton"),
        '部门名称': (MobileBy.IOS_PREDICATE, "name=='cc_contacts_organization_classA'"),
        '选择联系人': (MobileBy.ACCESSIBILITY_ID, "选择联系人"),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待选择联系人页面加载"""
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
    def click_back(self):
        """点击返回"""
        els = self.get_elements(self.__class__.__locators['返回'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 返回 控件")

    @TestLogger.log()
    def input_search_message(self, message):
        """输入查找信息"""
        self.input_text(self.__class__.__locators["搜索框"], message)

    @TestLogger.log()
    def find_element_by_swipe(self, locator, times=10):
        """找不到元素就滑动"""
        if self._is_element_present(locator):
            return self.get_element(locator)
        else:
            c = 0
            while c < times:
                self.page_up()
                if self._is_element_present(locator):
                    return self.get_element(locator)
                c += 1
            return None

    @TestLogger.log()
    def click_one_contact(self, contactName):
        """选择特定联系人"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % contactName))
        if el:
            el.click()
            return el
        else:
            print("本地联系人中无%s ，请添加此联系人再操作" % contactName)

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        els = self.get_elements(self.__class__.__locators['确定'])
        if els:
            els[0].click()
        else:
            raise AssertionError("该页面没有定位到 确定 控件")

    @TestLogger.log()
    def is_left_head_exit(self):
        """搜索栏左侧被取消人员人名和头像是否存在"""
        if self._is_element_present(self.__class__.__locators['搜索框左边头像']):
            return True
        else:
            return False

    @TestLogger.log()
    def get_check_all(self):
        """获取全选复选框"""
        el = self.get_element(self.__class__.__locators['全选复选框'])
        return el

    @TestLogger.log()
    def is_exist_text(self):
        """是否存在文本"""
        return self.page_should_contain_text2("无搜索结果")

    @TestLogger.log()
    def is_search_contacts_number_full_match(self, number):
        """搜索联系人号码是否精准匹配"""
        if self._is_element_present2(self.__class__.__locators["联系人号码"]):
            text = self.get_element(self.__class__.__locators["联系人号码"]).text
            if number == text[(text.rindex(" ") + 1):]:
                return True
            raise AssertionError('搜索结果"{}"没有找到与关键字"{}"完全匹配的号码'.format(text, number))
        else:
            raise AssertionError('找不到元素 {}'.format(number))

    @TestLogger.log()
    def is_search_contacts_number_match(self, number):
        """搜索联系人号码是否模糊匹配"""
        if self._is_element_present2(self.__class__.__locators["联系人号码"]):
            text = self.get_element(self.__class__.__locators["联系人号码"]).text
            if number in text[(text.rindex(" ") + 1):]:
                return True
            raise AssertionError('搜索结果"{}"没有找到包含关键字"{}"的号码'.format(text, number))
        else:
            raise AssertionError('找不到元素 {}'.format(number))

    @TestLogger.log()
    def is_search_contacts_name_full_match(self, name):
        """搜索联系人名是否精准匹配"""
        if self._is_element_present2(self.__class__.__locators["联系人名"]):
            text = self.get_element(self.__class__.__locators["联系人名"]).text
            if name == text[:text.rindex(" ")]:
                return True
            raise AssertionError('搜索结果"{}"没有找到与关键字"{}"完全匹配的文本'.format(text, name))
        else:
            raise AssertionError('找不到元素 {}'.format(name))

    @TestLogger.log()
    def is_search_contacts_name_match(self, name):
        """搜索联系人名是否模糊匹配"""
        if self._is_element_present2(self.__class__.__locators["联系人名"]):
            text = self.get_element(self.__class__.__locators["联系人名"]).text
            if name in text[:text.rindex(" ")]:
                return True
            raise AssertionError('搜索结果"{}"没有找到包含关键字"{}"的文本'.format(text, name))
        else:
            raise AssertionError('找不到元素 {}'.format(name))

    @TestLogger.log()
    def click_contacts_by_name(self, name):
        """选择指定联系人"""
        self.click_accessibility_id_attribute_by_name(name)

    @TestLogger.log()
    def click_contacts_by_number(self, number):
        """选择指定联系人号码"""
        locator = (
            MobileBy.XPATH,
            '//*[@resource-id="com.chinasofti.rcs:id/tv_number_personal_contactlist" and contains(@text,"%s")]' % number)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def sure_button_is_enabled(self):
        """确定按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators["确定按钮"])

    @TestLogger.log()
    def is_clear_search_box(self, content):
        """输入框是否自动清空"""
        if self._is_element_present2(self.__class__.__locators["搜索框"]):
            text = self.get_element(self.__class__.__locators["搜索框"]).text
            if not text == content:
                return True
            return False
        else:
            raise AssertionError('找不到元素 {}'.format(content))

    @TestLogger.log()
    def is_exist_select_contacts_name(self, name):
        """是否存在已选联系人名"""
        locator = (MobileBy.ACCESSIBILITY_ID, "%s" % name)
        return self._is_element_present2(locator)

    @TestLogger.log()
    def click_select_contacts_name(self, name):
        """点击已选联系人名"""
        locator = (MobileBy.ACCESSIBILITY_ID, "%s" % name)
        self.click_element(locator)

    @TestLogger.log()
    def is_exist_select_contacts_image(self, name):
        """是否存在已选联系人头像"""
        locator = (MobileBy.XPATH, '//*[@name="%s"]/../XCUIElementTypeImage' % name)
        return self._is_element_present2(locator)

    @TestLogger.log()
    def click_contacts_image(self):
        """点击搜索出的联系人头像"""
        self.click_element(self.__class__.__locators["联系人头像"])

    @TestLogger.log()
    def click_sure_button(self):
        """点击确定按钮"""
        self.click_element(self.__class__.__locators["确定按钮"])

    @TestLogger.log()
    def is_exist_select_and_all(self, text):
        """是否展示已选人数"""
        return self._is_element_present2((MobileBy.IOS_PREDICATE, "name contains '确定(%s/'" % text))

    @TestLogger.log()
    def is_exist_corporate_grade(self):
        """是否存在企业层级"""
        return self._is_element_present2(self.__class__.__locators['企业层级'])

    @TestLogger.log()
    def is_exist_department_name(self):
        """是否存在部门/企业名称"""
        return self._is_element_present2(self.__class__.__locators['部门名称'])

    @TestLogger.log()
    def click_contacts_image_by_name(self, name):
        """点击指定联系人头像"""
        locator = (MobileBy.XPATH, '//*[@name="%s"]/../XCUIElementTypeImage' % name)
        self.click_element(locator)

    @TestLogger.log()
    def click_department_by_name(self, name):
        """选择指定部门"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title_department" and @text="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def is_exist_department_by_name(self, name):
        """是否存在指定部门/企业名称"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title_department" and @text="%s"]' % name)
        return self._is_element_present(locator)