from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time


class ChatLocationPage(BasePage):
    """聊天 位置 页面"""
    ACTIVITY = 'com.cmicc.module_message.ui.activity.GDLocationActvity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '发送': (MobileBy.ACCESSIBILITY_ID, '发送'),
        '搜索地点': (MobileBy.XPATH, '(//XCUIElementTypeSearchField[@name="搜索地点"])[1]'),
        '搜索': (MobileBy.ACCESSIBILITY_ID, '搜索'),
        # '搜索结果列表': (MobileBy. ''),
        '地图': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeOther'),
        '位置名称1': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
        #聊天 位置详情页面
        '导航按钮': (MobileBy.ACCESSIBILITY_ID, 'cc chat navigation normal'),
        '定位按钮': (MobileBy.ACCESSIBILITY_ID, 'cc_chat_map_point_blue'),



        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),

        'com.chinasofti.rcs:id/location_back_btn': (MobileBy.ID, 'com.chinasofti.rcs:id/location_back_btn'),
        '位置': (MobileBy.ID, 'com.chinasofti.rcs:id/location_title'),
        'com.chinasofti.rcs:id/select_rl': (MobileBy.ID, 'com.chinasofti.rcs:id/select_rl'),

        'com.chinasofti.rcs:id/map_info_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/map_info_layout'),
        'com.chinasofti.rcs:id/gd_map_view': (MobileBy.ID, 'com.chinasofti.rcs:id/gd_map_view'),
        'com.chinasofti.rcs:id/location_round_tips': (
            MobileBy.ID, 'com.chinasofti.rcs:id/location_round_tips'),
        '可选附近500米范围内的地点': (MobileBy.ID, 'com.chinasofti.rcs:id/location_round_tips_text'),
        'com.chinasofti.rcs:id/location_poi_list': (MobileBy.ID, 'com.chinasofti.rcs:id/location_poi_list'),
        'com.chinasofti.rcs:id/poi_list_item_root_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_root_view'),
        '中国银行24小时自助银行(环城路)': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_title'),
        '地址详细信息': (
            MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_detail'),
        'com.chinasofti.rcs:id/poi_list_item_select': (
            MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_select'),
        '中国铁路二十二局': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_title'),
        '广东省深圳市坂田街道雪岗北路133号天安云谷对面中国铁路二十二局': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_detail'),
        '博兴大厦': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_title'),
        '广东省深圳市坂田街道岗头发展大厦岗头村中心围一区8号博兴大厦博兴大厦': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_detail'),
        '岗头发展大厦': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_title'),
        '广东省深圳市坂田街道办雪岗北路133号岗头发展大厦': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_detail'),
        '选择项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/poi_list_item_root_view"]/android.widget.ImageView'),
        '第一项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/poi_list_item_root_view" and @index="0"]/android.widget.ImageView'),
        '其它项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/poi_list_item_root_view" and not(android.widget.ImageView)]'),
        # 权限框
        '允许': (MobileBy.XPATH, '//android.widget.Button[@text="允许"]'),
        '拒绝': (MobileBy.XPATH, '//android.widget.Button[@text="拒绝"]'),
        '要允许 和飞信 通过网络或者卫星对您的手机定位吗？': (MobileBy.XPATH, '//*[contains(@text,"定位")] | //*[contains(@text,"位置")]'),
    }

    @TestLogger.log()
    def click_send(self):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(3)

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])


    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待位置页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["位置名称1"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在位置页面"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators['位置名称1'])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def page_contain_element_navigation_button(self):
        """页面应该包含导航按钮"""
        self.page_should_contain_element(self.__class__.__locators['导航按钮'])


    @TestLogger.log()
    def is_on_this_page_navitation_detail_page(self):
        """当前页面是否在位置页面"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators['导航按钮'])
            )
            return True
        except:
            return False


    @TestLogger.log()
    def click_search_box(self):
        """点击搜索框"""
        self.click_element(self.__class__.__locators["搜索地点"])

    @TestLogger.log()
    def input_search_keyward(self,text):
        """输入搜索文本"""
        self.input_text(self.__class__.__locators["搜索"],text)


    @TestLogger.log()
    def click_search_result(self,text):
        """点击搜索结果"""
        locator=(MobileBy.XPATH,'//XCUIElementTypeStaticText[contains(@name,"%s")]',text)
        self.click_element(locator)

    @TestLogger.log()
    def press_and_move_left_on_map(self, duration=0, locator2=None):
        """元素内向左滑动"""
        if self._is_element_present2(self.__class__.__locators["定位按钮"]):
            element = self.get_element(self.__class__.__locators["定位按钮"])
            rect = element.rect
            left, right = int(rect['x']) + 1, int(rect['x'] + rect['width']) - 1
            top, bottom = int(rect['y']) + 1, int(rect['y'] + rect['height']) - 1
            x_start = right
            x_end = left - 50
            y_start = (top + bottom) // 2
            y_end = (top + bottom) // 2
            self.driver.execute_script("mobile:dragFromToForDuration",
                                       {"duration": duration, "element": locator2, "fromX": x_start,
                                        "fromY": y_start,
                                        "toX": x_end, "toY": y_end})


    @TestLogger.log()
    def get_locator_name(self):
        """获取位置名称"""
        element=self.get_element((MobileBy.XPATH,'//XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeStaticText[1]'))
        return element.text










    @TestLogger.log()
    def select_other_item(self):
        """选择其它项"""
        els = self.get_elements(self.__class__.__locators["其它项"])
        if els:
            els[0].click()
        else:
            print("no locations info")

    @TestLogger.log()
    def is_selected_first_item(self):
        """检查默认是否选择的是第一项"""
        els = self.get_elements(self.__class__.__locators["第一项"])
        if els:
            return True
        return False

    @TestLogger.log()
    def get_location_info(self):
        """获取发送的位置信息"""
        el = self.get_element(self.__class__.__locators["选择项"])
        addr_info = el.parent.find_element(*self.__class__.__locators["地址详细信息"]).text
        return addr_info

    @TestLogger.log()
    def click_allow(self):
        """点击允许"""
        self.click_element(self.__class__.__locators["允许"])


    @TestLogger.log()
    def send_btn_is_enabled(self):
        """获取发送按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["发送"])



    @TestLogger.log()
    def wait_for_permission_message_load(self, timeout=6, auto_accept_alerts=False):
        """等待权限允许申请弹窗加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['要允许 和飞信 通过网络或者卫星对您的手机定位吗？'])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

