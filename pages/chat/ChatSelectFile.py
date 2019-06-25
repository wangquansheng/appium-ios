from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time

class ChatSelectFilePage(BasePage):
    """聊天选择文件页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ChooseLocalFileActivity'

    __locators = {'返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
                  '我收到的文件': (MobileBy.ACCESSIBILITY_ID, '我收到的文件'),
                  '本地照片': (MobileBy.ACCESSIBILITY_ID, '本地照片'),
                  '本地视频': (MobileBy.ACCESSIBILITY_ID, '本地视频'),

                  #选择本地视频页面
                  '视频列表1': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
                  '视频列表2': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]'),
                  '确定': (MobileBy.ACCESSIBILITY_ID, '确定'),
                  '取消': (MobileBy.ACCESSIBILITY_ID, '取消'),

                  '选择文件': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  'com.chinasofti.rcs:id/fl_container': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_container'),
                  '本地文件': (MobileBy.IOS_PREDICATE, "label == '我收到的文件'"),
                  '视频': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_vedio'),
                  '照片': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_pic'),
                  '音乐': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_music'),
                  }

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待选择文件页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["我收到的文件"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log("ios——我收到的文件")
    def click_local_file(self):
        self.click_element(self.__class__.__locators["本地文件"])

    @TestLogger.log()
    def click_video(self):
        """点击视频"""
        self.click_element(self.__class__.__locators["本地视频"])

    @TestLogger.log()
    def click_pic(self):
        """点击照片"""
        self.click_element(self.__class__.__locators["本地照片"])

    # @TestLogger.log()
    # def click_music(self):
    #     """点击音乐"""
    #     self.click_element(self.__class__.__locators["音乐"])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在选择文件界面"""
        el = self.get_elements(self.__locators['我收到的文件'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def is_on_this_page_select_video(self):
        """当前页面是否在通讯录"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["视频列表1"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_select_video(self):
        """点击选择视频列表第一项"""
        self.click_element(self.__class__.__locators["视频列表1"])
        time.sleep(1)
        if self.is_text_present('确定'):
            self.click_sure_send()
        time.sleep(3)


    @TestLogger.log()
    def click_sure_send(self):
        """点击确定发送"""
        self.click_element(self.__class__.__locators["确定"])

