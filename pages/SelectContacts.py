from appium.webdriver.common.mobileby import MobileBy
import re
import copy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time
from pages.message.Message import MessagePage
from pages.GroupChat import GroupChatPage


# noinspection PyBroadException
class SelectContactsPage(BasePage):
    """选择联系人页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {
        '返回': (MobileBy.ACCESSIBILITY_ID, 'back'),
        '发送': (MobileBy.ACCESSIBILITY_ID, '发送'),
        '选择联系人': (MobileBy.ACCESSIBILITY_ID, '选择联系人'),
        '发送名片': (MobileBy.ACCESSIBILITY_ID, '发送名片'),
        '发送名片1': (MobileBy.IOS_PREDICATE, 'name == "发送名片"'),
        '搜索或输入手机号': (MobileBy.XPATH, '//XCUIElementTypeOther/XCUIElementTypeTextField'),
        '面对面建群': (MobileBy.IOS_PREDICATE, 'value == "面对面建群"'),
        '选择一个群': (MobileBy.ACCESSIBILITY_ID, '选择一个群'),
        '选择团队联系人': (MobileBy.ACCESSIBILITY_ID, '选择团队联系人'),
        '选择手机联系人': (MobileBy.IOS_PREDICATE, 'name == "选择手机联系人"'),
        '最近聊天': (MobileBy.ACCESSIBILITY_ID, '最近聊天'),
        '群聊': (MobileBy.ACCESSIBILITY_ID, '群聊'),
        '最近聊天列表': (MobileBy.XPATH,
                   '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[4]'),
        # 标签分组 选择联系人
        '选择联系人标题': (MobileBy.ACCESSIBILITY_ID, '选择联系人'),
        '确定': (MobileBy.ACCESSIBILITY_ID, '确定'),
        '搜索或输入手机号2': (MobileBy.XPATH,
                      '//XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeTextField'),
        '联系人列表': (MobileBy.XPATH,
                  '//XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]'),
        '联系人头像1': (MobileBy.XPATH,
                   '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]/XCUIElementTypeImage'),
        '确定2': (MobileBy.IOS_PREDICATE, "name CONTAINS '确定'"),
        '已选择的联系人(联系人列表)': (MobileBy.ACCESSIBILITY_ID, 'cc_contacts_checkbox'),
        '已选择的联系人': (MobileBy.XPATH,
                    '//XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell/XCUIElementTypeOther'),

        # 搜索结果页面
        '搜索团队联系人入口': (MobileBy.IOS_PREDICATE, 'name CONTAINS "搜索团队联系人"'),
        '搜索结果列表1': (MobileBy.XPATH, '//XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]'),
        '搜索结果列表2': (MobileBy.XPATH,
                    '//XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[3]'),
        '搜索结果-联系人头像': (MobileBy.XPATH,
                       '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]/XCUIElementTypeImage'),
        '清空搜索文本': (MobileBy.ACCESSIBILITY_ID, 'cc contacts delete pressed'),
        '网络搜索结果': (MobileBy.XPATH,
                   '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[2]'),
        '搜索结果_第一个联系人': (
            MobileBy.XPATH, '//XCUIElementTypeOther[@name="手机联系人"]/following-sibling::XCUIElementTypeCell[1]'),
        # 团队联系人搜索结果页面
        '团队联系人搜索结果': (MobileBy.XPATH
                      ,
                      '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]'),
        # 分享名片页面
        '分享名片左上角的X按钮': (MobileBy.ACCESSIBILITY_ID, "cc contancts sendcard close no"),
        '分享名片-头像': (MobileBy.XPATH,
                    '//XCUIElementTypeApplication[@name="和飞信"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeImage[2]'),
        '分享名片-姓名': (MobileBy.ACCESSIBILITY_ID, ""),
        '分享名片-可选项': (MobileBy.XPATH, '(//XCUIElementTypeImage[@name="cc_chat_card_circle_unselected"])[1]'),

        '查看更多': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="查看更多"])'),
        # '查看更多2': (MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="查看更多"])[2]'),

        '取消': (MobileBy.ACCESSIBILITY_ID, "取消"),
        # 分享二维码
        '确定发送': (MobileBy.ACCESSIBILITY_ID, "发送"),
        '取消发送': (MobileBy.ACCESSIBILITY_ID, "取消"),
        '确定3': (MobileBy.XPATH, "(//*[contains(@name,'确定')])[2]"),

        '聊天电话': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        # 分享二维码的选择联系人页面
        'tel:+86': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_number"]'),

        # 未知号码
        '未知号码': (MobileBy.XPATH, '//*[contains(@text,"未知号码")]'),
        # 选择一个联系人转发消息时的弹框
        '发送给': (MobileBy.XPATH, "//*[contains(@text, '发送给')]"),

        'local联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),

        '联系人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/head_tv'),
        '右侧字母索引': (MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView'),
        '左侧字母索引': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/index_text"]'),
        '和通讯录返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back'),
        "最近聊天消息名称": (MobileBy.ID, "com.chinasofti.rcs:id/tv_name"),
        "联系人横框": (MobileBy.ID, "com.chinasofti.rcs:id/contact_list_item"),
        "搜索框左边选中联系人": (MobileBy.ID, "com.chinasofti.rcs:id/image"),
        # 'aaa':(MobileBy.XPATH,"*[@text='aaa']"),
        'aaa': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),

        "搜索群组": (MobileBy.ID, 'com.chinasofti.rcs:id/et_search'),
        "搜索1": (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),

        "中软国际科技服务有限公司": (MobileBy.XPATH, "//*[@text='中软国际科技服务有限公司']"),
        "选择联系人列表": (MobileBy.ID, 'com.chinasofti.rcs:id/textview_action_bar_title'),
        "分组名": (MobileBy.ID, 'com.chinasofti.rcs:id/img_icon_department'),
        "成员ID": (MobileBy.ID, 'com.chinasofti.rcs:id/img_icon_contactlist'),
        "我已阅读": (MobileBy.ID, 'com.chinasofti.rcs:id/btn_check'),
        "最近聊天联系人": (MobileBy.ID, 'com.chinasofti.rcs:id/iv_photo'),
        "群二维码": (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
        "保存图片": (MobileBy.XPATH, '//*[@text="保存图片"]'),
        "识别图中二维码": (MobileBy.XPATH, '//*[@text="识别图中二维码"]'),
        "转发": (MobileBy.XPATH, '//*[@text="转发"]'),
        "企业通讯录联系人": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'),
        "搜索3": (MobileBy.ID, 'com.chinasofti.rcs:id/search_edit'),
        "搜索4": (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query01'),
        "发送人头像": (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        "发送时间": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
        "选中联系人头像": (MobileBy.ID, 'com.chinasofti.rcs:id/contact_icon'),
        "加入群聊": (MobileBy.IOS_PREDICATE, 'name == "加入群聊"'),

        'A': (MobileBy.XPATH, '//*[@text ="A"]'),
        'K': (MobileBy.XPATH, '//*[@text ="K"]'),
        "字母栏": (MobileBy.ID, '	com.chinasofti.rcs:id/contact_index_bar_container'),
        'bm1': (MobileBy.XPATH, "//*[contains(@text, 'bm1')]"),
        'bm2': (MobileBy.XPATH, "//*[contains(@text, 'bm2')]"),
        "联系人姓名": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
        "部门名称": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
        "禁止": (MobileBy.ID, 'com.android.packageinstaller:id/permission_deny_button'),
        "联系人栏": (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
        "群聊名称": (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeTextField"'),
        "创建按钮": (MobileBy.IOS_PREDICATE, 'name == "创建"'),
        '联系人转发-确定': (MobileBy.XPATH, '(//*[@name="确定"])'),

    }

    @TestLogger.log("当前页面是否在选择联系人页")
    def is_on_this_page(self):
        bol = self.wait_until(
            condition=lambda d: self.is_text_present('选择联系人')
        )
        return bol

    @TestLogger.log("点击返回")
    def click_back(self, text='返回'):
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log("点击确定（创建群组）")
    def click_sure_bottom(self, text='确定2'):
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log("点击最近聊天记录")
    def click_recent_chat_contact(self, text='最近聊天列表'):
        self.click_element(self.__locators[text])

    @TestLogger.log("点击最近聊天记录")
    def get_recent_chat_contact_name(self):
        locator = (MobileBy.XPATH, '//XCUIElementTypeCell/XCUIElementTypeStaticText')
        el = self.get_elements(locator)
        return el[3].text

    @TestLogger.log("检查控件是否存在")
    def check_if_element_exist(self, text='发送人头像'):
        self.page_should_contain_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_element_by_id(self, text='搜索结果列表1'):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def is_element_present(self, locator='最近聊天列表'):
        return self._is_element_present(self.__class__.__locators[locator])

    @TestLogger.log("检查控件是否存在")
    def check_if_element_not_exist(self, text='发送人头像'):
        self.page_should_not_contain_element(self.__class__.__locators[text])

    @TestLogger.log("最近聊天联系人")
    def click_recent_contact(self, text='最近聊天联系人'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("选择团队联系人")
    def click_group_contact(self, text='选择团队联系人'):
        """点击选择团队联系人"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("选择手机联系人")
    def click_phone_contact(self, text='选择手机联系人'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log('点击选择手机联系人')
    def click_phone_contacts(self):
        """点击选择手机联系人"""
        self.click_element(self.__locators['选择手机联系人'])

    @TestLogger.log('点击确定')
    def click_confirm_button(self):
        """点击确定"""
        self.click_element(self.__locators['确定2'])

    @TestLogger.log()
    def input_group_name_message(self, message):
        """输入要修改的群名称"""
        self.input_text(self.__class__.__locators["群聊名称"], message)
        return self

    @TestLogger.log('点击创建')
    def click_create_button(self):
        """点击创建按钮"""
        self.click_element(self.__locators['创建按钮'])

    @TestLogger.log()
    def is_exist_search_phone_number(self):
        """是否存在搜索或输入手机号输入框"""
        return self._is_element_present(self.__class__.__locators["搜索或输入手机号"])

    @TestLogger.log('搜索或输入手机号')
    def click_search_contact(self):
        """点击搜索或输入手机号"""
        self.click_element(self.__locators['搜索或输入手机号'])

    @TestLogger.log('搜索或输入手机号')
    def input_search_keyword(self, keyword):
        """输入搜索内容"""
        self.input_text(self.__locators['搜索或输入手机号'], keyword)

    @TestLogger.log('搜索或输入手机号2')
    def click_search_box(self):
        """点击搜索或输入手机号2（群聊 选择联系人界面）"""
        self.click_element(self.__locators['搜索或输入手机号2'])

    @TestLogger.log('搜索或输入手机号')
    def input_search_text(self, text):
        """输入搜索内容"""
        self.input_text(self.__locators['搜索或输入手机号2'], text)

    @TestLogger.log('判断该页面是否有元素')
    def page_contain_element(self, locator):
        return self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log()
    def click_select_one_group(self):
        """点击 选择一个群"""
        self.click_element(self.__class__.__locators["选择一个群"])

    @TestLogger.log()
    def click_he_contacts(self):
        """点击 选择和通讯录联系人/选择团队联系人"""
        self.click_element(self.__class__.__locators["选择团队联系人"])

    @TestLogger.log()
    def select_local_contacts(self):
        """选择本地联系人/选择手机联系人"""
        self.click_element(self.__class__.__locators["选择手机联系人"])

    @TestLogger.log()
    def click_x_icon(self):
        """点击 X"""
        self.click_element(self.__class__.__locators["清空搜索文本"])

    @TestLogger.log("选择成员ID")
    def click_sure_send(self, text='确定发送'):
        """点击确定发送"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log()
    def click_cancel_send(self, text='取消发送'):
        """点击取消发送"""
        time.sleep(1)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_search_group_contact(self, text='搜索团队联系人入口'):
        """点击搜索团队联系人入口"""
        time.sleep(1)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_share_card_close_icon(self, text='分享名片左上角的X按钮'):
        """点击搜索团队联系人入口"""
        time.sleep(1)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def select_one_contact_by_name(self, name):
        """通过名称选择一个联系人"""
        self.click_element((MobileBy.ACCESSIBILITY_ID, '%s' % name))

    @TestLogger.log()
    def click_search_result(self, text='搜索结果列表1'):
        """点击搜索结果列表排列第一的元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_sure_forward(self):
        """点击确定转发"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def click_sure_forward_code(self):
        """点击确定分享二维码"""
        self.click_element(self.__class__.__locators['确定3'])

    @TestLogger.log()
    def click_cancel_forward(self):
        """点击取消转发"""
        self.click_element(self.__class__.__locators['取消'])

    @TestLogger.log()
    def click_search_result_my_PC(self):
        """点击搜索结果列表-我的电脑头像"""
        locator = (MobileBy.ACCESSIBILITY_ID, 'cc_chat_ic_headportrait_computer')
        self.click_element(locator)

    @TestLogger.log()
    def click_search_result_from_internet(self, text):
        """点击搜索结果列表-网络搜索结果"""
        locator = (MobileBy.ACCESSIBILITY_ID, '%s（未知号码）' % text)
        self.click_element(locator)

    @TestLogger.log()
    def click_search_result_from_local_by_name(self, text):
        """点击搜索结果列表-本地搜索结果"""
        locator = (MobileBy.ACCESSIBILITY_ID, '%s' % text)
        els = self.get_elements(locator)
        return els[0].click()

    @TestLogger.log("点击已选择的联系人")
    def click_contact_which_is_selecd(self, text='已选择的联系人'):
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log("点击右侧字母")
    def click_right_word(self, text='A'):
        self.click_element(self.__locators[text])

    @TestLogger.log("点击群二维码")
    def click_group_code(self, text='群二维码'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("识别图中二维码")
    def click_recognize_code(self, text='识别图中二维码'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("选择:中软国际科技服务有限公司")
    def click_group_chinasoft(self, text='中软国际科技服务有限公司'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("选择成员ID")
    def click_group_contact_member(self, text='成员ID'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("选择分组名")
    def click_group_contact_name(self, text='分组名'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("点击组名")
    def click_group_name(self, text='aaa'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("点击搜索群组")
    def click_group_search(self):
        """搜索联系人"""
        time.sleep(1)
        self.click_element(self.__locators["搜索群组"])

    @TestLogger.log("搜索群组")
    def group_search(self, text='aaa'):
        """搜索联系人"""
        time.sleep(1)
        self.input_text(self.__class__.__locators["搜索1"], text)
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()

    @TestLogger.log()
    def search(self, text):
        """搜索联系人"""
        self.input_text(self.__class__.__locators["搜索或输入手机号"], text)
        # if self.driver.is_keyboard_shown():
        #     self.driver.hide_keyboard()

    @TestLogger.log()
    def is_present_unknown_member(self, timeout=3, auto_accept_alerts=True):
        """是否是未知号码（陌生号码）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["未知号码"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_unknown_member(self):
        """点击 未知号码（陌生号码）"""
        self.click_element(self.__class__.__locators["未知号码"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=3, auto_accept_alerts=True):
        """等待选择联系人页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择一个群"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_he_back(self):
        """点击 和通讯录返回"""
        self.click_element(self.__class__.__locators["和通讯录返回"])

    @TestLogger.log('点击分享名片')
    def click_share_card(self):
        """点击分享名片"""
        self.click_element(self.__class__.__locators['发送名片'])

    @TestLogger.log()
    def click_send_card(self):
        """点击发送名片"""
        self.click_element(self.__class__.__locators['发送名片1'])

    @TestLogger.log()
    def click_search_keyword(self):
        """点击搜索或输入手机号"""
        self.click_element(self.__class__.__locators["搜索或输入手机号"])

    @TestLogger.log('点击联系人')
    def click_contact(self, name):
        """点击联系人"""
        self.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and ' +
                            '@text="{}"]'.format(name)))

    @TestLogger.log('点击联系人头像')
    def click_cantact_avatar(self):
        """点击联系人头像"""
        self.click_element(self.__locators['选中联系人头像'])

    @TestLogger.log()
    def click_one_local_contacts(self):
        """点击一个本地联系人"""
        # els = self.get_elements(self.__class__.__locators["local联系人"])
        # contactnames = []
        # if els:
        #     for el in els:
        #         contactnames.append(el.text)
        #     self.select_one_contact_by_name(contactnames[0])
        try:
            self.wait_until(
                condition=lambda x: self.get_elements(self.__class__.__locators["联系人列表"])[0],
                auto_accept_permission_alert=False
            ).click()
        # else:
        except:
            raise AssertionError("没有本地联系人可转发")

    @TestLogger.log()
    def select_one_group_by_name(self, name):
        """通过群名选择一个群"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name))

    @TestLogger.log()
    def selecting_one_group_by_name(self, name):
        """根据群名选择一个群"""
        locator = (MobileBy.ACCESSIBILITY_ID, '%s' % name)
        self.click_element(locator, 20)

    @TestLogger.log()
    def select_one_recently_contact_by_name(self, name):
        """通过名称选择一个最近聊天的联系人"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text ="%s"]' % name))

    @TestLogger.log()
    def wait_for_page_local_contact_load(self, timeout=8, auto_accept_alerts=True):
        """等待选择联系人页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择联系人"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def catch_message_in_page(self, text):
        return self.is_toast_exist(text)

    @TestLogger.log()
    def find_element_by_swipe(self, locator, times=10):
        """找不到元素就滑动"""
        if self._is_element_present(locator):
            return self.get_element(locator)
        else:
            c = 0
            while c < times:
                self.page_up()
                if self._is_element_present(locator):
                    return self.get_element(locator)
                c += 1
            return None

    # @TestLogger.log("下一页")
    # def page_up(self):
    #     """向上滑动"""
    #     self.driver.execute_script('mobile: swipe', {'direction': 'up'})

    # @TestLogger.log("上一页")
    # def page_down(self):
    #     """向下滑动"""
    #     self.driver.execute_script('mobile: swipe', {'direction': 'down'})

    @TestLogger.log()
    def click_one_contact(self, contactName):
        """选择特定联系人"""
        el = self.find_element_by_swipe((MobileBy.IOS_PREDICATE, 'name contains "%s"' % contactName))
        if el:
            el.click()
            return el
        else:
            print("本地联系人中无%s ，请添加此联系人再操作" % contactName)

    @TestLogger.log()
    def input_search_contact_message(self, message):
        """输入查询联系人查询信息"""
        self.input_text(self.__class__.__locators["搜索或输入手机号"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log('检验搜索名称')
    def get_element_text_net_name(self, locator):
        text = self.get_text(self.__locators["搜索或输入手机号"])
        text = text + "(未知号码)"
        return self.element_should_contain_text(self.__locators[locator], text)

    @TestLogger.log('检验搜索号码')
    def get_element_text_net_number(self, locator):
        text = self.get_text(self.__locators["搜索或输入手机号"])
        text = "tel: +86" + text
        return self.element_should_contain_text(self.__locators[locator], text)

    @TestLogger.log('获取元素文本内容')
    def get_element_texts(self, locator):
        text = self.get_text(self.__locators["搜索或输入手机号"])
        locator = self.get_text(self.__locators[locator])
        if text.startswith("+86"):
            text = text[3:]
        if text.startswith("+852"):
            text = text[4:]
        if text.startswith("+"):
            text = text[1:]
        if text in locator:
            return True
        return False

    @TestLogger.log('点击最近聊天')
    def click_search_he_contact(self):
        self.click_element(self.__locators["最近聊天"])

    @TestLogger.log()
    def click_read_more(self):
        """点击查看更多"""
        self.click_element(self.__class__.__locators["查看更多"])

    @TestLogger.log()
    def wait_for_create_msg_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待 '消息页面 点击+ ->新建消息->选择联系人页面' 加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择联系人"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log()
    def is_left_letters_sorted(self):
        """左侧字母是否顺序排序"""
        els = self.get_elements(self.__locators['左侧字母索引'])
        letters = []
        for el in els:
            letters.append(el.text)
        # 过滤特殊字符
        for item in letters:
            if not re.match(r'[A-Za-z]', item):
                letters.remove(item)
        arrs = copy.deepcopy(letters)
        letters = sorted(letters)
        return arrs == letters

    @TestLogger.log()
    def is_right_letters_sorted(self):
        """右侧字母是否顺序排序"""
        els = self.get_elements(self.__locators['右侧字母索引'])
        letters = []
        for el in els:
            letters.append(el.text)
        for item in letters:
            if not re.match(r'[A-Za-z]', item):
                letters.remove(item)
        arrs = copy.deepcopy(letters)
        letters = sorted(letters)
        return arrs == letters

    @TestLogger.log()
    def select_recent_chat_by_name(self, name):
        """根据名字选择某一条最近聊天记录"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text="%s"]' % name)
        if self._is_element_present(locator):
            self.click_element(locator)

    @TestLogger.log()
    def is_exists_recent_chat_by_name(self, name):
        """是否存在指定最近聊天记录"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text="%s"]' % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def select_recent_chat_by_number(self, number):
        """选择某一条最近聊天记录"""
        if self._is_element_present(self.__class__.__locators["最近聊天消息名称"]):
            els = self.get_elements(self.__class__.__locators["最近聊天消息名称"])
            els[number].click()

    @TestLogger.log()
    def is_page_more_text(self, menu):
        """选择某一条最近聊天记录"""
        for text in menu:
            self.is_text_present(text)
        return True

    #
    # @TestLogger.log()
    # def click_sure_bottom(self):
    #     """点击确定"""
    #     self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def sure_icon_is_checkable(self):
        """确定按钮是否可点击"""
        return self._is_clickable(self.__class__.__locators['确定'])

    @TestLogger.log()
    def result_is_more_tree(self):
        """点击确定"""
        els = self.get_elements(self.__class__.__locators["local联系人"])
        if len(els) > 3:
            return True
        else:
            return False

    @TestLogger.log()
    def is_element_present_by_locator(self, text):
        """判断指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def swipe_and_find_element(self, text):
        """滑动并查找特定元素"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % text))
        if el:
            return True
        else:
            return False

    @TestLogger.log()
    def click_back_by_android(self, times=1):
        """
        点击返回，通过android返回键
        """
        # times 返回次数
        for i in range(times):
            self.driver.back()
            time.sleep(1)

    @TestLogger.log("创建群")
    def create_message_group(self, text='aaa'):
        time.sleep(2)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        from pages.groupset.GroupChatSet import GroupChatSetPage
        if self.get_elements(self.__locators['aaa']):
            self.click_element(self.__locators['aaa'])
            time.sleep(1)
            gcp = GroupChatPage()
            group_set = GroupChatSetPage()
            time.sleep(1)
            gcp.click_setting()
            time.sleep(1)
            sc.page_up()
            time.sleep(1)
            group_set.click_delete_and_exit()
            time.sleep(3)
        else:
            self.click_back_by_android()
        # mess.click_create_group()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        mess.click_contact_group()
        mess.click_text("大佬2")
        time.sleep(1)
        mess.click_text("大佬3")
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)
        mess.click_group_name()
        time.sleep(1)
        mess.set_group_name(text=text)
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)

    @TestLogger.log("选择多个联系人")
    def create_multi_contacts_group(self, groupname='aaa', num=1, times=1):
        time.sleep(2)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        from pages.groupset.GroupChatSet import GroupChatSetPage
        if self.get_elements(self.__locators['aaa']):
            self.click_element(self.__locators['aaa'])
            time.sleep(1)
            gcp = GroupChatPage()
            group_set = GroupChatSetPage()
            time.sleep(1)
            gcp.click_setting()
            time.sleep(1)
            sc.page_up()
            time.sleep(1)
            group_set.click_delete_and_exit()
            time.sleep(3)
        else:
            self.click_back_by_android()
        # mess.click_create_group()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        mess.click_contact_group()
        while times > 0:
            self.page_up()
            els = self.get_elements(self.__locators['aaa'])
            if els is None:
                break
            for i in range(num):
                time.sleep(1)
                els[i].click()
            times -= 1
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)
        mess.click_group_name()
        time.sleep(1)
        mess.set_group_name(text=groupname)
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)

    @TestLogger.log("选择团队联系人")
    def select_group_contacts(self, groupname='aaa', num=1, times=1):
        time.sleep(2)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        from pages.groupset.GroupChatSet import GroupChatSetPage
        if self.get_elements(self.__locators['aaa']):
            self.click_element(self.__locators['aaa'])
            time.sleep(1)
            gcp = GroupChatPage()
            group_set = GroupChatSetPage()
            time.sleep(1)
            gcp.click_setting()
            time.sleep(1)
            sc.page_up()
            time.sleep(1)
            group_set.click_delete_and_exit()
        else:
            self.click_back_by_android()
        # mess.click_create_group()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        mess.click_contact_group()
        while times > 0:
            self.page_up()
            els = self.get_elements(self.__locators['aaa'])
            if els is None:
                break
            for i in range(num):
                time.sleep(1)
                els[i].click()
            times -= 1
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)
        mess.click_group_name()
        time.sleep(1)
        mess.set_group_name(text=groupname)
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)

    @TestLogger.log()
    def press_and_move_right(self):
        """元素内向右滑动"""
        self.swipe_by_direction(self.__class__.__locators["搜索或输入手机号"], "right")

    @TestLogger.log()
    def get_firm_contacts_name_list(self):
        """获取企业通讯录联系人名"""
        els = self.get_elements(self.__class__.__locators["企业通讯录联系人"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        return contacts_name

    @TestLogger.log("删除自建群")
    def del_message_group(self):
        flag = True
        time.sleep(2)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        # 删除原来的群
        while flag:
            mess.click_add_icon()
            # 点击 发起群聊
            mess.click_group_chat()
            # 选择联系人界面，选择一个群
            sc = SelectContactsPage()
            sc.click_select_one_group()
            time.sleep(1)
            from pages.groupset.GroupChatSet import GroupChatSetPage
            if self.get_elements(self.__locators['aaa']):
                self.click_element(self.__locators['aaa'])
                time.sleep(1)
                gcp = GroupChatPage()
                group_set = GroupChatSetPage()
                time.sleep(1)
                gcp.click_setting()
                time.sleep(1)
                sc.page_up()
                time.sleep(1)
                group_set.click_delete_and_exit()
                time.sleep(3)
            else:
                self.click_back_by_android()
                break

    @TestLogger.log("创建群,选择手机联系人")
    def create_message_group2(self, text='aaa'):
        time.sleep(2)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        # 删除原来的群
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        time.sleep(1)
        mess.click_contact_group()
        mess.click_text("大佬2")
        time.sleep(1)
        mess.click_text("大佬3")
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)
        mess.click_group_name()
        time.sleep(1)
        mess.set_group_name(text=text)
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)

    @TestLogger.log("通过索引选择最近联系人最近聊天")
    def select_recent_chat_by_number(self, num):
        elements_list = self.get_elements(('id', 'com.chinasofti.rcs:id/item_rl'))
        elements_list[num].click()

    @TestLogger.log()
    def get_element_(self, text):
        """点击元素"""
        return self.get_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_send(self):
        """点击发送"""
        self.click_element(self.__class__.__locators['发送'])

    @TestLogger.log()
    def selecting_local_contacts_by_name(self, name):
        """根据名字选择一个手机联系人"""
        locator = (MobileBy.IOS_PREDICATE, 'name=="%s"' % name)
        self.click_element(locator)

    @TestLogger.log()
    def click_element_(self, text):
        """点击指定元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def is_element_exit_(self, text):
        """指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def is_text_present_(self, text):
        """指定文本是否存在（精确匹配）"""
        return self._is_element_present((MobileBy.IOS_PREDICATE, 'name == "%s"' % text)) or self._is_element_present(
            (MobileBy.IOS_PREDICATE, 'value == "%s"' % text))

    @TestLogger.log()
    def is_text_contain_present_(self, text):
        """指定文本是否存在（模糊匹配）"""
        return self._is_element_present(
            (MobileBy.IOS_PREDICATE, 'name contains "%s"' % text)) or self._is_element_present(
            (MobileBy.IOS_PREDICATE, 'value contains "%s"' % text))

    @TestLogger.log("点击联系人转发-确定")
    def click_forward_sure(self):
        if self._is_element_present(self.__class__.__locators["确定3"]):
            self.click_element(self.__class__.__locators["确定3"])
        else:
            self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log("判断是否包含文本")
    def is_text_present_c(self, text):
        try:
            if self.is_text_present(text):
                return True
            else:
                return False
        except Exception:
            return False

    @TestLogger.log()
    def is_element_exit_c(self, locator):
        """指定元素是否存在"""
        try:
            if len(self.get_elements(self.__class__.__locators[locator])) > 0:
                return True
            else:
                return False
        except Exception:
            return False
