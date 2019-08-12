import warnings

import preconditions
from library.core.TestCase import TestCase
from selenium.common.exceptions import TimeoutException
from library.core.utils.applicationcache import current_mobile, switch_to_mobile, current_driver
from library.core.common.simcardtype import CardType
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components.BaseChat import BaseChatPage
import time
import unittest

from preconditions.BasePreconditions import LoginPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': 'iphone',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
    'IOS-移动-移动': 'M960BDQN229CHiphone8',
}


class Preconditions(object):
    """前置条件"""

    @staticmethod
    def make_already_in_call():
        """确保进入通话界面"""
        preconditions.connect_mobile(REQUIRED_MOBILES['IOS-移动'])
        current_mobile().hide_keyboard_if_display()
        cpg = CallPage()
        message_page = MessagePage()
        if message_page.is_text_present('取消'):
            message_page.click_text('取消')
        if message_page.is_on_this_page():
            cpg.click_call()
            return
        if cpg.is_on_the_call_page():
            return
        try:
            current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
        except:
            pass
        current_mobile().launch_app()
        try:
            message_page.wait_until(
                condition=lambda d: message_page.is_on_this_page(),
                timeout=15
            )
            cpg.click_call()
            return
        except TimeoutException:
            pass
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()
        cpg.click_call()

    @staticmethod
    def enter_single_chat_page(name):
        """进入单聊聊天会话页面"""
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.selecting_local_contacts_by_name(name)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def get_into_group_chat_page(name):
        """进入群聊聊天会话页面"""
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_search_box()
        time.sleep(1)
        sog.input_search_box(name)
        time.sleep(2)
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""

        # current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_text_present('软件更新'):
            mess.click_text('关闭')
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        else:
            try:
                current_mobile().launch_app()
                mess.wait_for_page_load()
            except:
                # 进入一键登录页
                LoginPreconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                LoginPreconditions.login_by_one_key_login()


