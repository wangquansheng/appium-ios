from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MyQRCodePage(BasePage):
    """我的二维码"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.QRCodeActivity'

    __locators = {

        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '我的二维码': (MobileBy.ACCESSIBILITY_ID, '我的二维码'),
        '扫一扫': (MobileBy.ACCESSIBILITY_ID, 'cc chat create qr'),
        '扫描二维码，加我和飞信': (MobileBy.ACCESSIBILITY_ID, '扫描二维码，加我和飞信'),
        '分享二维码': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc me qrcode share normal"'),
        '保存二维码': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc me qrcode save normal"'),
        '进行中': (MobileBy.ACCESSIBILITY_ID, '进行中'),


    }


    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在当前页面-我的二维码"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["分享二维码"])
            )
            return True
        except:
            return False


    @TestLogger.log('等待加载完毕')
    def wait_for_loading_animation_end(self):
        self.mobile.wait_until_not(
            condition=lambda d: self._is_element_present(self.__locators['进行中']),
            timeout=60
        )

    def decode_qr_code(self):
        from pyzbar import pyzbar
        import io
        from PIL import Image

        screen_shot = self.mobile.get_element(self.__locators['二维码']).screenshot_as_png
        fp = io.BytesIO(screen_shot)
        qr = pyzbar.decode(Image.open(fp))
        if qr:
            return qr[0].data.decode()
        raise AssertionError('不是有效的二维码')

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击转发（分享）二维码')
    def click_forward_qr_code(self):
        self.click_element(self.__locators["分享二维码"], default_timeout=15)

    @TestLogger.log('点击下载（保存）二维码')
    def click_save_qr_code(self):
        self.click_element(self.__locators['保存二维码'], default_timeout=15)

    @TestLogger.log()
    def is_element_exist(self, text):
        """当前页面是否包含此元素"""
        return self._is_element_present(self.__locators[text])
