from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger

class ChatfileProviewPage(BasePage):
    """预览文件页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ACCESSIBILITY_ID, ''),
                  # 可预览文件页面
                  '返回': (MobileBy.ACCESSIBILITY_ID, '返回'),
                  '预览文件-更多': (MobileBy.ACCESSIBILITY_ID, 'cc chat file more normal'),
                  '预览文件-转发': (MobileBy.ACCESSIBILITY_ID, "转发"),
                  '预览文件-收藏': (MobileBy.ACCESSIBILITY_ID, "收藏"),
                  '其他应用打开': (MobileBy.ACCESSIBILITY_ID, "其他应用打开"),
                  '预览文件-取消': (MobileBy.ACCESSIBILITY_ID, "取消"),
                  #不可预览文件页面
                  '不可预览文件-打开': (MobileBy.ACCESSIBILITY_ID, '打开'),
                  '不可预览文件-文件头像': (MobileBy.ACCESSIBILITY_ID, '/var/containers/Bundle/Application/D2DC6C77-35DD-4A89-B9E9-624930C97BF1/AndFetion.app/ic_unknown@3x.png'),

                  #未下载的文件
                  '下载':(MobileBy.ACCESSIBILITY_ID,'下载'),
                  '打开': (MobileBy.ACCESSIBILITY_ID, '打开'),

                  # 选择其他应用界面
                  '选择其他应用-信息': (MobileBy.ACCESSIBILITY_ID, "信息"),


                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待预览文件页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["预览文件-更多"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_page_load_download_file_success(self, timeout=8, auto_accept_alerts=True):
        """等待预览文件页面文件下载成功 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["打开"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self



    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在预览文件页面"""
        try:
            self.wait_until(
                timeout=5,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["预览文件-更多"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])


    @TestLogger.log("点击预览文件页面-更多按钮")
    def click_more_Preview(self):
        self.click_element(self.__class__.__locators["预览文件-更多"])


    @TestLogger.log("点击预览文件页面-转发")
    def click_forward_Preview(self):
        self.click_element(self.__class__.__locators["预览文件-转发"])


    @TestLogger.log("点击预览文件页面-收藏")
    def click_collection_Preview(self):
        self.click_element(self.__class__.__locators["预览文件-收藏"])

    @TestLogger.log("点击其他应用打开")
    def click_other_App_open(self):
        self.click_element(self.__class__.__locators["其他应用打开"])

    @TestLogger.log()
    def get_preview_file_name(self):
        """获取预览文件页面-文件名称"""
        locator=(MobileBy.XPATH, '//XCUIElementTypeOther/XCUIElementTypeStaticText')
        return self.get_element(locator).text

    @TestLogger.log()
    def page_contain_element(self,locator='预览文件-更多'):
        """判断页面包含元素"""
        self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log()
    def page_contain_element_more(self,locator='预览文件-更多'):
        """判断页面包含元素"""
        self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log()
    def check_is_select_others_app_visionable(self):
        """判断选择其他应用页面是否吊起"""
        self.page_should_contain_element(self.__locators['选择其他应用-信息'])


    @TestLogger.log()
    def is_exist_element(self,locator='预览文件-更多'):
        """判断元素是否存在"""
        return self._is_element_present(self.__locators[locator])


    @TestLogger.log("点击其他应用打开")
    def click_open_icon(self):
        self.click_element(self.__class__.__locators["不可预览文件-打开"])

    @TestLogger.log("点击下载")
    def click_download(self):
        self.click_element(self.__class__.__locators["下载"])
