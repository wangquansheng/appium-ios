from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time
from pages import MessagePage, MePage, SettingPage, MeSetDialPage, MeSetDialWayPage, GroupListPage, SelectContacts
from pages.call.CallTypeSelect import CallTypeSelectPage
from pages.contacts.local_contact import localContactPage
from pages.call.MultiPartyVideo import MultiPartyVideoPage


class CallPage(BasePage):
    """主界面-通话tab页"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        '通话': (MobileBy.ID, '通话'),
        '拨号': (MobileBy.ID, '拨号盘'),
        "消息": (MobileBy.ID, "消息"),
        "拨号盘": (MobileBy.ID, "拨号盘"),
        '拨号键1': (MobileBy.ID, 'cc_call_keypad_1'),
        '拨号键2': (MobileBy.ID, 'cc_call_keypad_2'),
        '拨号键3': (MobileBy.ID, 'cc_call_keypad_3'),
        '拨号键4': (MobileBy.ID, 'cc_call_keypad_4'),
        '拨号键5': (MobileBy.ID, 'cc_call_keypad_5'),
        '拨号键6': (MobileBy.ID, 'cc_call_keypad_6'),
        '拨号键7': (MobileBy.ID, 'cc_call_keypad_7'),
        '拨号键8': (MobileBy.ID, 'cc_call_keypad_8'),
        '拨号键9': (MobileBy.ID, 'cc_call_keypad_9'),
        '拨号键0': (MobileBy.ID, 'cc_call_keypad_0'),
        '拨号键*': (MobileBy.ID, 'cc_call_keypad_*'),
        '拨号键#': (MobileBy.ID, 'cc_call_keypad_#'),
        '删除X': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeButton[3]'),
        '小键盘多方通话按钮': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeButton[1]'),
        '拨号盘收缩删除X': (MobileBy.XPATH, '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeButton'),
        '拨打电话按键': (MobileBy.ACCESSIBILITY_ID, 'cc call startcall normal'),
        '通话界面高清显示图片': (MobileBy.ID, 'com.chinasofti.rcs:id/ivNoRecords'),
        '直接拨号或开始搜索': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextField"'),
        '新建联系人': (MobileBy.XPATH, "//*[contains(@label, '新建联系人')]"),
        '发送消息': (MobileBy.XPATH, "//*[contains(@value, '发送消息')]"),
        '结束通话': (MobileBy.ID, 'com.android.incallui:id/endButton'),
        '呼叫中': (MobileBy.ID, 'com.chinasofti.rcs:id/ivAvatar'),
        '挂断语音通话': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_call_out_term'),
        '挂断视频通话': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_out_Cancel'),
        '挂断和飞信电话': (MobileBy.ID, 'cc call ipcall red normal'),
        '通话显示': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="通话"]'),
        '通话记录': (MobileBy.XPATH, '//*[@type="XCUIElementTypeCell"]'),
        '删除通话记录': (MobileBy.ID, "com.chinasofti.rcs:id/tvContent"),
        '通话profile': (MobileBy.XPATH, "call list details normal@2x"),
        '通话详情按钮': (MobileBy.IOS_PREDICATE, 'name contains "call list details normal"'),
        "返回": (MobileBy.ID, "back"),
        "多方视频图标": (MobileBy.ACCESSIBILITY_ID, "cc call groupvideo normal"),
        "通话记录时间": (MobileBy.XPATH, "//*[@type='XCUIElementTypeButton']"),
        "通话记录时间-搜索状态": (MobileBy.XPATH, '//*[@label="call list details normal@2x"]'),
        "profileName": (MobileBy.XPATH, "//*[@type='XCUIElementTypeStaticText']"),
        "+号": (MobileBy.ACCESSIBILITY_ID, 'cc contacts add normal'),
        '飞信电话': (MobileBy.XPATH, '//*[@value="飞信电话"]'),
        '飞信电话(免费)': (MobileBy.XPATH, '//*[@name="飞信电话(免费)"]'),
        '多方视频': (MobileBy.IOS_PREDICATE, '//*[@label="多方视频"]'),
        '语音通话': (MobileBy.XPATH, '//*[@label="语音通话"]'),
        '视频通话': (MobileBy.XPATH, '//*[@label="视频通话"]'),
        '多方视频搜索框': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_contacts_search"'),
        '本机号码置灰按钮': (MobileBy.IOS_PREDICATE, 'name == "cc_contacts_checkbox_selected_grey"'),
        '当前组织搜索框标示': (MobileBy.IOS_PREDICATE, 'name CONTAINS "cc_contacts_search"'),
        "通话时间": (MobileBy.XPATH, "//XCUIElementTypeCell/XCUIElementTypeButton"),
        '缩放按钮-语音通话': (MobileBy.XPATH, '//*[@name="call audio scale normal"]'),
        '缩放按钮-视频通话': (MobileBy.XPATH, '//*[@name="call video scale normal"]'),
        '悬浮窗—点击返回通话': (MobileBy.XPATH, '//*[@name="点击返回通话"]'),
        '正在呼叫': (MobileBy.XPATH, '//*[@name="正在呼叫..."]'),
        '视频通话界面': (MobileBy.XPATH, '//*[@name="网络视频通话呼叫中..."]'),
        '呼叫': (MobileBy.IOS_PREDICATE, 'name CONTAINS "呼叫"'),
        "名片页电话按钮": (MobileBy.ID, "cc profile call normal"),
        "打开键盘": (MobileBy.ACCESSIBILITY_ID, "cc_call_keypad_expand"),
        "收起键盘": (MobileBy.ACCESSIBILITY_ID, "cc_call_keypaddown_normal"),
    }

    @TestLogger.log()
    def click_free_call(self):
        """点击多方通话"""
        self.click_element(self.__locators["多方通话"])

    @TestLogger.log()
    def wait_for_call_page(self, timeout=60, auto_accept_alerts=True):
        """
        等待通话界面
        """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("拨号盘")
            )
        except:
            raise AssertionError("通话界面未显示")
        return self

    @TestLogger.log()
    def is_on_the_call_page(self):
        """判断当前页是否通话界面"""
        flag = False
        element = self.get_elements(self.__locators["多方视频图标"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def is_on_the_dial_pad(self):
        """判断当前页是否调起拨号盘"""
        flag = False
        element = self.get_elements(self.__locators["拨打电话按键"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def click_one(self):
        """点击拨号键1"""
        self.click_element(self.__locators["拨号键1"])

    @TestLogger.log()
    def click_two(self):
        """点击拨号键2"""
        self.click_element(self.__locators["拨号键2"])

    @TestLogger.log()
    def click_three(self):
        """点击拨号键3"""
        self.click_element(self.__locators["拨号键3"])

    @TestLogger.log()
    def click_four(self):
        """点击拨号键4"""
        self.click_element(self.__locators["拨号键4"])

    @TestLogger.log()
    def click_five(self):
        """点击拨号键5"""
        self.click_element(self.__locators["拨号键5"])

    @TestLogger.log()
    def click_six(self):
        """点击拨号键6"""
        self.click_element(self.__locators["拨号键6"])

    @TestLogger.log()
    def click_seven(self):
        """点击拨号键7"""
        self.click_element(self.__locators["拨号键7"])

    @TestLogger.log()
    def click_eight(self):
        """点击拨号键8"""
        self.click_element(self.__locators["拨号键8"])

    @TestLogger.log()
    def click_nine(self):
        """点击拨号键9"""
        self.click_element(self.__locators["拨号键9"])

    @TestLogger.log()
    def click_zero(self):
        """点击拨号键0"""
        self.click_element(self.__locators["拨号键0"])

    @TestLogger.log()
    def click_star(self):
        """点击拨号键*"""
        self.click_element(self.__locators["拨号键*"])

    @TestLogger.log()
    def click_sharp(self):
        """点击拨号键#"""
        self.click_element(self.__locators["拨号键#"])

    @TestLogger.log()
    def click_delete(self):
        """点击删除X"""
        self.click_element(self.__locators["删除X"])

    @TestLogger.log()
    def click_delete_hide(self):
        """点击拨号盘收缩删除X"""
        self.click_element(self.__locators["拨号盘收缩删除X"])

    @TestLogger.log()
    def press_zero(self):
        """长按按键0"""
        self.swipe_by_direction(self.__class__.__locators['拨号键0'], 'press', 2)


    @TestLogger.log()
    def press_delete(self):
        """长按删除X"""
        # ios先更改为单按删除，请空文本
        # el = self.get_element(self.__locators["删除X"])
        # self.press(el)
        for i in range(20):
            self.click_element(self.__locators["删除X"])

    @TestLogger.log()
    def press_delete_hide(self):
        """拨号盘收缩删除X"""
        el = self.get_element(self.__locators["拨号盘收缩删除X"])
        self.press(el)

    @TestLogger.log()
    def click_call(self):
        """点击通话"""
        self.click_element(self.__locators["通话"])

    @TestLogger.log()
    def click_message(self):
        """点击消息"""
        self.click_element(self.__locators["消息"])

    @TestLogger.log()
    def click_call_phone(self):
        """点击拨打电话按键"""
        self.click_element(self.__locators["拨打电话按键"])

    @TestLogger.log()
    def check_call_phone(self):
        """检查拨打电话按键"""
        flag = False
        element = self.get_elements(self.__locators["拨打电话按键"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def check_call_image(self):
        """检查通话界面高清图片"""
        flag = False
        element = self.get_elements(self.__locators["通话界面高清显示图片"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def check_call_text(self, val=""):
        """检查拨号输入框文本内容与输入相同
        value：输入的文本内容：电话号码，str
        """
        callText = self.get_text(self.__locators["直接拨号或开始搜索"])
        flag = False
        if callText == val:
            flag = True
        return flag

    @TestLogger.log()
    def check_delete_hide(self):
        """检查拨号盘收缩删除X"""
        flag = False
        element = self.get_elements(self.__locators["拨号盘收缩删除X"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def click_new_contact(self):
        """点击新建联系人"""
        self.click_element(self.__locators["新建联系人"])

    @TestLogger.log()
    def click_send_message(self):
        """点击发送消息"""
        self.click_element(self.__locators["发送消息"])

    @TestLogger.log()
    def click_call_end(self):
        """点击结束通话"""
        self.click_element(self.__locators["结束通话"])

    @TestLogger.log()
    def check_call_success(self):
        """检查拨打电话成功"""
        flag = False
        element = self.get_elements(self.__locators["结束通话"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def wait_for_dial_pad(self, timeout=60, auto_accept_alerts=True):
        """
        等待拨号键盘
        """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("直接拨号")
            )
        except:
            raise AssertionError("通话界面未显示")
        return self

    @TestLogger.log()
    def click_back_by_android(self, times=1):
        """通过android键返回"""
        # times 返回次数
        for i in range(times):
            self.driver.back()
            time.sleep(1)

    @TestLogger.log()
    def get_call_color_of_element(self):
        """获取打电话控件坐标颜色"""
        self.get_coordinate_color_of_element(element=self.__locators["通话"], x=50, y=50, by_percent=True, mode='RGBA')

    @TestLogger.log()
    def check_end_voice_call(self):
        """检查语音通话结束按键是否存在"""
        flag = False
        element = self.get_elements(self.__locators["挂断语音通话"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def click_end_voice_call(self):
        """点击结束语音通话"""
        self.click_element(self.__locators["挂断语音通话"])

    @TestLogger.log()
    def hang_up_voice_call(self):
        """挂断语音通话"""
        if self._is_element_present(self.__class__.__locators["挂断语音通话"]):
            self.click_element(self.__class__.__locators["挂断语音通话"])

    @TestLogger.log()
    def hang_up_video_call(self):
        """挂断视频通话"""
        if self._is_element_present(self.__class__.__locators["挂断视频通话"]):
            self.click_element(self.__class__.__locators["挂断视频通话"])

    @TestLogger.log()
    def hang_up_hefeixin_call(self):
        """挂断和飞信电话"""
        if self._is_element_present(self.__class__.__locators["挂断和飞信电话"]):
            self.click_element(self.__class__.__locators["挂断和飞信电话"])

    @TestLogger.log()
    def is_phone_in_calling_state(self):
        """判断是否在通话界面"""
        return self.driver.current_activity == '.InCallActivity'

    @TestLogger.log()
    def is_on_calling_page(self, timeout=20, auto_accept_alerts=True):
        """当前是否在通话页面"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.driver.current_activity == '.InCallActivity'
            )
            return True
        except:
            return False

    @TestLogger.log()
    def hang_up_the_call(self):
        """挂断电话"""
        command = 'input keyevent KEYCODE_ENDCALL'
        if self.is_phone_in_calling_state():
            return self.execute_shell_command(command)

    @TestLogger.log()
    def check_multiparty_video(self):
        """判断是否存在视频图片来检查是否在通话界面"""
        return self._is_element_present(self.__locators["多方视频图标"])

    @TestLogger.log()
    def check_call_display(self):
        """判断是否存在通话显示"""
        return self._is_element_present(self.__locators["通话显示"])

    @TestLogger.log()
    def check_feixin_call(self):
        """判断是否存在多方通话"""
        return self._is_element_present(self.__locators["飞信电话"])

    def get_call_history(self, index):
        """通过下标获取通话记录号码"""
        elements = self.get_elements(self.__locators["通话记录"])
        try:
            if len(elements) > 0:
                return elements[index].text
        except:
            raise IndexError("元素超出索引")

    def dial_number(self, text):
        """输入拨打号码"""
        # ios无法拨打直接输入号码
        for i in range(len(text)):
            if text[i] == "1":
                self.click_one()
            if text[i] == "2":
                self.click_two()
            if text[i] == "3":
                self.click_three()
            if text[i] == "4":
                self.click_four()
            if text[i] == "5":
                self.click_five()
            if text[i] == "6":
                self.click_six()
            if text[i] == "7":
                self.click_seven()
            if text[i] == "8":
                self.click_eight()
            if text[i] == "9":
                self.click_nine()
            if text[i] == "0":
                self.click_zero()

    def dial_number_ios(self, text):
        """输入拨打号码"""
        self.input_text(self.__locators["直接拨号或开始搜索_ios"], text)

    @TestLogger.log()
    def press_delete_entry(self):
        """长按删除通话记录"""
        el = self.get_element(self.__locators["通话记录"])
        self.press(el)

    @TestLogger.log()
    def click_delete_entry(self):
        """删除通话记录"""
        self.click_element(self.__locators["删除通话记录"])

    @TestLogger.log()
    def check_delete_entry(self):
        """判断是否删除通话记录弹框"""
        return self._is_element_present(self.__locators["删除通话记录"])

    @TestLogger.log("清空通话记录")
    def delete_all_call_entry(self):
        """前置条件：当前已进入call界面"""
        if self.check_multiparty_video():
            for i in range(20):
                el = self.get_elements(self.__locators["通话记录"])
                if len(el) > 0:
                    self.swipe_by_percent_on_screen(90, 15, 30, 15)
                    time.sleep(1)
                    try:
                        mp = MessagePage()
                        mp.click_element_by_name("删除")
                        # self.click_text("删除")
                    except:
                        print("删除失败,重试")
                else:
                    print("已删除通话记录")
                    break
        else:
            raise AttributeError

    @TestLogger.log()
    def get_call_entry_color_of_element(self):
        """获取通话记录控件坐标颜色"""
        return self.get_coordinate_color_of_element(element=self.__locators["通话记录"], x=50, y=50, by_percent=True,
                                                    mode='RGBA')

    @TestLogger.log()
    def click_call_profile(self):
        """点击通话profile"""
        self.click_element(self.__locators["通话profile"])

    @TestLogger.log()
    def press_keyboard(self):
        """长按拨号盘输入框"""
        el = self.get_element(self.__locators["直接拨号或开始搜索"])
        self.press(el)

    @TestLogger.log()
    def is_exist_specified_prompt(self):
        """是否存在指定提示"""
        return self._is_element_present(self.__class__.__locators["指定提示"])

    @TestLogger.log()
    def click_multi_party_telephone(self):
        """点击多方电话"""
        self.click_element(self.__class__.__locators["多方电话提示框"])

    @TestLogger.log()
    def is_exist_know(self):
        """是否存在“知道了”文本"""
        return self._is_element_present(self.__class__.__locators["知道了"])

    @TestLogger.log()
    def click_know(self):
        """点击知道了"""
        self.click_element(self.__class__.__locators["知道了"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def is_exist_allow_button(self):
        """是否存在始终允许"""
        return self._is_element_present(self.__class__.__locators["始终允许"])

    @TestLogger.log()
    def click_allow_button(self, auto_accept_permission_alert=True):
        """点击允许"""
        self.click_element(self.__class__.__locators["始终允许"], auto_accept_permission_alert=auto_accept_permission_alert)

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待通话页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["多方视频图标"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_call_time(self):
        """点击通话记录时间"""
        self.click_element(self.__class__.__locators["通话记录时间"])

    @TestLogger.log()
    def is_exist_call_time(self):
        """判断是否存在通话记录时间"""
        return self._is_element_present(self.__locators["通话记录时间"])

    @TestLogger.log()
    def click_call_time_search_status(self):
        """点击通话记录时间-搜索状态"""
        self.click_element(self.__class__.__locators["通话记录时间"])

    @TestLogger.log()
    def is_exist_profile_name(self):
        """判断是否存在profile_name"""
        return self._is_element_present(self.__locators["profileName"])

    @TestLogger.log()
    def get_profile_name(self):
        """获取profile_name"""
        return self.get_text(self.__locators["profileName"])

    @TestLogger.log()
    def select_dial_mode(self):
        """进入拨号方式选择"""
        MessagePage().open_me_page()
        MePage().click_setting_menu()
        SettingPage().click_dial_setting()
        MeSetDialPage().click_dial_mode()

    @TestLogger.log()
    def setting_dial_mode_and_go_back_call(self):
        """设置拨号方式为总是询问，并返回call界面"""
        self.select_dial_mode()
        MeSetDialWayPage().click_call_type_alaways_ask()
        self.click_back_by_android(times=3)
        self.click_call()

    @TestLogger.log()
    def create_call_entry(self, text):
        """当前界面已在call界面，创建通话记录，并返回call界面"""
        self.click_dial()
        time.sleep(1)
        self.dial_number(text)
        self.click_call_phone()
        time.sleep(2)
        if CallTypeSelectPage().is_select_call():
            CallTypeSelectPage().click_call_by_voice()
        # self.click_call_end()
        self.wait_for_dial_pad()
        time.sleep(1)
        if not self.is_on_the_call_page():
            self.click_dial()

    @TestLogger.log()
    def click_multi_party_video(self):
        """点击多方视频"""
        self.click_element(self.__class__.__locators["多方视频图标"])

    @TestLogger.log()
    def select_type_start_call(self, text, calltype):
        """在call界面，输入号码选择拨打电话类型并拨打电话"""
        self.click_dial()
        self.dial_number(text)
        self.click_call_phone()
        time.sleep(2)
        if CallTypeSelectPage().is_select_call():
            if calltype == 2:
                CallTypeSelectPage().click_call_by_general()
            if calltype == 1:
                CallTypeSelectPage().click_call_by_voice()
            if calltype == 0:
                CallTypeSelectPage().click_call_by_app()
        time.sleep(1)

    @TestLogger.log()
    def is_on_this_messagepage(self):
        """当前页面是否在消息页"""
        try:
            self.wait_until(
                timeout=30,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def enter_contact_details(self, name):
        """进入联系人详情界面"""
        GroupListPage().open_contacts_page()
        for i in range(10):
            time.sleep(2)
            if self.is_text_present(name):
                self.click_text(name)
                break
            else:
                self.page_up()

    @TestLogger.log()
    def click_video_call(self):
        """点击视频通话"""
        self.click_element(self.__class__.__locators["视频通话"])

    @TestLogger.log()
    def click_voice_call(self):
        """点击语音通话"""
        self.click_element(self.__class__.__locators["语音通话"])

    @TestLogger.log()
    def click_mutil_call(self):
        """点击多方电话"""
        self.click_element(self.__class__.__locators["多方电话"])

    @TestLogger.log()
    def click_mutil_video_call(self):
        """点击多方视频"""
        self.click_element(self.__class__.__locators["多方视频"])

    @TestLogger.log('点击继续拨打')
    def click_go_on(self):
        self.click_element(self.__locators['继续拨打'])

    @TestLogger.log()
    def is_exist_go_on(self):
        """是否存在继续拨打按钮"""
        return self._is_element_present(self.__class__.__locators["继续拨打"])


    @TestLogger.log()
    def wait_for_chat_page(self):
        """等待单聊界面展示"""
        self.wait_until(
            timeout=30,
            auto_accept_permission_alert=True,
            condition=lambda d: self.is_text_present("说点什么..."))

    @TestLogger.log()
    def click_feixin_call(self):
        """点击飞信电话"""
        self.click_element(self.__locators['飞信电话'])

    @TestLogger.log()
    def click_dial(self):
        """点击拨号"""
        self.click_element(self.__locators['拨号'])

    @TestLogger.log()
    def click_feixin_call_free(self):
        """点击飞信电话(免费)"""
        self.click_element(self.__locators["飞信电话(免费)"])

    @TestLogger.log()
    def click_call_entry(self):
        """点击通话记录"""
        self.click_element(self.__locators["通话记录"])

    @TestLogger.log()
    def is_exists_call_entry(self):
        """是否存在通话记录"""
        flag = False
        element = self.get_elements(self.__locators["通话记录"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def input_video_search_text(self, text):
        """输入搜索文本"""
        self.input_text(self.__locators['多方视频搜索框'], text)

    @TestLogger.log()
    def is_exist_number_grey(self):
        """是否存在本机号码置灰按钮"""
        return self._is_element_present2(self.__class__.__locators["本机号码置灰按钮"])

    @TestLogger.log()
    def is_exist_group_contact_search(self):
        """是否存在团队联系人搜索框"""
        return self._is_element_present2(self.__class__.__locators["当前组织搜索框标示"])

    @TestLogger.log()
    def click_many_people_call(self):
        """点击多人通话呼叫按钮"""
        self.click_element(self.__locators["呼叫"])

    @TestLogger.log()
    def is_exist_stop_call_button(self):
        """是否存在挂断和飞信电话按钮"""
        return self._is_element_present2(self.__class__.__locators["挂断和飞信电话"])

    @TestLogger.log()
    def click_dial_button(self):
        """点击拨号盘按钮"""
        self.click_element(self.__locators["拨号盘"])

    @TestLogger.log()
    def click_keyboard_feixin_call(self):
        """点击小键盘多方通话按钮"""
        self.click_element(self.__locators["小键盘多方通话按钮"])

    @TestLogger.log()
    def click_infor_call(self):
        """点击名片页电话按钮"""
        self.click_element(self.__locators["名片页电话按钮"])

    @TestLogger.log()
    def click_call_times(self):
        """点击通话记录时间"""
        self.click_element(self.__class__.__locators["通话时间"])

    @TestLogger.log()
    def click_voice_zoom_button(self):
        """点击缩放按钮-语音通话按钮"""
        self.click_element(self.__class__.__locators["缩放按钮-语音通话"])

    @TestLogger.log()
    def click_suspension_window(self):
        """点击悬浮窗"""
        self.click_element(self.__class__.__locators["悬浮窗—点击返回通话"])

    @TestLogger.log()
    def is_on_voice_call_page(self):
        """判断是否在语音通话界面"""
        return self._is_element_present(self.__locators["正在呼叫"])

    @TestLogger.log()
    def click_video_zoom_button(self):
        """点击缩放按钮-视频通话按钮"""
        self.click_element(self.__class__.__locators["缩放按钮-视频通话"])

    @TestLogger.log()
    def is_on_video_call_page(self):
        """判断是否在视频通话界面"""
        return self._is_element_present(self.__locators["视频通话界面"])

    @TestLogger.log()
    def input_phone_numbers(self, numbers):
        """输入手机号码"""
        self.input_text(self.__class__.__locators["直接拨号或开始搜索"], numbers)

    @TestLogger.log()
    def is_exists_element_by_text(self, text):
        """是否存在指定元素"""
        return self._is_element_present2(self.__class__.__locators[text])

    @TestLogger.log()
    def click_element_by_text(self, text):
        """点击指定元素"""
        self.click_element(self.__class__.__locators[text])