from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ScanPage(BasePage):
    """扫一扫"""
    ACTIVITY = 'cn.com.fetion.zxing.qrcode.activity.CaptureActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_back_white_normal'),
        '扫一扫': (MobileBy.XPATH, '(//*[@name="扫一扫"])'),
        'com.chinasofti.rcs:id/finderView': (MobileBy.ID, 'com.chinasofti.rcs:id/finderView'),
        'com.chinasofti.rcs:id/surfaceView': (MobileBy.ID, 'com.chinasofti.rcs:id/surfaceView'),
        'com.chinasofti.rcs:id/qrcode_scan_anim': (MobileBy.ID, 'com.chinasofti.rcs:id/qrcode_scan_anim'),
        '将二维码放入扫描框内,即可自动扫描': (MobileBy.XPATH, '(//*[@name="将二维码放入扫描框内,即可自动扫描"])'),
        '我的二维码': (MobileBy.XPATH, '(//*[@name="我的二维码"])'),
    }

    @TestLogger.log('进入我的二维码页面')
    def open_my_qr_code_page(self):
        self.click_element(self.__locators['我的二维码'])

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待消息页面加载（自动允许权限）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["我的二维码"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在扫一扫"""
        el = self.get_elements(self.__locators['扫一扫'])
        if len(el) > 0:
            return True
        return False
