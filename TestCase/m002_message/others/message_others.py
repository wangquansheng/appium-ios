import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from preconditions.BasePreconditions import WorkbenchPreconditions
from pages import *


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        # 如果在消息页，不做任何操作
        mp = MessagePage()
        if mp.is_on_this_page():
            return
        else:
            try:
                current_mobile().launch_app()
                mp.wait_for_page_load()
            except:
                # 进入一键登录页
                Preconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                Preconditions.login_by_one_key_login()


class MessageOthersTotalTest(TestCase):
    """消息其他模块"""

    @classmethod
    def setUpClass(cls):

        Preconditions.select_mobile('IOS-移动')
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits(name, number)
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                flag1 = True
            except:
                fail_time1 += 1
            if flag1:
                break

    def default_setUp(self):

        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangcaizui_A_0184(self):
        """聊天会话窗口的批量选择器页面展示"""

        # 进入群聊聊天会话页面
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 确保存在多条消息体
        for i in range(3):
            gcp.input_text_message(str(i + 1))
            gcp.click_send_button()
        # 消息会话框中长按消息体
        gcp.press_last_text_message()
        # 1.弹出操作列表
        self.assertEquals(gcp.page_should_contain_text2("多选"), True)
        # 点击“多选”
        gcp.click_accessibility_id_attribute_by_name("多选")
        # 2.进入聊天会话窗口的批量选择器页面
        self.assertEquals(gcp.page_should_contain_text2("已选择"), True)
        # 3.页面显示，顶部导航栏为左上角的【×】关闭按钮，标题右侧显示已勾选消息气泡的数量 有勾选消息时，左上角文案展示为：已选择+数量
        self.assertEquals(gcp.is_exists_element_by_text("多选关闭按钮"), True)
        self.assertEquals(gcp.is_exists_element_by_text("已选择"), True)
        self.assertEquals(gcp.is_exists_element_by_text("已选择数量"), True)
        # 取消勾选最后一条消息
        gcp.click_element_by_text("多选最后一条消息勾选框")
        # 未选择任何消息时，左上角文案展示为：未选择，底部有删除，转发两按钮
        self.assertEquals(gcp.is_exists_element_by_text("未选择"), True)
        self.assertEquals(gcp.is_exists_element_by_text("多选删除按钮"), True)
        self.assertEquals(gcp.is_exists_element_by_text("多选转发按钮"), True)
        # 勾选最后一条消息
        gcp.click_element_by_text("多选最后一条消息勾选框")
        # 当有选择消息体时，底部两个操作按钮呈高亮，可操作使用
        self.assertEquals(gcp.is_enabled_element_by_text("多选删除按钮"), True)
        self.assertEquals(gcp.is_enabled_element_by_text("多选转发按钮"), True)
        # 取消勾选最后一条消息
        gcp.click_element_by_text("多选最后一条消息勾选框")
        # 当未选择任何消息体时，点击删除/转发无效，两个操作按钮呈灰色
        self.assertEquals(gcp.is_enabled_element_by_text("多选删除按钮"), False)
        self.assertEquals(gcp.is_enabled_element_by_text("多选转发按钮"), False)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangcaizui_A_0191(self):
        """转发默认选中项（1条）—删除"""

        # 进入单聊聊天会话页面
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        # 确保存在多条消息体
        for i in range(3):
            scp.input_text_message(str(i + 1))
            scp.send_text()
        # 获取消息记录数量
        message_numbers = scp.get_message_record_number()
        # 消息会话框中长按消息体
        scp.press_last_text_message()
        # 1.弹出操作列表
        self.assertEquals(scp.page_should_contain_text2("复制"), True)
        # 没找到多选，则显示更多
        if not scp.page_should_contain_text2("多选", 3):
            scp.click_accessibility_id_attribute_by_name("显示更多项目")
        # 点击“多选”
        scp.click_accessibility_id_attribute_by_name("多选")
        # 2.进入聊天会话窗口的批量选择器页面
        self.assertEquals(scp.page_should_contain_text2("已选择"), True)
        # 查看页面选中的消息体数量
        self.assertEquals(scp.get_element_value_by_text("已选择数量"), "1")
        # 3.默认选中长按的那一条消息体
        self.assertEquals(scp.get_element_value_by_text("多选最后一条消息勾选框"), "1")
        # 点击删除
        scp.click_element_by_text("多选删除按钮")
        # 4.弹出确认提示框
        self.assertEquals(scp.page_should_contain_text2("删除"), True)
        # 点击确定
        scp.click_accessibility_id_attribute_by_name("删除")
        # 5.删除成功，聊天会话中toast提示“删除成功”(toast难以抓取，不稳定，间接验证)
        # self.assertEquals(scp.page_should_contain_text2("删除成功"), True)
        time.sleep(2)
        self.assertEquals(scp.is_exists_element_by_text("多选删除按钮"), False)
        # 查看聊天会话窗口
        scp.wait_for_page_load()
        # 获取新的消息记录数量
        new_message_numbers = scp.get_message_record_number()
        # 6.删除掉的消息体已删除成功(由于文本消息的文本无法定位，采用间接验证)
        self.assertEquals(new_message_numbers, message_numbers - 1)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangcaizui_A_0212(self):
        """删除选中的消息体"""

        # 进入单聊聊天会话页面
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        # 确保存在多条消息体
        for i in range(3):
            scp.input_text_message(str(i + 1))
            scp.send_text()
        # 获取消息记录数量
        message_numbers = scp.get_message_record_number()
        # 消息会话框中长按消息体
        scp.press_last_text_message()
        # 1.弹出操作列表
        self.assertEquals(scp.page_should_contain_text2("复制"), True)
        # 没找到多选，则显示更多
        if not scp.page_should_contain_text2("多选", 3):
            scp.click_accessibility_id_attribute_by_name("显示更多项目")
        # 点击“多选”
        scp.click_accessibility_id_attribute_by_name("多选")
        # 2.进入聊天会话窗口的批量选择器页面
        self.assertEquals(scp.page_should_contain_text2("已选择"), True)
        # 点击其他消息体的复选框/消息气泡/头像
        scp.click_element_by_text("多选倒数第二条消息勾选框")
        # 3.被点到的相对应消息体被选中
        self.assertEquals(scp.get_element_value_by_text("多选最后一条消息勾选框"), "1")
        self.assertEquals(scp.get_element_value_by_text("多选倒数第二条消息勾选框"), "1")
        # 点击删除
        scp.click_element_by_text("多选删除按钮")
        # 4.弹出确认提示框
        self.assertEquals(scp.page_should_contain_text2("删除"), True)
        # 点击确定
        scp.click_accessibility_id_attribute_by_name("删除")
        # 5.删除成功，聊天会话中toast提示“删除成功”(toast难以抓取，不稳定，间接验证)
        # self.assertEquals(scp.page_should_contain_text2("删除成功"), True)
        time.sleep(2)
        self.assertEquals(scp.is_exists_element_by_text("多选删除按钮"), False)
        # 查看聊天会话窗口
        scp.wait_for_page_load()
        # 获取新的消息记录数量
        new_message_numbers = scp.get_message_record_number()
        # 6.删除掉的消息体已删除成功(由于文本消息的文本无法定位，采用间接验证)
        self.assertEquals(new_message_numbers, message_numbers - 2)

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangcaizui_A_0260(self):
        """消息送达状态显示开关入口"""

        mp = MessagePage()
        # 点击我-设置-消息设置
        mp.open_me_page()
        me_page = MePage()
        me_page.wait_for_page_load()
        me_page.click_accessibility_id_attribute_by_name("设置")
        msp = MeSetUpPage()
        msp.wait_for_page_load()
        msp.click_accessibility_id_attribute_by_name("消息")
        # 1.显示消息设置页，显示【消息送达状态显示】开关，默认开启
        self.assertEquals(msp.get_no_disturbing_btn_text(), "1")

    @staticmethod
    def tearDown_test_msg_huangcaizui_A_0260():
        """恢复环境"""

        try:
            fail_time = 0
            while fail_time < 5:
                try:
                    Preconditions.make_already_in_message_page()
                    mp = MessagePage()
                    # 点击我-设置-消息设置
                    mp.open_me_page()
                    me_page = MePage()
                    me_page.wait_for_page_load()
                    me_page.click_accessibility_id_attribute_by_name("设置")
                    msp = MeSetUpPage()
                    msp.wait_for_page_load()
                    msp.click_accessibility_id_attribute_by_name("消息")
                    # 确保消息送达状态显示开关打开
                    if msp.get_no_disturbing_btn_text() == "0":
                        msp.click_no_disturbing_button()
                        time.sleep(3)
                    return
                except:
                    fail_time += 1
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangcaizui_A_0279(self):
        """从通话——拨号盘——输入陌生号码——进入单聊页面"""

        mp = MessagePage()
        mp.open_call_page()
        call_page = CallPage()
        # 等待通话页面加载
        call_page.wait_for_page_load()
        # 点击拨号盘
        call_page.click_accessibility_id_attribute_by_name("拨号盘")
        # 1.调起拨号盘，输入陌生号码
        self.assertEquals(call_page.is_exists_element_by_text("收起键盘"), True)
        numbers = "19899996666"
        for i in numbers:
            call_page.click_element_by_text("拨号键" + str(i))
        # 点击上方发送消息
        call_page.click_accessibility_id_attribute_by_name("发送消息")
        scp = SingleChatPage()
        # 2.进入单聊页面
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'LXD_IOS')
    def test_msg_huangcaizui_A_0280(self):
        """从通话——拨号盘——数字搜索手机联系人——进入单聊页面"""

        mp = MessagePage()
        mp.open_call_page()
        call_page = CallPage()
        # 等待通话页面加载
        call_page.wait_for_page_load()
        # 点击拨号盘
        call_page.click_accessibility_id_attribute_by_name("拨号盘")
        # 1.调起拨号盘
        self.assertEquals(call_page.is_exists_element_by_text("收起键盘"), True)
        # 任意输入一个或多个数字
        numbers = "13800138005"
        for i in numbers:
            call_page.click_element_by_text("拨号键" + str(i))
        # 2.搜索出对应的手机联系人
        self.assertEquals(call_page.is_exists_accessibility_id_attribute_by_name("大佬1"), True)
        # 任意选择一联系人，点击右边通话详情按钮
        call_page.click_element_by_text("通话详情按钮")
        cdp = ContactDetailsPage()
        # 3.进入联系人详情页面
        cdp.wait_for_page_load()
        # 点击消息
        cdp.click_message_icon()
        scp = SingleChatPage()
        # 4.进入单聊页面
        scp.wait_for_page_load()