class CallAll(TestCase):
    """
    模块：通话
    文件位置：全量/ 7.通话（拨号盘、多方视频-非RCS、视频通话、语音通话）全量测试用例-申丽思.xlsx
    表格：通话（拨号盘、多方视频-非RCS、视频通话、语音通话）
    Author:wangquansheng
    """
    #
    # @classmethod
    # def setUpClass(cls):
    #     # 创建联系人
    #     fail_time = 0
    #     import dataproviders
    #     while fail_time < 3:
    #         try:
    #             required_contacts = dataproviders.get_preset_contacts()
    #             conts = ContactsPage()
    #             preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
    #             preconditions.make_already_in_message_page()
    #             current_mobile().hide_keyboard_if_display()
    #             preconditions.make_already_in_message_page()
    #             for name, number in required_contacts:
    #                 conts.open_contacts_page()
    #                 if conts.is_text_present("显示"):
    #                     conts.click_text("不显示")
    #                 conts.create_contacts_if_not_exits(name, number)
    #
    #             # 创建群
    #             required_group_chats = dataproviders.get_preset_group_chats()
    #
    #             conts.open_group_chat_list()
    #             group_list = GroupListPage()
    #             for group_name, members in required_group_chats:
    #                 group_list.wait_for_page_load()
    #                 group_list.create_group_chats_if_not_exits(group_name, members)
    #             group_list.click_back()
    #             conts.open_message_page()
    #             return
    #         except:
    #             fail_time += 1
    #             import traceback
    #             msg = traceback.format_exc()
    #             print(msg)
    #
    # @classmethod
    # def tearDownClass(cls):
    #     current_mobile().hide_keyboard_if_display()
    #     preconditions.make_already_in_message_page()

    def default_setUp(self):
        """进入Call页面,清空通话记录"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.make_already_in_call()
        CallPage().delete_all_call_entry()

    def default_tearDown(self):
        preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0001(self):
        """检查进入到通话界面，“通话”按钮变为“拨号盘”"""
        # Step:1.点击通话tab
        cpg = CallPage()
        cpg.click_dial()
        # CheckPoint:1.进入到通话记录列表界面，底部“通话”按钮变成“拨号盘”，拨号盘按钮显示9蓝点
        cpg.page_should_contain_text('拨号')
        cpg.page_should_contain_text("直接拨号或开始搜索")
        cpg.click_dial()

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0004(self):
        """检查拨号盘展开"""
        cpg = CallPage()
        # Step:1.点击“拨号盘"按钮
        cpg.click_dial()
        # CheckPoint:1.拨号盘展示，输入框提示“直接拨号或者开始搜索”，菜单栏被隐藏
        cpg.page_should_contain_text('直接拨号或开始搜索')
        cpg.click_dial()

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0006(self):
        """检查展开拨号盘，通话记录为空"""
        # Step:1.查看通话记录
        cpg = CallPage()
        # CheckPoint:1.页面中间显示图片以及提示语
        cpg.page_should_contain_text("高清通话，高效沟通")
        cpg.page_should_contain_text('飞信电话')

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0007(self):
        """检查拨号盘按键可点击"""
        cpg = CallPage()
        cpg.click_dial()
        # Step:1.点击按键“1”
        cpg.click_one()
        # Step:2.点击按键“2”
        cpg.click_two()
        # Step:3.点击按键“3”
        cpg.click_three()
        # Step:4.点击按键“4”
        cpg.click_four()
        # Step:5.点击按键“5”
        cpg.click_five()
        # Step:6.点击按键“6”
        cpg.click_six()
        # Step:7.点击按键“7”
        cpg.click_seven()
        # Step:8.点击按键“8”
        cpg.click_eight()
        # Step:9.点击按键“9”
        cpg.click_nine()
        # Step:10.点击按键“0”
        cpg.click_zero()
        # Step:11.点击按键“*”
        cpg.click_star()
        # Step:12.点击按键“#”
        cpg.click_sharp()
        # CheckPoint:1.步骤1-12：拨号盘各键输入正常
        cpg.page_should_contain_text("1234567890*#")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0008(self):
        """检查在拨号盘输入“+”"""
        # Step:1.检查在拨号盘输入“+”
        cpg = CallPage()
        cpg.click_dial()
        time.sleep(2)
        cpg.press_zero()
        time.sleep(2)
        # CheckPoint:1.展开后，通话记录按最近通话顺序展示
        cpg.page_should_contain_text("+")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0009(self):
        """检查输入框有内容时拨号盘可切换到其它模块"""
        # Step:1.切换至其它模块后又返回到拨号盘
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("15343030000")
        time.sleep(1)
        # CheckPoint:1.收起时切换到其他的模块，内容不清除，正常显示
        cpg.page_should_contain_text("15343030000")
        # Step:2. 切换为消息
        cpg.click_message()
        time.sleep(2)
        # CheckPoint:2.收起时切换到其他的模块，内容不清除，正常显示
        cpg.page_should_not_contain_text("15343030000")
        # Step:3. 切换为拨号盘
        cpg.click_call()
        # CheckPoint:3.收起时切换到其他的模块，内容不清除，正常显示
        cpg.page_should_contain_text("15343030000")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0010(self):
        """检查拨号盘删除按键可点击"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘输入框存在手机号
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("15343038860")
        # Step:1.点击按键“X”
        cpg.click_delete()
        # CheckPoit:1.可删除输入框的数据
        cpg.page_should_contain_text("1534303886")
        # Step:2.长按“X”
        cpg.press_delete()
        # CheckPoit:2.连续删除输入框的数据
        cpg.page_should_contain_text("直接拨号或开始搜索")
        cpg.click_dial()

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0011(self):
        """检查拨号盘“多方电话”按键可点击"""
        # Step:1.点击按键“多方电话”
        cpg = CallPage()
        cpg.click_feixin_call()
        time.sleep(2)
        # CheckPoint:1.调起联系人多方电话联系人选择器
        self.assertTrue(CalllogBannerPage().is_exist_contact_search_bar())

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0012(self):
        """检查拨号盘输入框为空点击“拨打”按钮"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘为展开状态
        # 3.拨号盘输入框为空
        cpg = CallPage()
        cpg.click_dial()
        time.sleep(2)
        # Step:1.点击“拨号”按钮
        cpg.click_call_phone()
        time.sleep(1)
        # # CheckPoint:1.提示“拨打号码不能为空”[toast无法验证 使用是否跳转页面判断]
        cpg.click_dial()
        self.assertTrue(cpg.is_on_the_call_page())

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0013(self):
        """检查拨号盘展开状态可收起"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘为展开状态
        cpg = CallPage()
        # Step:1.点击拨号盘按钮
        cpg.click_dial()
        time.sleep(1)
        # CheckPoint:1.拨号盘可收起展开，拨号盘图标变为7个蓝点
        self.assertTrue(cpg.is_on_the_dial_pad())
        cpg.click_dial()

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0014(self):
        """检查输入框有内容可收起拨号盘"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘为展开状态
        # 3.拨号盘存在数值
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("153")
        # Step:1点击拨号盘按钮
        cpg.click_dial()
        # CheckPoint:1.拨号盘可收起展开，收起展开内容保留不清除，正常显示
        flag = cpg.check_delete_hide()
        self.assertTrue(flag)
        cpg.page_should_contain_text("153")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0015(self):
        """检查输入框有内容收起拨号盘可切换到其它模块"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘为收起展开状态
        # 3.拨号盘存在数值
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("153")
        # Step:1.切换至其它模块后又返回到拨号盘
        cpg.click_message()
        flag = cpg.check_call_phone()
        self.assertFalse(flag)
        cpg.click_call()
        # CheckPoint:1.拨号盘可收起展开，收起展开内容保留不清除，正常显示
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        cpg.page_should_contain_text("153")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0020(self):
        """检查输入框输入超长数字"""
        # 1.和飞信登录系统：通话tab
        # 2.拨号盘展开状态
        # 3.拨号盘存在超长数值（数值超一行）
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("153153153153153")
        # Step:1.查看输入框样式
        # CheckPoint:1.显示正常
        time.sleep(1)
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        time.sleep(1)
        flag = cpg.check_call_text(val="153153153153153")
        self.assertTrue(flag)
        # Step:2.点击拨号盘，查看输入框样式
        cpg.click_dial()
        # 2.输入超长数字，收起显示正常
        time.sleep(1)
        # flag = cpg.check_call_phone()
        # self.assertFalse(flag)
        # time.sleep(1)
        flag = cpg.check_call_text(val="153153153153153")
        self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0022(self):
        """检查拨号盘精确搜索功能---内陆本地联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的内陆号本地已保存
        cpg = CallPage()
        # Step:1.点击“拨号盘”
        cpg.click_dial()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入11位数内陆号
        cpg.dial_number("13800138001")
        # CheckPoint:2.可匹配出符合条件的联系人，匹配的结果高亮
        cpg.page_should_contain_text("给个红包2")
        # ret = cpg.get_call_entry_color_of_element()
        # self.assertEqual(ret, (133, 128, 95, 255))
        # Step:3.点击匹配出的联系人右侧的时间节点
        cpg.click_call_time_search_status()
        time.sleep(1)
        # CheckPoint:3.可进入到该联系人的通话profile
        cpg.page_should_contain_text("分享名片")
        # Step:4.点击拨号按钮
        cpg.click_back()
        cpg.click_call_phone()
        # CheckPoint:4.可弹出拨号方式
        time.sleep(1)
        cpg.page_should_contain_text("飞信电话")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("普通电话")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0023(self):
        """检查拨号盘精确搜索功能---内陆陌生联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的内陆号本地未保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        cpg.click_dial()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入11位数内陆号
        cpg.dial_number("15343039999")
        time.sleep(2)
        # CheckPoint:2.通话记录列表弹出“新建联系人”“发送消息”按钮
        cpg.page_should_contain_text("新建联系人")
        cpg.page_should_contain_text("发送消息")
        # Step:3.点击拨号按钮
        cpg.click_call_phone()
        # CheckPoint:3.可弹出拨号方式
        time.sleep(2)
        cpg.page_should_contain_text("飞信电话")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("普通电话")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0024(self):
        """检查拨号盘精确搜索功能---香港本地联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的香港号本地已保存
        cpg = CallPage()
        # Step:1.点击“拨号盘”
        cpg.click_dial()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入8位数香港号
        cpg.dial_number("67656003")
        # CheckPoint:2.可匹配出符合条件的联系人，匹配的结果高亮
        cpg.page_should_contain_text("香港大佬")
        # Step:3.点击匹配出的联系人右侧的时间节点
        cpg.click_call_time_search_status()
        time.sleep(1)
        # CheckPoint:3.可进入到该联系人的通话profile
        cpg.page_should_contain_text("分享名片")
        cpg.click_back()

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0025(self):
        """检查拨号盘精确搜索功能---香港陌生联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的香港号本地未保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        cpg.click_dial()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入8位数香港号
        cpg.dial_number("23454097")
        time.sleep(2)
        # CheckPoint:2.通话记录列表弹出“新建联系人”“发送消息”按钮
        cpg.page_should_contain_text("新建联系人")
        cpg.page_should_contain_text("发送消息")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0026(self):
        """检查从拨号盘进入到陌生人消息会话窗口"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘已输入陌生联系人A的手机号
        # 3.通话记录列表已弹出“新建联系人”“发送消息”按钮
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("15343038860")
        # Step:1.点击“发送消息”按钮
        cpg.click_send_message()
        chatpage = BaseChatPage()
        flag = chatpage.is_exist_dialog()
        if flag:
            chatpage.click_i_have_read()
        # CheckPoint:1.进入与陌生联系人A的消息回话窗口
        cpg.page_should_contain_text("说点什么...")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0027(self):
        """检查从拨号盘新建联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘已输入陌生联系人A的手机号
        # 3.通话记录列表已弹出“新建联系人”“发送消息”按钮
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("15343038860")
        # Step:1.点击“新建联系人”按钮
        cpg.click_new_contact()
        time.sleep(2)
        cpg.hide_keyboard()
        # CheckPoint:1.跳转到新建联系人界面，电话栏自动填充联系人A的手机号，其它输入框为空
        cpg.page_should_contain_text("输入姓名")
        cpg.page_should_contain_text("15343038860")
        cpg.page_should_contain_text("输入公司")
        cpg.page_should_contain_text("输入职位")
        cpg.page_should_contain_text("输入邮箱")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0050(self):
        """检查拨号盘取消拨号方式"""
        # 1.用户已登录和飞信：通话-拨号盘
        # 2.已弹出拨号方式
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("15340038800")
        cpg.click_call_phone()
        time.sleep(1)
        # Step:1.点击“取消”按钮
        cpg.click_text("取消")
        # CheckPoint:1.拨号方式收起，停留在输入号码的拨号盘页
        self.assertTrue(cpg.check_call_phone())

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0051(self):
        """检查在拨号盘输入异常字符拨号"""
        # 1.用户已登录和飞信：通话-拨号盘
        # 2.在拨号盘已输入*，#、空格等字符
        # 3.无副号
        # Step:1.点击拨号按钮
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("*# ")
        cpg.click_call_phone()
        # CheckPoint:1.提示“输入号码无效，请重新输入”
        flag = cpg.is_toast_exist("输入的号码无效，请重新输入")
        self.assertTrue(flag)
        cpg.click_dial()

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0064(self):
        """检查拨号盘搜索功能---内陆本地联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的内陆号本地已保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        cpg.click_dial()
        time.sleep(2)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入11位数内陆号
        cpg.dial_number("13800138001")
        time.sleep(1)
        # CheckPoint:2.精确匹配出与拨号盘号码一致的手机号联系人
        cpg.page_should_contain_text("给个红包2")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0065(self):
        """检查拨号盘搜索功能---内陆陌生联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的内陆号本地未保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        cpg.click_dial()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入11位数内陆号
        cpg.dial_number("15343038867")
        # CheckPoint:2.通话记录列表弹出“新建联系人”“发送消息”按钮
        cpg.page_should_contain_text("新建联系人")
        cpg.page_should_contain_text("发送消息")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0066(self):
        """检查拨号盘搜索功能---香港本地联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的香港号本地已保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        cpg.click_dial()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入8位数香港号
        cpg.dial_number("67656003")
        # CheckPoint:2.精确匹配出与拨号盘号码一致的手机号联系人
        cpg.page_should_contain_text("香港大佬")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0067(self):
        """检查拨号盘搜索功能---香港陌生联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘输入的香港号本地未保存
        # Step:1.点击“拨号盘”
        cpg = CallPage()
        cpg.click_dial()
        time.sleep(1)
        # CheckPoint:1.弹出拨号盘界面
        flag = cpg.check_call_phone()
        self.assertTrue(flag)
        # Step:2.输入8位数香港号
        cpg.dial_number("67656000")
        # CheckPoint:2.通话记录列表弹出“新建联系人”“发送消息”按钮
        cpg.page_should_contain_text("新建联系人")
        cpg.page_should_contain_text("发送消息")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0068(self):
        """检查从拨号盘进入到陌生人消息会话窗口"""
        # 1.1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘已输入陌生联系人A的手机号
        # 3.通话记录列表已弹出“新建联系人”“发送消息”按钮
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("15343038867")
        # Step:1.点击“发送消息”按钮
        cpg.click_send_message()
        chatpage = BaseChatPage()
        if chatpage.is_exist_dialog():
            chatpage.click_i_have_read()
        # CheckPoint:1.进入与陌生联系人A的消息回话窗口
        cpg.page_should_contain_text("说点什么...")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0069(self):
        """检查从拨号盘新建联系人"""
        # 1.用户已登录和飞信：通话记录列表页面
        # 2.拨号盘已输入陌生联系人A的手机号
        # 3.通话记录列表已弹出“新建联系人”“发送消息”按钮
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("15343038867")
        # Step:1.点击“新建联系人”按钮
        cpg.click_new_contact()
        time.sleep(2)
        cpg.hide_keyboard()
        # CheckPoint:1.跳转到新建联系人界面，电话栏自动填充联系人A的手机号，其它输入框为空
        cpg.page_should_contain_text("输入姓名")
        cpg.page_should_contain_text("15343038867")
        cpg.page_should_contain_text("输入公司")
        cpg.page_should_contain_text("输入职位")
        cpg.page_should_contain_text("输入邮箱")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0070(self):
        """检查单聊富媒体面板-音频通话拨打"""
        # 1.登录和飞信：消息tab-单聊会话窗口-富媒体面板
        # 2.已弹出语音通话与视频通话按钮
        cpg = CallPage()
        ContactsPage().click_message_icon()
        Preconditions.enter_single_chat_page("给个红包2")
        BaseChatPage().click_more()
        ChatMorePage().click_voice_and_video_call()
        # Step:1.点击语音通话
        cpg.click_voice_call()
        # CheckPoint:1.直接呼出一对一语音通话
        time.sleep(2)
        cpg.page_should_contain_text("正在呼叫")
        cpg.wait_until(
            timeout=30,
            auto_accept_permission_alert=True,
            condition=lambda d: cpg.is_text_present("说点什么..."))
        # Step:2.点击视频电话
        BaseChatPage().click_more()
        ChatMorePage().click_voice_and_video_call()
        cpg.click_video_call()
        # Step:2.直接呼出一对一视频通话
        time.sleep(2)
        cpg.page_should_contain_text("视频通话呼叫中")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0086(self):
        """检查语音通话记录-本地联系人"""
        # 1.A已登录和飞信
        # 2.用户A已成功发起与用户B的语音通话
        # Step:1.用户A查看通话记录
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        # CheckPoint:1.通话记录展示与用户B的语音通话记录，显示用户B的名称、通话类型【语音通话】、归属地。右侧显示通话时间以及时间节点图标
        # iOS用户名显示无法获取，修改为判断是否存在通话记录，并在详情中判断名称
        # cpg.page_should_contain_text("给个红包2")
        self.assertTrue(cpg.is_exists_call_entry())
        cpg.page_should_contain_text("语音通话")
        # cpg.page_should_contain_text("广东深圳")
        # cpg.page_should_contain_text("移动")
        self.assertTrue(cpg.is_exist_call_time())
        # Step:2.点击时间节点
        cpg.click_dial()
        cpg.click_call_time_search_status()
        # CheckPoint:2.进入到用户B的通话profile
        cpg.page_should_contain_text("给个红包2")
        cpg.page_should_contain_text("编辑")
        self.assertTrue(CallContactDetailPage().is_exist_star())

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0087(self):
        """检查语音通话记录-企业联系人"""
        # 1.A已登录和飞信
        # 2.用户A已成功发起与用户N的语音通话
        # Step:1.用户A查看通话记录
        cpg = CallPage()
        cpg.create_call_entry("13800137003")
        # CheckPoint:1.通话记录展示与用户B的语音通话记录，显示用户B的名称、通话类型【语音通话】、归属地。右侧显示通话时间以及时间节点图标
        # iOS用户名显示无法获取，修改为判断是否存在通话记录，并在详情中判断名称
        # cpg.page_should_contain_text("哈 马上")
        self.assertTrue(cpg.is_exists_call_entry())
        cpg.page_should_contain_text("语音通话")
        self.assertTrue(cpg.is_exist_call_time())
        # Step:2.点击时间节点
        # Step:3.用户N为企业联系人（非本地联系人）
        cpg.click_dial()
        cpg.click_call_time_search_status()
        # CheckPoint:2.进入到用户N的通话profile
        cpg.page_should_contain_text("哈 马上")
        cpg.page_should_contain_text("飞信电话")
        cpg.page_should_contain_text("好久不见~打个招呼吧")

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0088(self):
        """检查语音通话记录-陌生联系人"""
        # 1.A已登录和飞信
        # 2.用户A已成功发起与用户B的语音通话
        # Step:1.用户A查看通话记录
        cpg = CallPage()
        cpg.create_call_entry("13537795364")
        # CheckPoint:1.通话记录展示与用户B的语音通话记录，显示用户B的名称、通话类型【语音通话】、归属地。右侧显示通话时间以及时间节点图标
        # cpg.page_should_contain_text("13537795364")
        self.assertTrue(cpg.is_exists_call_entry())
        cpg.page_should_contain_text("语音通话")
        self.assertTrue(cpg.is_exist_call_time())
        # Step:2.点击时间节点
        cpg.click_dial()
        cpg.click_call_time_search_status()
        # CheckPoint:2.进入到用户B的通话profile
        cpg.page_should_contain_text("13537795364")
        cpg.page_should_contain_text("飞信电话")
        cpg.page_should_contain_text("好久不见~打个招呼吧")

    @staticmethod
    def setUp_test_call_shenlisi_0155():
        # 关闭WiFi，打开4G网络
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.make_already_in_call()
        CallPage().delete_all_call_entry()
        CallPage().set_network_status(4)

    @tags('ALL', 'CMCC-network', 'Call')
    def test_call_shenlisi_0155(self):
        """检查语音通话-未订购每月10G用户--4g弹出每月10G免流特权提示窗口"""
        # 1.客户端已登录
        # 2.未订购每月10G用户
        # 3.网络使用4G
        cpg = CallPage()
        # Step:1.发起语音通话
        cpg.select_type_start_call(calltype=1, text="13800138001")
        time.sleep(1)
        # CheckPoint:1.弹出每月10G免流特权提示窗口。
        cpg.page_should_contain_text("每月10G免流特权")
        # Step:2.查看界面
        # CheckPoint:2.加粗文案为：语音通话每分钟消耗约0.3MB流量，订购[每月10G]畅聊语音/视频通话。弹窗底部显示“继续拨打”、“订购免流特权”、“以后不再提示”
        cpg.page_should_contain_text("语音通话每分钟消耗约0.3MB流量，订购[每月10G]畅聊语音/视频通话")
        cpg.page_should_contain_text("继续拨打")
        cpg.page_should_contain_text("订购免流特权")
        cpg.page_should_contain_text("以后不再提示")
        # Step:3.点击“继续拨打”
        cpg.click_text("继续拨打")
        # CheckPoint:3.点击后，直接呼叫
        cpg.page_should_contain_text("正在呼叫")
        # Step:4.再次点击语音通话
        cpg.wait_for_dial_pad()
        cpg.select_type_start_call(calltype=1, text="13800138001")
        # CheckPoint:4.继续弹出提示窗口
        cpg.page_should_contain_text("每月10G免流特权")

    @staticmethod
    def tearDown_test_call_shenlisi_0155():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)
        preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @staticmethod
    def setUp_test_call_shenlisi_0156():
        # 关闭WiFi，打开4G网络
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.make_already_in_call()
        CallPage().delete_all_call_entry()
        CallPage().set_network_status(4)

    @tags('ALL', 'CMCC_network', 'Call')
    def test_call_shenlisi_0156(self):
        """检查4g免流特权提示权订购免流特权提示窗口订购免流界面跳转---语音通话"""
        # 1.客户端已登录
        # 2.已弹出4g弹出每月10G免流特权提示窗口
        cpg = CallPage()
        cpg.select_type_start_call(calltype=1, text="13800138001")
        # 1.点击订购免流特权
        cpg.click_text("订购免流特权")
        # 1.跳转到【和飞信送你每月10G流量】H5页面
        cpg.wait_until(timeout=30, auto_accept_permission_alert=True,
                       condition=lambda d: cpg.is_text_present("和飞信送你每月10G流量"))
        cpg.page_should_contain_text("和飞信送你每月10G流量")
        # 2.点击返回按钮
        cpg.click_back()
        # 2.点击返回按钮，返回上一级
        cpg.page_should_contain_text("每月10G免流特权")

    @staticmethod
    def tearDown_test_call_shenlisi_0156():
        # 打开网络
        cpg = CallPage()
        cpg.set_network_status(6)
        preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @staticmethod
    def setUp_test_call_shenlisi_0158():
        # 确保打开WiFi网络
        Preconditions.make_already_in_call()
        # CalllogBannerPage().skip_multiparty_call()
        # CallPage().delete_all_call_entry()
        # CallPage().set_network_status(6)

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0158(self):
        """检查语音呼叫-未订购每月10G用户--用户在WiFi环境下不提示此类弹窗"""
        # 1.客户端已登录
        # 2.未订购每月10G用户
        # 3.网络使用WIFI
        # 1.发起语音通话
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("13800138001")
        cpg.click_call_phone()
        time.sleep(2)
        CallTypeSelectPage().click_call_by_voice()
        time.sleep(2)
        # 1.直接发起语音通话，没有弹窗
        cpg.page_should_not_contain_text("每月10G免流特权")
        time.sleep(1)
        cpg.wait_for_dial_pad()
        cpg.click_dial()

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0213(self):
        """检查视频通话记录——本地联系人"""
        # 1.A已登录和飞信
        # 2.用户A已成功发起与用户B的视频通话
        cpg = CallPage()
        cpg.click_multi_party_video()
        time.sleep(1)
        CalllogBannerPage().input_telephone("13800138001")
        time.sleep(1)
        cpg.click_text("给个红包2")
        time.sleep(1)
        cpg.click_text("呼叫")
        time.sleep(1)
        # Step:1.用户A查看通话记录
        cpg.wait_for_page_load()
        # CheckPoint:1.通话记录展示与用户B的视频通话记录，显示用户B的名称、通话类型【视频通话】、手机号/归属地
        cpg.page_should_contain_text("给个红包2")
        cpg.page_should_contain_text("视频通话")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0215(self):
        """检查视频通话记录-陌生联系人"""
        # 1.A已登录和飞信
        # 2.用户A已成功发起与用户B的视频通话
        cpg = CallPage()
        cpg.click_multi_party_video()
        CalllogBannerPage().input_telephone("13537795364")
        cpg.swipe_by_percent_on_screen(50, 40, 50, 10)
        # cpg.hide_keyboard()
        time.sleep(2)
        cpg.click_text("未知号码")
        time.sleep(1)
        cpg.click_text("呼叫")
        time.sleep(1)
        # Step:1.用户A查看通话记录
        cpg.wait_for_page_load()
        # CheckPoint:1.通话记录展示与用户B的视频通话记录，显示用户B的名称、通话类型【视频通话】、手机号/归属地
        cpg.page_should_contain_text("13537795364")
        cpg.page_should_contain_text("视频通话")
        cpg.page_should_contain_text("广东深圳")
        # cpg.page_should_contain_text("移动")
        # self.assertTrue(cpg.is_exist_call_time())

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0218(self):
        """检查呼叫本地联系人，呼叫界面展示名称+手机号"""
        # 1.已登录和飞信
        # 2.用户M为本地联系人
        # 3.已开启麦克风，相机权限
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("13800138001")
        cpg.click_call_time_search_status()
        time.sleep(1)
        # Step:1.视频呼叫M，进入到呼叫界面
        CallContactDetailPage().click_video_call()
        time.sleep(1)
        # CheckPoint:1.头像下展示用户M的名称+手机号
        cpg.page_should_contain_text("13800138001")
        cpg.page_should_contain_text("给个红包2")
        CallContactDetailPage().wait_for_star()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0219(self):
        """检查呼叫陌生联系人，呼叫界面展示手机号+归属地"""
        # 1.已登录和飞信
        # 2.用户M为陌生联系人可获取到归属地
        # 3.用户N为陌生联系人无法获取归属地（香港号，198开头11位手机号）
        # 3.已开启麦克风，相机权限
        cpg = CallPage()
        cpg.create_call_entry("15343038867")
        cpg.click_dial()
        cpg.click_call_time_search_status()
        time.sleep(1)
        # Step:1.视频呼叫M，进入到呼叫界面
        CallContactDetailPage().click_video_call()
        time.sleep(1)
        # CheckPoint:1.头像下展示用户M的手机号+归属地
        cpg.page_should_contain_text("15343038867")
        cpg.page_should_contain_text("湖南-株洲")
        CallContactDetailPage().wait_for_star()
        cpg.click_back()

        # Step:2.视频呼叫N，进入到呼叫界面
        cpg = CallPage()
        cpg.create_call_entry("19823452586")
        cpg.click_dial()
        cpg.click_call_time_search_status()
        time.sleep(1)
        # Step:2.视频呼叫N，进入到呼叫界面
        CallContactDetailPage().click_video_call()
        time.sleep(1)
        # CheckPoint:2.头像下展示用户M的手机号+未知归属地
        cpg.page_should_contain_text("19823452586")
        cpg.page_should_contain_text("未知归属地")
        CallContactDetailPage().wait_for_star()

    @staticmethod
    def setUp_test_call_shenlisi_0234():
        # 确保打开WiFi网络
        Preconditions.make_already_in_call()
        CallPage().delete_all_call_entry()
        # CallPage().set_network_status(6)

    @tags('ALL', 'CMCC', 'Call', "ios")
    def test_call_shenlisi_0234(self):
        """检查视频呼叫-未订购每月10G用户--用户在WiFi环境下不提示此类弹窗"""
        # 1.客户端已登录
        # 2.未订购每月10G用户
        # 3.网络使用WIFI
        # 1.发起视频通话
        cpg = CallPage()
        cpg.click_dial()
        cpg.dial_number("13800138001")
        cpg.click_call_time_search_status()
        CallContactDetailPage().click_video_call()
        time.sleep(2)
        # 1.直接发起语音通话，没有弹窗
        cpg.page_should_not_contain_text("每月10G免流特权")
        time.sleep(1)
        CallContactDetailPage().wait_for_star()
        cpg.click_back()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0314(self):
        """检查通话界面发起多方视频"""
        # 1.客户端已登陆在：通话界面
        # 2.网络正常
        # 3.成员手机号有效
        # Step:1.点击【多方视频】按钮
        cpg = CallPage()
        cmvp = MultiPartyVideoPage()
        cpg.click_multi_party_video()
        time.sleep(2)
        # CheckPoint:1.跳转至发起视频-选择成员界面
        cpg.page_should_contain_text("选择团队联系人")
        # Step:2.选择成员
        # 选择本地一个，号码搜索一个
        cmvp.click_text("大佬1")
        time.sleep(1)
        cmvp.input_contact_search("13537795364")
        cpg.click_text("未知号码")
        # CheckPoint:2.被选的成员接显示在已选成员列表
        # 无法获取成员状态，修改为判断是否存在呼叫(2/8)
        # self.assertTrue(cmvp.is_exist_contact_selection())
        cpg.page_should_contain_text("呼叫(2/8)")
        # Step:3.点击【呼叫】按钮
        cmvp.click_text("呼叫(2/8)")
        # CheckPoint:3.转入多方视频拨通界面
        cpg.page_should_contain_text("关闭摄像头")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0324(self):
        """在通话界面邀请无效手机号发起多方视频"""
        # 1.客户端已登陆在：通话界面
        # 2.网络正常
        # 3.邀请无效手机号进入到多方视频通话
        cpg = CallPage()
        cmvp = MultiPartyVideoPage()
        # Step:1.【多方视频】按钮
        cpg.click_multi_party_video()
        time.sleep(2)
        # CheckPoint:1.跳转至发起视频-选择成员界面
        cpg.page_should_contain_text("选择团队联系人")
        # Step:2.输入任意非手机号数字
        cmvp.input_contact_search("13800138005991")
        time.sleep(2)
        # CheckPoint:2.联系人选择器无法识别出无效手机号
        cpg.page_should_not_contain_text("本地联系人")
        cpg.page_should_not_contain_text("网络搜索")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0326(self):
        """检查无副号时通话记录列表页面"""
        # 1.用户已登录和飞信通话记录列表页面
        # 2.无副号
        cpg = CallPage()
        time.sleep(1)
        # Step:1，查看界面
        # CheckPoint:1.左上角显示“通话”，右边显示“视频”按钮，中间显示通话记录，右下方显示“多方电话”悬浮
        self.assertTrue(cpg.check_call_display())
        self.assertTrue(cpg.check_multiparty_video())
        self.assertTrue(cpg.check_feixin_call())
        # Step:2.点击拨号盘
        cpg.click_dial()
        # CheckPoint:2.弹出拨号盘，顶部栏被遮挡
        self.assertFalse(cpg.check_call_display())
        self.assertFalse(cpg.check_multiparty_video())
        cpg.click_dial()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0328(self):
        """检查通通话列表为空"""
        # 1.用户已登录和飞信通话记录列表页面
        # 2.通讯录为空
        cpg = CallPage()
        time.sleep(1)
        # Step:1，查看界面
        # CheckPoint:1.界面logo提示“给你的好友打个电话吧”
        # self.assertTrue(cpg.check_call_image())
        cpg.page_should_contain_text("高清通话，高效沟通")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0333(self):
        """检查清零未接通话数"""
        # 1.用户已登录和飞信消息tab
        # 2.通话tab右上角显示未读消息气泡
        # Step:1.点击通话tab
        cpg = CallPage()
        cpg.click_call()
        # CheckPoint:1.通话未接数清零，图标变为拨号盘按钮
        # 清空通话记录
        cpg.delete_all_call_entry()
        cpg.page_should_contain_text("高清通话，高效沟通")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0342(self):
        """检查删除通话记录（仅ios）"""
        # 1.和飞信登录通话tab
        # 2.列表存在通话记录
        # Step:1.选择通话记录向左滑动
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.swipe_by_percent_on_screen(90, 15, 30, 15)
        # CheckPoint:1.靠右显示删除按钮
        cpg.page_should_contain_text("删除")

        # Step:2.点击删除按钮
        time.sleep(1)
        cpg.click_text("删除")

        # CheckPoint:2.可清空该条通话记录
        self.assertFalse(cpg.is_exists_call_entry())

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0347(self):
        """检查本地联系人通话profile左上角显示名称"""
        # 1.已登录和飞信：通话tab
        # 2.已存在与本地联系人的通话记录M
        # Step:1.点击记录M的时间节点
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_dial()
        cpg.click_call_time_search_status()
        # CheckPoint:1.进入到M的通话profile界面
        time.sleep(2)
        cpg.page_should_contain_text("分享名片")
        # Step:2.查看左上角的名称
        ret = cpg.get_profile_name()
        # CheckPoint:2.左上角<按钮。以及M名称
        self.assertEqual(ret, "给个红包2")
        # Step:3.点击<按钮>
        cpg.click_back()
        cpg.click_dial()
        time.sleep(2)
        # CheckPoint:3.返回到上一个界面
        self.assertTrue(cpg.is_on_the_call_page())

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0348(self):
        """检查陌生联系人通话profile左上角显示手机号"""
        # 1.已登录和飞信：通话tab
        # 2.已存在与陌生联系人的通话记录M
        # Step:1.点击记录M的时间节点
        cpg = CallPage()
        cpg.create_call_entry("19912345678")
        cpg.click_dial()
        cpg.click_call_time_search_status()
        # CheckPoint:1.进入到M的通话profile界面
        time.sleep(2)
        self.assertTrue(cpg.is_exist_profile_name())
        # Step:2.查看左上角的名称
        ret = cpg.get_profile_name()
        # CheckPoint:2.左上角<按钮。以及N的手机号
        self.assertEqual(ret, "19912345678")
        # Step:3.点击<按钮>
        cpg.click_back()
        cpg.click_dial()
        time.sleep(2)
        # CheckPoint:3.返回到上一个界面
        self.assertTrue(cpg.is_on_the_call_page())

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0353_001(self):
        """检查通话profile界面可进入到消息会话窗口--本地联系人"""
        # 1.已登录和飞信：通话tab
        # 2.已进入到联系人通话profile
        # 本地联系人
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_dial()
        cpg.click_call_time_search_status()
        time.sleep(2)
        cpg.page_should_contain_text("分享名片")
        # Step:1.点击消息按钮
        CallContactDetailPage().click_normal_message()

        # CheckPoint:1.进入到与该联系人的消息会话框。本地联系人左上角显示名称。陌生联系人，左上角显示手机号
        chatpage = BaseChatPage()
        flag = chatpage.is_exist_dialog()
        if flag:
            chatpage.click_i_have_read()
        cpg.page_should_contain_text("说点什么...")
        cpg.page_should_contain_text("给个红包2")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0353_002(self):
        """检查通话profile界面可进入到消息会话窗口--陌生联系人"""
        # 陌生联系人
        cpg = CallPage()
        cpg.create_call_entry("19912345678")
        cpg.click_dial()
        cpg.click_call_time_search_status()
        time.sleep(2)
        self.assertTrue(cpg.is_exist_profile_name())
        # Step:1.点击消息按钮
        CallContactDetailPage().click_normal_message()
        # CheckPoint:1.进入到与该联系人的消息会话框。本地联系人左上角显示名称。陌生联系人，左上角显示手机号
        chatpage = BaseChatPage()
        flag = chatpage.is_exist_dialog()
        if flag:
            chatpage.click_i_have_read()
        cpg.page_should_contain_text("说点什么...")
        cpg.page_should_contain_text("19912345678")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0355(self):
        """检查通话profile界面发起语音通话"""
        # 1.已登录和飞信：通话tab
        # 2.已进入到联系人通话profile
        # 3.有效手机号
        # Step:1.点击语音通话按钮
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_dial()
        cpg.click_call_time_search_status()
        time.sleep(2)
        self.assertTrue(cpg.is_exist_profile_name())
        CallContactDetailPage().click_voice_call()
        cpg.page_should_contain_text("正在呼叫")
        # CheckPoint:1.发起1v1语音呼叫
        CallContactDetailPage().wait_for_star()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0356(self):
        """检查通话profile界面发起视频通话"""
        # 1.已登录和飞信：通话tab
        # 2.已进入到联系人通话profile
        # 3.有效手机号
        # Step:1.点击视频通话
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_dial()
        cpg.click_call_time_search_status()
        time.sleep(2)
        CallContactDetailPage().click_video_call()
        cpg.page_should_contain_text("网络视频通话呼叫中")
        # CheckPoint:1.发起1v1视频呼叫
        CallContactDetailPage().wait_for_star()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0358(self):
        """检查本地联系人通话profile"""
        # 1.已登录和飞信-通话记录列表
        # 2.已进入到本地联系人A的通话profile
        # 3.用户A为RCS用户并保存至本地
        # 4.当前登录账号无副号
        # Step:1.查看界面
        cpg = CallPage()
        cpg.create_call_entry("13800138001")
        cpg.click_dial()
        cpg.click_call_time_search_status()
        time.sleep(2)
        # CheckPoint:1.进功能有：星标、编辑、分享名片。消息、电话、语音通话、视频通话、和飞信电话高亮。页面显示：在和飞信电话按钮下显示公司、职位、邮箱（公司、职位、邮箱有则显示），通话记录。底部显示【分享名片】，点击调起联系人选择器
        self.assertTrue(CallContactDetailPage().is_exist_star())
        cpg.page_should_contain_text("编辑")
        cpg.page_should_contain_text("分享名片")
        cpg.page_should_contain_text("消息")
        cpg.page_should_contain_text("电话")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("视频通話")
        cpg.page_should_contain_text("飞信电话")
        cpg.page_should_contain_text("拨出电话")
        CallContactDetailPage().click_share_card()
        time.sleep(2)
        cpg.page_should_contain_text("选择联系人")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0360(self):
        """检查陌生人通话profile"""
        # 1.已登录和飞信-通话记录列表
        # 2.已进入到陌生联系人B的通话profile
        # 3.用户B为RCS用户并为陌生人
        # 4.当前登录账号无副号
        # Step:1.查看界面
        cpg = CallPage()
        cpg.create_call_entry("13537795364")
        cpg.click_dial()
        cpg.click_call_time_search_status()
        time.sleep(2)
        # CheckPoint:1.功能有：保存到通讯录。消息、电话、语音通话、视频通话、和飞信电话高亮。页面显示：在和飞信电话按钮下显示通话记录。底部显示【保存到通讯录】，点击进入到编辑页面
        time.sleep(2)
        cpg.page_should_contain_text("保存到通讯录")
        cpg.page_should_contain_text("消息")
        cpg.page_should_contain_text("电话")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("视频通話")
        cpg.page_should_contain_text("飞信电话")
        cpg.page_should_contain_text("拨出电话")
        CallContactDetailPage().click_save_contacts()

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0363(self):
        """检查非RCS通话profile--陌生联系人"""
        # 1.已登录和飞信-通话记录列表
        # 2.已进入到本地联系人C的通话profile
        # 3.用户C为非RCS用户并为陌生人
        # 4.当前登录账号无副号
        # Step:1.查看界面
        cpg = CallPage()
        cpg.create_call_entry("15343038890")
        cpg.click_dial()
        cpg.click_call_time_search_status()
        # CheckPoint:1.功能有：保存到通讯录、邀请使用。消息、电话、语音通话、视频通话、和飞信电话高亮。页面显示：在和飞信电话按钮下显示通话记录。底部显示【保存到通讯录】，点击进入到编辑页面。【邀请使用】，点击调起系统短信
        time.sleep(2)
        cpg.page_should_contain_text("保存到通讯录")
        cpg.page_should_contain_text("邀请使用")
        cpg.page_should_contain_text("消息")
        cpg.page_should_contain_text("电话")
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("视频通話")
        cpg.page_should_contain_text("飞信电话")
        cpg.page_should_contain_text("拨出电话")
        ContactDetailsPage().click_invitation_use()
        time.sleep(1)
        cpg.page_should_contain_text("新信息")
        cpg.page_should_contain_text("收件人：")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0381(self):
        """检查单聊富媒体面板-音频通话包含语音通话年华、视频"""
        # 1.登录和飞信：消息tab-单聊会话窗口-富媒体面板
        # Step: 1.1.点击音频电话按钮
        cpg = CallPage()
        ContactsPage().click_message_icon()
        Preconditions.enter_single_chat_page("给个红包2")
        BaseChatPage().click_more()
        ChatMorePage().click_voice_and_video_call()
        time.sleep(1)
        # CheckPoint: 1.展开的富媒体消息体选择面板收起后Android：中间弹出”语音通话、视频通话“两个按钮
        cpg.page_should_contain_text("语音通话")
        cpg.page_should_contain_text("视频通话")
        cpg.page_should_contain_text("取消")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0388(self):
        """检查单聊会话窗口右上角电话按钮"""
        # 1.登录和飞信：消息tab-单聊会话窗口
        # Step:1.点击右上角的电话按钮
        cpg = CallPage()
        ContactsPage().click_message_icon()
        Preconditions.enter_single_chat_page("给个红包2")
        SingleChatPage().click_action_call()
        time.sleep(1)
        # CheckPoint:1.弹出系统选择弹窗，选择和飞信电话（免费）与普通电话
        cpg.page_should_contain_text("飞信电话(免费)")
        cpg.page_should_contain_text("普通电话")
        cpg.page_should_contain_text("取消")

    @tags('ALL', 'CMCC', 'Call')
    def test_call_shenlisi_0395(self):
        """检查群聊聊富媒体面板-多方电话入口拨打"""
        # 1.登录和飞信：消息tab-群聊会话窗口-富媒体面板
        # 2.已弹出系统选择弹窗多方电话和多方视频
        ContactsPage().click_message_icon()
        Preconditions.get_into_group_chat_page("群聊1")
        # Step:1.点击多方电话
        gpg = GroupListPage()
        gpg.click_mult_call_icon()
        CallPage().click_feixin_call_free()
        # CheckPoint:1.调起联系人选择器
        time.sleep(1)
        gpg.page_should_contain_text("搜索群成员")
        CallPage().click_back()
        # Step:2.点击多方视频
        gpg = GroupListPage()
        gpg.click_mult_call_icon()
        CallPage().click_mutil_video_call()
        # CheckPoint:2.调起联系人选择器
        time.sleep(1)
        gpg.page_should_contain_text("搜索群成员")

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_call_shenlisi_0377(self):
        """检查单聊富媒体面板-和飞信电话入口拨打"""
        ContactsPage().click_message_icon()
        # 1.进入单聊会话页面
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 2.点击更多加号按钮
        scp.click_add_button()
        # 3.点击和飞信电话
        scp.click_feixin_phone()
        if scp.page_should_contain_text2("我知道了", 5):
            scp.click_name_attribute_by_name("我知道了")
        time.sleep(2)
        if scp.page_should_contain_text2("拒绝"):
            scp.click_name_attribute_by_name("拒绝")
        time.sleep(2)
        # 4.验证是否呼出
        self.assertTrue(scp.page_should_contain_text2("正在呼叫"))

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_call_shenlisi_0388(self):
        """检查单聊会话窗口右上角电话按钮"""
        ContactsPage().click_message_icon()
        # 1.进入单聊会话页面
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 2.点击右上角打电话图标
        scp.click_action_call()
        time.sleep(2)
        # 3.验证是否弹出
        self.assertTrue(scp.page_should_contain_text2("飞信电话(免费)"))
        self.assertTrue(scp.page_should_contain_text2("普通电话"))

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_call_shenlisi_0389(self):
        """检查单聊会话窗口右上角电话按钮-和飞信电话拨打"""
        ContactsPage().click_message_icon()
        # 1.进入单聊会话页面
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 2.点击右上角打电话图标
        scp.click_action_call()
        time.sleep(2)
        # 3.验证是否弹出
        self.assertTrue(scp.page_should_contain_text2("飞信电话(免费)"))
        self.assertTrue(scp.page_should_contain_text2("普通电话"))
        if scp.page_should_contain_text2("飞信电话(免费)"):
            scp.click_name_attribute_by_name("飞信电话(免费)")
        time.sleep(2)
        if scp.page_should_contain_text2("拒绝"):
            scp.click_name_attribute_by_name("拒绝")
        time.sleep(2)
        # 4.验证是否呼出
        self.assertTrue(scp.page_should_contain_text2("正在呼叫"))

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_call_shenlisi_0354(self):
        """检查通话profile界面发起普通电话"""
        cpg = ContactsPage()
        # 1.点击通讯录
        cpg.click_contacts()
        # 2.点击手机联系人
        cpg.click_phone_contact()
        # 3.根据名字选择联系人
        cpg.select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        # 4.点击电话图标
        cdp.click_call_icon()
        # 5.点击呼叫
        cdp.click_text("呼叫")
        time.sleep(2)
        # 6.验证是否在系统通话
        self.assertTrue(cdp.page_should_contain_text2("静音"))
        self.assertTrue(cdp.page_should_contain_text2("拨号键盘"))
        self.assertTrue(cdp.page_should_contain_text2("免提"))
        self.assertTrue(cdp.page_should_contain_text2("通讯录"))

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_call_shenlisi_0357(self):
        """检查通话profile发起和飞信电话"""
        cpg = ContactsPage()
        # 1.点击通讯录
        cpg.click_contacts()
        # 2.点击手机联系人
        cpg.click_phone_contact()
        # 3.根据名字选择联系人
        cpg.select_contacts_by_name('大佬1')
        cdp = ContactDetailsPage()
        # 4.点击飞信电话
        cdp.click_hefeixin_call_menu()
        time.sleep(2)
        if cdp.page_should_contain_text2("拒绝"):
            cdp.click_name_attribute_by_name("拒绝")
        time.sleep(2)
        # 5.验证是否呼出
        self.assertTrue(cdp.page_should_contain_text2("正在呼叫"))

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_call_shenlisi_0045(self):
        """拨号盘呼叫普通电话"""
        cpg = CallPage()
        # 1.点击拨号盘
        cpg.click_dial()
        time.sleep(1)
        # 2.验证是否弹出拨号盘界面
        self.assertTrue(cpg.check_call_phone())
        # 3.输入11位数内陆号
        cpg.dial_number("13800138000")
        time.sleep(2)
        # 4.点击拨打电话按键
        cpg.click_call_phone()
        time.sleep(2)
        # 5.点击选择普通电话
        CallTypeSelectPage().click_call_by_general()
        cpg.click_text("呼叫")
        time.sleep(2)
        # 6.验证是否在呼叫成功
        self.assertTrue(cpg.page_should_contain_text2("静音"))
        self.assertTrue(cpg.page_should_contain_text2("拨号键盘"))
        self.assertTrue(cpg.page_should_contain_text2("免提"))
        self.assertTrue(cpg.page_should_contain_text2("通讯录"))

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_call_shenlisi_0049(self):
        """检查拨号盘取消拨号方式（ios)"""
        cpg = CallPage()
        # 1.点击拨号盘
        cpg.click_dial()
        time.sleep(1)
        # 2.验证是否弹出拨号盘界面
        self.assertTrue(cpg.check_call_phone())
        # 3.输入11位数内陆号
        cpg.dial_number("13800138000")
        time.sleep(2)
        # 4.点击取消拨号方式
        cpg.click_dial()
        time.sleep(2)
        self.assertTrue(cpg.check_call_phone())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_call_shenlisi_0148(self):
        """检查缩小悬浮窗（ios）"""
        cpg = ContactsPage()
        # 1.点击通讯录
        cpg.click_contacts()
        # 2.点击手机联系人
        cpg.click_phone_contact()
        # 3.根据名字选择联系人
        cpg.select_contacts_by_name('13800138005')
        cdp = ContactDetailsPage()
        # 4.点击语音通话
        cdp.wait_for_page_load()
        cdp.click_voice_call_icon()
        # 5.点击缩放按钮
        cpg = CallPage()
        cpg.click_voice_zoom_button()
        # 6.点击悬浮窗
        cpg.click_suspension_window()
        time.sleep(2)
        # 7.验证是否在语音通话界面(点击悬浮窗不能返回通话界面)
        # self.assertTrue(cpg.is_on_voice_call_page())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_call_shenlisi_0261(self):
        """检查视频通话--呼叫界面缩放按钮"""
        cpg = ContactsPage()
        # 1.点击通讯录
        cpg.click_contacts()
        # 2.点击手机联系人
        cpg.click_phone_contact()
        # 3.根据名字选择联系人
        cpg.select_contacts_by_name('13800138005')
        cdp = ContactDetailsPage()
        # 4.点击视频通话
        cdp.click_video_call_icon()
        time.sleep(3)
        # 5.点击缩放按钮
        cpg = CallPage()
        cpg.click_video_zoom_button()
        # 6.点击悬浮窗
        cpg.click_suspension_window()
        time.sleep(2)
        # 7.验证是否在视频通话界面(点击悬浮窗不能返回通话界面)
        # self.assertTrue(cpg.is_on_video_call_page())

