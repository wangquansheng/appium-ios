from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class FreeMsgPage(BasePage):
    """免费短信"""
    ACTIVITY = 'com.cmicc.module_message.ui.activity.SuperMsgActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/super_msg_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/super_msg_layout'),
        'com.chinasofti.rcs:id/image_bg': (MobileBy.ID, 'com.chinasofti.rcs:id/image_bg'),
        'com.chinasofti.rcs:id/ll': (MobileBy.ID, 'com.chinasofti.rcs:id/ll'),
        '启用和飞信收发免费短信': (MobileBy.ID, 'com.chinasofti.rcs:id/group_tip'),
        '你可': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_tip2'),
        '免费给移动用户发送短信，': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_tip3'),
        '给非移动用户发短信将收取0.01元/条，': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_tip'),
        '给港澳台等境外用户发短信将收取1元/条。': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_tip_more'),
        'com.chinasofti.rcs:id/ll_bt': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_bt'),
        '以后再说': (MobileBy.XPATH, '//*[@name="以后再说"]'),
        '确定': (MobileBy.XPATH, '//*[@name="确定"]'),
        '欢迎使用免费短信！': (MobileBy.XPATH, '//*[@name="欢迎使用免费短信！"]'),
        "返回": (MobileBy.ACCESSIBILITY_ID, 'back'),
        "电话": (MobileBy.ACCESSIBILITY_ID, 'cc chat message call normal'),
        "设置": (MobileBy.ACCESSIBILITY_ID, 'cc chat message site normal'),
        '输入框': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextView"'),
        "发送": (MobileBy.ACCESSIBILITY_ID, 'cc chat send normal'),
        '你正在使用免费短信': (MobileBy.XPATH, '//*[@name="你正在使用免费短信"]'),
        '退出': (MobileBy.XPATH, '//*[@name="退出"]'),
        '资费说明': (MobileBy.XPATH, '//*[@name="资费说明"]'),
        '最后一条短信标识': (MobileBy.XPATH, '(//*[@name="短信"])[last()]'),
        '清空本地聊天记录': (MobileBy.XPATH, '(//*[@name="清空本地聊天记录"])'),
        '清空本地聊天记录_确定清除': (MobileBy.XPATH, '(//*[@name="清空本地聊天记录"][last()])'),
        "转发": (MobileBy.ACCESSIBILITY_ID, 'cc chat checkbox forward norma'),
        "删除": (MobileBy.ACCESSIBILITY_ID, 'cc chat checkbox delete normal'),

    }

    @TestLogger.log()
    def click_cancle_btn(self):
        """点击以后再说"""
        self.click_element(self.__locators['以后再说'])

    @TestLogger.log()
    def click_sure_btn(self):
        """点击确定"""
        self.click_element(self.__locators['确定'])

    @TestLogger.log()
    def is_exist_cancle_btn(self):
        """判断以后再说是否存在"""
        return self._is_element_present(self.__class__.__locators["以后再说"])

    @TestLogger.log()
    def is_exist_free_message_tariff(self):
        """判断是否在资费介绍页"""
        return self._is_element_present(self.__class__.__locators["欢迎使用免费短信！"])

    @TestLogger.log()
    def is_exist_using_free_message(self):
        """判断是否存在你正在使用免费短信"""
        return self._is_element_present(self.__class__.__locators["你正在使用免费短信"])

    @TestLogger.log()
    def click_quit_btn(self):
        """点击退出"""
        self.click_element(self.__locators['退出'])

    @TestLogger.log()
    def is_exists_element_by_text(self, text):
        """是否存在指定元素"""
        return self._is_element_present2(self.__class__.__locators[text])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在单聊会话页面"""
        return self._is_element_present2(self.__class__.__locators["输入框"])

    @TestLogger.log()
    def input_message_text(self, content):
        """输入消息文本"""
        self.input_text(self.__locators['输入框'], content)

    @TestLogger.log()
    def click_back_btn(self):
        """点击退出"""
        self.click_element(self.__locators['返回'])

    @TestLogger.log()
    def clear_input_text(self):
        """清空消息输入框"""
        self.click_element(self.__locators['输入框'])
        el = self.get_element(self.__locators["输入框"])
        el.clear()

    @TestLogger.log()
    def click_send_btn(self):
        """点击发送"""
        self.click_element(self.__locators['发送'])

    @TestLogger.log()
    def press_last_text_message(self):
        """长按最后一条短信消息"""
        if self._is_element_present2(self.__class__.__locators["最后一条短信标识"]):
            el = self.get_element(self.__class__.__locators["最后一条短信标识"])
            rect = el.rect
            x = rect['x']
            y = rect['y']
            width = rect['width']
            height = rect['height']
            x -= width
            y -= height
            self.driver.execute_script("mobile:dragFromToForDuration",
                                       {"duration": 5, "element": None, "fromX": x,
                                        "fromY": y,
                                        "toX": x, "toY": y})

    @TestLogger.log()
    def click_setting_btn(self):
        """点击设置"""
        self.click_element(self.__locators['设置'])

    @TestLogger.log()
    def click_clear_local_chat_history(self):
        """点击清空本地聊天记录"""
        self.click_element(self.__locators['清空本地聊天记录'])

    @TestLogger.log()
    def click_sure_clear_local_chat_history(self):
        """点击确定清空本地聊天记录"""
        self.click_element(self.__locators['清空本地聊天记录_确定清除'])

    @TestLogger.log()
    def click_forward_btn(self):
        """点击转发"""
        self.click_element(self.__locators['转发'])

    @TestLogger.log()
    def click_delete_btn(self):
        """点击删除"""
        self.click_element(self.__locators['删除'])



