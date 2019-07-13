from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class FindChatRecordPage(BasePage):
    """查找聊天内容页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageSearchActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  '返回': (MobileBy.ID, 'back'),
                  'com.chinasofti.rcs:id/iv_back': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
                  '输入关键词快速搜索': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTextField'),
                  '分类索引': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint_2'),
                  'com.chinasofti.rcs:id/layout_file_search': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_file_search'),
                  '文件': (MobileBy.ID, '文件'),
                  'com.chinasofti.rcs:id/layout_video_img_search': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/layout_video_img_search'),
                  '图片与视频': (MobileBy.ID, '图片与视频'),
                  'com.chinasofti.rcs:id/result_list': (MobileBy.ID, 'com.chinasofti.rcs:id/result_list'),
                  '发送人头像': (MobileBy.XPATH, '//XCUIElementTypeTable[2]/XCUIElementTypeCell/XCUIElementTypeImage'),
                  '发送人名称': (
                  MobileBy.XPATH, '//XCUIElementTypeTable[2]/XCUIElementTypeCell/XCUIElementTypeStaticText[1]'),
                  '发送的内容': (
                  MobileBy.XPATH, '//XCUIElementTypeTable[2]/XCUIElementTypeCell/XCUIElementTypeStaticText[3]'),
                  '发送的时间': (
                  MobileBy.XPATH, '//XCUIElementTypeTable[2]/XCUIElementTypeCell/XCUIElementTypeStaticText[2]'),
                  '聊天记录': (
                      MobileBy.XPATH, '//XCUIElementTypeTable[2]/XCUIElementTypeCell'),
                  }

    def is_exist_find_portrait(self):
        """当前页面是否有发送人头像"""
        el = self.get_elements(self.__locators['发送人头像'])
        return len(el) > 0

    def is_exist_find_name(self):
        """当前页面是否有发送人名称"""
        el = self.get_elements(self.__locators['发送人名称'])
        return len(el) > 0

    def is_exist_find_content(self):
        """当前页面是否有发送的内容"""
        el = self.get_elements(self.__locators['发送的内容'])
        return len(el) > 0

    def is_exist_find_time(self):
        """当前页面是否有发送的时间"""
        el = self.get_elements(self.__locators['发送的时间'])
        return len(el) > 0

    @TestLogger.log()
    def click_chat_records(self):
        """点击聊天记录"""
        self.click_element(self.__class__.__locators['聊天记录'])

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def click_file(self):
        """点击 文件"""
        self.click_element(self.__class__.__locators['文件'])

    @TestLogger.log()
    def click_pic_video(self):
        """点击 图片与视频"""
        self.click_element(self.__class__.__locators['图片与视频'])

    @TestLogger.log()
    def click_edit_query(self):
        """点击 输入关键词快速搜索"""
        self.click_element(self.__class__.__locators['输入关键词快速搜索'])

    @TestLogger.log()
    def input_search_message(self, message):
        """输入搜索信息"""
        self.input_text(self.__class__.__locators["输入关键词快速搜索"], message)
        # try:
        #     self.driver.hide_keyboard()
        # except:
        #     pass
        return self

    @TestLogger.log()
    def is_element_exit(self,keyName):
        """判断指定元素是否存在"""
        if self.get_element(self.__class__.__locators[keyName]):
            return True
        else:
            return False

    @TestLogger.log()
    def click_record(self):
        """点击 记录"""
        self.click_element(self.__class__.__locators['发送的内容'])

    @TestLogger.log()
    def wait_for_page_loads(self, timeout=60):
        """等待 页面加载"""
        try:
            self.wait_until(
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["输入关键词快速搜索"]),
                timeout=timeout
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self
