from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time


class SelectOneGroupPage(BasePage):
    """选择一个群页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupChatListActivity'

    __locators = {'返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
                  '选择一个群': (MobileBy.ACCESSIBILITY_ID, '选择一个群'),
                  '搜索群组': (MobileBy.ACCESSIBILITY_ID, '搜索群组'),
                  '群聊列表': (MobileBy.ACCESSIBILITY_ID, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
                  '群聊列表-第一个群': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell'),
                  '群聊头像': (MobileBy.XPATH, '(//XCUIElementTypeImage[@name="cc_chat_group_default"])'),
                  '企业群标志': (MobileBy.XPATH, '(//XCUIElementTypeImage[@name="cc_chat_company"])'),
                  '发送名片': (MobileBy.ACCESSIBILITY_ID, '发送名片'),
                  #搜索结果
                  '搜索群组框': (MobileBy.XPATH, '(//XCUIElementTypeSearchField[@name="搜索群组"])[1]'),
                  '搜索结果展示': (MobileBy.XPATH
                       , '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell'),
                  '搜索结果头像': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_group_default'),
                  #弹出框
                  '取消': (MobileBy.ACCESSIBILITY_ID, '取消'),
                  '发送': (MobileBy.ACCESSIBILITY_ID, '发送'),
                  '确定': (MobileBy.ACCESSIBILITY_ID, '确定'),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/recyclerView_contactList': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView_contactList'),
                  '列表项': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_group_list_item'),
                  'Q': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/contact_image': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_image'),
                  '群聊002': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '群聊001': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  '群聊名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  'com.chinasofti.rcs:id/contact_index_bar_view': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_view'),
                  'com.chinasofti.rcs:id/contact_index_bar_container': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container'),
                  'A': (MobileBy.ID, ''),
                  'B': (MobileBy.ID, ''),
                  'C': (MobileBy.ID, ''),
                  '右侧字母索引': (MobileBy.XPATH,
                             '//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView'),
                  '左侧字母索引': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_index"]'),
                  # 选择一个群转发消息时的弹框
                  '发送给': (MobileBy.XPATH, "//*[contains(@text, '发送给')]"),
                  '企业群标识': (MobileBy.IOS_PREDICATE, 'name=="cc_chat_company"'),
                  }

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在选择一个群"""
        el = self.get_elements(self.__locators['选择一个群'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待选择一个群页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择一个群"])
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
        self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def click_sure_send(self):
        """点击确定发送"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def input_search_keyword(self, keyword):
        """输入搜索内容"""
        self.input_text(self.__locators['搜索群组框'], keyword)

    @TestLogger.log()
    def click_search_box(self):
        """点击搜索群组"""
        self.click_element(self.__class__.__locators["搜索群组"])

    @TestLogger.log()
    def click_share_card(self):
        """点击发送名片"""
        self.click_element(self.__class__.__locators['发送名片'])

    @TestLogger.log()
    def select_first_group(self):
        """选择第一个群"""
        self.click_element(self.__class__.__locators['群聊列表-第一个群'])

    @TestLogger.log()
    def is_element_exit(self, text='确定'):
        """指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def select_one_company_group(self):
        """选择一个企业群"""
        self.click_element(self.__class__.__locators['企业群标志'])

    @TestLogger.log('点击搜索结果')
    def click_search_result(self):
        self.click_element(self.__class__.__locators['搜索结果展示'])

    @TestLogger.log()
    def click_sure_forward(self):
        """点击确定发送"""
        self.click_element(self.__class__.__locators['发送'])

    @TestLogger.log()
    def click_cancel_forward(self):
        """点击取消发送"""
        self.click_element(self.__class__.__locators['取消'])

    @TestLogger.log()
    def page_contain_element_result(self):
        """页面应该展示搜索结果"""
        self.page_should_contain_element(self.__class__.__locators['搜索结果展示'])

    @TestLogger.log()
    def page_not_contain_element_result(self):
        """页面应该不展示搜索结果"""
        self.page_should_not_contain_element(self.__class__.__locators['搜索结果展示'])

    @TestLogger.log()
    def page_contain_element(self,text='确定'):
        """页面应该包含元素"""
        self.page_should_contain_element(self.__class__.__locators[text])

    @TestLogger.log()
    def selecting_one_group_by_name(self, name):
        """根据群名选择一个群"""
        locator = (MobileBy.ACCESSIBILITY_ID, '%s' % name)
        self.click_element(locator, 20)

    @TestLogger.log()
    def find_one_group_by_name(self, name):
        """根据群名寻找一个群"""
        locator = (MobileBy.ACCESSIBILITY_ID, '%s' % name)
        self.find_element_by_swipe(locator, 20)

    # @TestLogger.log()
    # def select_one_group_by_name(self, name):
    #     """通过群名选择一个群"""
    #     self.click_element(
    #         (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text ="%s"]' % name))
    #

    @TestLogger.log()
    def click_one_contact(self, contactName):
        """选择特定联系人"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[contains(@text, "%s")]' % contactName))
        if el:
            el.click()
            return el
        else:
            print("本地联系人中无%s ，请添加此联系人再操作" % contactName)

    @TestLogger.log()
    def is_exists_group_search_box(self):
        """是否存在群搜索输入框"""
        return self._is_element_present(self.__class__.__locators['搜索群组'])

    @TestLogger.log('搜索群')
    def search_group(self, group_name):
        self.input_text(self.__locators['搜索群组'], group_name)

    @TestLogger.log('判断列表中是否包含XX群')
    def is_group_in_list(self, name):
        iterator = self.mobile.list_iterator(self.__locators['群列表'], self.__locators['列表项'])
        for group in iterator:
            if group.find_elements('xpath', '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                            '@text="{}"]'.format(name)):
                return True
        return False

    @TestLogger.log('toast信息存在判断')
    def catch_message_in_page(self, text):
        return self.is_toast_exist(text)

    @TestLogger.log()
    def input_search_box(self, message):
        """输入群聊名"""
        self.input_text(self.__class__.__locators["搜索群组框"], message)

    @TestLogger.log()
    def select_one_enterprise_group(self):
        """选择一个企业群 返回群名"""
        locator = (MobileBy.XPATH, '//*[@name="cc_chat_company"]/following-sibling::*[1]')
        if self._is_element_present2(locator):
            el = self.get_element(locator)
            name = el.text
            self.click_element(locator)
            return name

    @TestLogger.log()
    def is_exists_enterprise_group_icon(self):
        """是否存在企业群标识"""
        return self._is_element_present2(self.__class__.__locators["企业群标识"])

    @TestLogger.log()
    def get_search_result_group(self):
        """获取搜索结果群"""
        els = self.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'))
        if els:
            return els
        else:
            raise AssertionError("没有搜索结果")

    @TestLogger.log("根据导航栏的第一个字母定位")
    def choose_index_bar_click_element(self):
        self.click_element(
            ('xpath','//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView[1]'))
        elements = self.get_elements(self.__class__.__locators["群聊名"])
        elements[0].click()

    @TestLogger.log('搜索结果是否存在')
    def is_element_present_result(self):
        return self._is_element_present(self.__locators['搜索结果展示'])

    @TestLogger.log()
    def is_search_group_name_full_match(self, name):
        """搜索群名是否精准匹配"""
        els = self.get_elements(self.__class__.__locators["群聊名"])
        texts = []
        for el in els:
            text = el.text.strip()
            if text:
                texts.append(text)
        for t in texts:
            if name == t:
                return True
        raise AssertionError('搜索结果"{}"没有找到与关键字"{}"完全匹配的文本'.format(texts, name))

    @TestLogger.log()
    def get_group_name(self):
        """获取群名"""
        els = self.get_elements(self.__class__.__locators["群聊列表"])
        group_names = []
        if els:
            for el in els:
                group_names.append(el.text)
        return group_names
