from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time

class SingleChatSetPage(BasePage):
    """单聊设置页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.OneToOneSettingActivity'

    __locators = {
                  '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
                  '添加成员+号': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc chat groupchat add normal"'),
                    # 	cc chat groupchat add normal@3
                  '消息免打扰按钮': (MobileBy.XPATH, '//XCUIElementTypeSwitch[@name="消息免打扰"]'),
                  '消息免打扰': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="消息免打扰"]'),
                  '置订聊天按钮': (MobileBy.XPATH, '//XCUIElementTypeSwitch[@name="置顶聊天"]'),
                  '置顶聊天': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="置顶聊天"]'),
                  '查找聊天内容': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="查找聊天内容"])[1]'),
                  '清空本地聊天记录': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="清空本地聊天记录"])[1]'),
                  #查找聊天内容页面
                  '输入关键字快速搜索': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTextField'),
                  '文件': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="文件"])[1]'),
                  '图片与视频': (MobileBy.ACCESSIBILITY_ID, '(//XCUIElementTypeStaticText[@name="图片与视频"])[2]'),
                  '头像': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeImage'),
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待单聊设置页面加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("聊天设置")
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self


    @TestLogger.log()
    def click_file(self):
        """点击 文件"""
        self.click_element(self.__class__.__locators['文件'])

    @TestLogger.log()
    def search_chat_record(self):
        """点击 查找聊天内容"""
        self.click_element(self.__class__.__locators['查找聊天内容'])

    @TestLogger.log()
    def click_clear_local_chat_record(self):
        """点击清空本地聊天记录"""
        self.click_element(self.__class__.__locators['清空本地聊天记录'])

    @TestLogger.log()
    def click_sure_clear_local_chat_record(self):
        """点击确定清空本地聊天记录"""
        locator=(MobileBy.XPATH,'//XCUIElementTypeButton[@name="清空本地聊天记录"]')
        self.click_element(locator)

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators['返回'])


    @TestLogger.log()
    def click_add_icon(self):
        """点击添加成员+号"""
        self.click_element(self.__class__.__locators['添加成员+号'])


    @TestLogger.log()
    def click_avatar(self):
        """点击 头像"""
        self.click_element(self.__class__.__locators['头像'])



    @TestLogger.log()
    def is_open_msg_undisturb_switch(self):
        """消息免打扰开关是否开启"""
        return self.get_element_attribute(self.__class__.__locators['消息免打扰按钮'], attr="checkable")

    @TestLogger.log()
    def is_open_chat_set_to_top_switch(self):
        """置订聊天按钮开关是否开启"""
        el = self.get_element(self.__class__.__locators['置订聊天按钮'])
        return el.text == '开启'

    @TestLogger.log()
    def get_switch_undisturb_value(self):
        """获取免打扰开关的值"""
        time.sleep(2)
        if self._is_element_present2(self.__class__.__locators["消息免打扰按钮"]):
            el = self.get_element(self.__class__.__locators["消息免打扰按钮"])
            return el.text


    @TestLogger.log()
    def click_msg_undisturb_switch(self):
        """点击 消息免打扰按钮"""
        self.click_element(self.__class__.__locators['消息免打扰按钮'])

    @TestLogger.log()
    def click_chat_set_to_top_switch(self):
        """点击 置订聊天按钮"""
        self.click_element(self.__class__.__locators['置订聊天按钮'])

    @TestLogger.log()
    def search_chat_record(self):
        """点击 查找聊天内容"""
        self.click_element(self.__class__.__locators['查找聊天内容'])


    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在单聊设置页面"""
        try:
            self.wait_until(
                timeout=5,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["聊天设置"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def get_name(self):
        """获取聊天人的人名"""
        return self.get_element(self.__class__.__locators['axz']).text

    @TestLogger.log()
    def is_selected_no_disturb(self):
        """消息免打扰是否开启"""
        return self.is_selected(self.__class__.__locators["消息免打扰开关"])

    @TestLogger.log()
    def click_no_disturb(self):
        """点击 消息免打扰开关"""
        self.click_element(self.__class__.__locators['消息免打扰开关'])

