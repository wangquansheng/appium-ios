
import time

from library.core.TestCase import TestCase

from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags

from pages import *
from pages.me.MePayment import MePayPage

from preconditions.BasePreconditions import LoginPreconditions
import warnings

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': 'iphone',
    'IOS-移动-移动': 'M960BDQN229CHiphone8',
}


class Preconditions(LoginPreconditions):
    """
    分解前置条件
    """
    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def disconnect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(category)
        client.disconnect_mobile()
        return client


    @staticmethod
    def create_contacts(name, number):
        """
        导入联系人数据
        :param name:
        :param number:
        :return:
        """
        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        try:
            contacts_page.wait_for_page_load()
            contacts_page.open_contacts_page()
        except:
            Preconditions.make_already_in_message_page(reset=False)
            contacts_page.open_contacts_page()
        # 创建联系人
        contacts_page.click_search_box()
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword(name)
        contact_search.click_back()
        contacts_page.click_add()
        create_page = CreateContactPage()
        create_page.hide_keyboard_if_display()
        create_page.create_contact(name, number)
        detail_page.wait_for_page_load()
        detail_page.click_back_icon()

    @staticmethod
    def take_logout_operation_if_already_login():
        """已登录状态，执行登出操作"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()

        me = MePage()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.click_setting_menu()

        setting = SettingPage()
        setting.scroll_to_bottom()
        setting.click_logout()
        setting.click_ok_of_alert()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def terminate_app():
        """
        强制关闭app,退出后台
        :return:
        """
        app_id = current_driver().desired_capability['appPackage']
        current_mobile().termiate_app(app_id)

    @staticmethod
    def background_app():
        """后台运行"""
        current_mobile().press_home_key()

    @staticmethod
    def activate_app(app_id=None):
        """激活APP"""
        if not app_id:
            app_id = current_mobile().driver.desired_capabilities['appPackage']
        current_mobile().driver.activate_app(app_id)


class MyPayPageTest(TestCase):
    """和包支付"""

    def default_setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('IOS-移动')
        Preconditions.make_already_in_message_page()
        MessagePage().open_me_page()
        time.sleep(2)

    def default_tearDown(self):
        Preconditions.disconnect_mobile(REQUIRED_MOBILES['IOS-移动'])

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_084(self):
        """授权-确认授权"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.验证是否在和包支付页面
        self.assertTrue(mpp.is_on_paymentn_page())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_089(self):
        """已授权，清除客户端缓存，再授权"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.验证功能是否可以用(是否可以点击)
        self.assertTrue(mpp.bank_card_btn_is_enabled())
        self.assertTrue(mpp.cash_bonus_btn_is_enabled())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_109(self):
        """和包余额页面元素检查"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击和包余额
        mpp.click_balance()
        time.sleep(2)
        # 4.验证元素是否存在
        self.assertTrue(mpp.check_if_element_exist())
        self.assertTrue(mpp.check_if_balance_element_exist())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_109(self):
        """无现金余额提现"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击和包余额
        mpp.click_balance()
        time.sleep(2)
        # 4.点击提现
        mpp.click_cash_withdrawal()
        # 5.验证是否提示"提现余额需大于0"
        self.assertTrue(mpp.page_should_contain_text2("提现余额需大于0"))

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_144(self):
        """银行卡页面展示"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击银行卡
        mpp.click_bank_card()
        # 4.验证是否显示新添银行卡入口
        time.sleep(5)
        self.assertTrue(mpp.is_exist_binding_new_bank_cards())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_146(self):
        """银行卡页面填写0-14位银行卡号"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击银行卡
        mpp.click_bank_card()
        # 4.点击绑定新银行卡
        time.sleep(5)
        mpp.click_binding_new_bank_cards()
        # 5.输入银行卡号
        mpp.input_bank_card_number("111111111111")
        # 6.验证下一步是否可以点击
        self.assertFalse(mpp.next_step_btn_is_enabled())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_147(self):
        """银行卡页面填写15-19位无效的银行卡号"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击银行卡
        mpp.click_bank_card()
        # 4.点击绑定新银行卡
        time.sleep(5)
        mpp.click_binding_new_bank_cards()
        # 5.输入银行卡号
        mpp.input_bank_card_number("1111111111111111")
        # 6.点击下一步
        mpp.click_next_step()
        time.sleep(5)
        # 7.验证是否提示您的银行卡号有误，请核对后重试
        self.assertTrue(mpp.is_exist_error())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_148(self):
        """银行预留信息页面仅填写持卡人姓名"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击银行卡
        mpp.click_bank_card()
        # 4.点击绑定新银行卡
        time.sleep(5)
        mpp.click_binding_new_bank_cards()
        # 5.输入银行卡号
        mpp.input_bank_card_number("6214180300001315198")
        # 6.点击下一步
        mpp.click_next_step()
        # 7.持卡人姓名
        mpp.input_name("测试")
        # 8.验证下一步是否可以点击
        self.assertFalse(mpp.next_step_btn_is_enabled())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_149(self):
        """行预留信息页面仅填写持卡人身份证号"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击银行卡
        mpp.click_bank_card()
        # 4.点击绑定新银行卡
        time.sleep(5)
        mpp.click_binding_new_bank_cards()
        # 5.输入银行卡号
        mpp.input_bank_card_number("6214180300001315198")
        # 6.点击下一步
        mpp.click_next_step()
        # 7.输入持卡人身份证号
        mpp.input_ID_card("441426199008112345")
        # 8.验证下一步是否可以点击
        self.assertFalse(mpp.next_step_btn_is_enabled())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_150(self):
        """银行预留信息页仅填写手机号"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击银行卡
        mpp.click_bank_card()
        # 4.点击绑定新银行卡
        time.sleep(5)
        mpp.click_binding_new_bank_cards()
        # 5.输入银行卡号
        mpp.input_bank_card_number("6214180300001315198")
        # 6.点击下一步
        mpp.click_next_step()
        # 7.输入持卡人手机号
        mpp.input_phone_number("14775970982")
        # 8.验证下一步是否可以点击
        self.assertFalse(mpp.next_step_btn_is_enabled())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_151(self):
        """银行预留信息页填写持卡人姓名与手机号&输入小于15位的身份证号"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击银行卡
        mpp.click_bank_card()
        # 4.点击绑定新银行卡
        time.sleep(5)
        mpp.click_binding_new_bank_cards()
        # 5.输入银行卡号
        mpp.input_bank_card_number("6214180300001315198")
        # 6.点击下一步
        mpp.click_next_step()
        # 7.输入持卡人姓名，身份证号，手机号
        mpp.input_name("测试")
        # 输入小于15位的身份证号
        mpp.input_ID_card("44142619900811")
        mpp.input_phone_number("14775970982")
        # 8.验证下一步是否可以点击
        self.assertFalse(mpp.next_step_btn_is_enabled())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_152(self):
        """银行预留信息页填写持卡人姓名与手机号&输入大于15位&小于18位的身份证号"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击银行卡
        mpp.click_bank_card()
        # 4.点击绑定新银行卡
        time.sleep(5)
        mpp.click_binding_new_bank_cards()
        # 5.输入银行卡号
        mpp.input_bank_card_number("6214180300001315198")
        # 6.点击下一步
        mpp.click_next_step()
        # 7.输入持卡人姓名，身份证号，手机号
        mpp.input_name("测试")
        # 输入大于15位&小于18位的身份证号
        mpp.input_ID_card("4414261990081112")
        mpp.input_phone_number("14775970982")
        # 8.验证下一步是否可以点击
        self.assertFalse(mpp.next_step_btn_is_enabled())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_153(self):
        """银行预留信息页-填写持卡人姓名&身份证号&小于11位手机号"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击银行卡
        mpp.click_bank_card()
        # 4.点击绑定新银行卡
        time.sleep(5)
        mpp.click_binding_new_bank_cards()
        # 5.输入银行卡号
        mpp.input_bank_card_number("6214180300001315198")
        # 6.点击下一步
        mpp.click_next_step()
        # 7.输入持卡人姓名，身份证号，手机号
        mpp.input_name("测试")
        mpp.input_ID_card("441426199008111234")
        # 输入小于11位手机号
        mpp.input_phone_number("1477597098")
        # 8.验证下一步是否可以点击
        self.assertFalse(mpp.next_step_btn_is_enabled())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_154(self):
        """银行预留信息页填写持卡人姓名&身份证号&手机号，未勾选协议"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击银行卡
        mpp.click_bank_card()
        # 4.点击绑定新银行卡
        time.sleep(5)
        mpp.click_binding_new_bank_cards()
        # 5.输入银行卡号
        mpp.input_bank_card_number("6214180300001315198")
        # 6.点击下一步
        mpp.click_next_step()
        # 7.输入持卡人姓名，身份证号，手机号
        mpp.input_name("测试")
        mpp.input_ID_card("441426199008111234")
        mpp.input_phone_number("14775970980")
        # 8.点击取消勾选
        mpp.click_checklist()
        # 9.验证下一步是否可以点击
        self.assertFalse(mpp.next_step_btn_is_enabled())

    @tags('ALL', 'CMCC', 'Call', 'YX', 'YX_IOS')
    def test_me_zhangshuli_155(self):
        """银行预留信息页面查看快捷支付协议"""
        me = MePage()
        # 1.点击和包支付
        me.click_payment_by_package()
        time.sleep(3)
        # 2.若在授权页面，点击确认授权
        mpp = MePayPage()
        if mpp.is_on_payment_authorization_page():
            mpp.click_sure_authorization()
        time.sleep(2)
        # 3.点击银行卡
        mpp.click_bank_card()
        # 4.点击绑定新银行卡
        time.sleep(5)
        mpp.click_binding_new_bank_cards()
        # 5.输入银行卡号
        mpp.input_bank_card_number("6214180300001315198")
        # 6.点击下一步
        mpp.click_next_step()
        # 7.输入持卡人姓名，身份证号，手机号
        mpp.input_name("测试")
        mpp.input_ID_card("441426199008111234")
        mpp.input_phone_number("14775970980")
        # 8.点击快捷支付协议
        mpp.click_fast_payment_protocol()
        time.sleep(2)
        # 9.验证是否存在协议内容
        self.assertTrue(mpp.is_exist_agreement_common())
        # 10.点击确定
        mpp.click_sure()
        # 11.验证是否在银行预留信息页面
        time.sleep(1)
        self.assertTrue(mpp.is_on_bank_reservation_page())

