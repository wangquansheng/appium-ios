import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.manager_console.EnterpriseInterests import EnterpriseInterestsPage
from pages.workbench.manager_console.ManagerGuide import ManagerGuidePage
from preconditions.BasePreconditions import WorkbenchPreconditions


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

    @staticmethod
    def enter_workbench_page():
        """进入工作台首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def enter_manager_guide_page():
        """进入管理员指引首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_manager_guide()
        mgp = ManagerGuidePage()
        mgp.wait_for_page_load()

    @staticmethod
    def enter_enterprise_interests_page():
        """进入企业权益首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_rights()
        eip = EnterpriseInterestsPage()
        eip.wait_for_page_load()


class ManagerGuideAllTest(TestCase):
    """管理员指引、权益"""

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在工作台首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_workbench_page()
            return
        wbp = WorkbenchPage()
        if not wbp.is_on_workbench_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_workbench_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0001(self):
        """能够正常打开管理员指引页面，可以正常返回"""

        # 1.用户能正常打管理员指引页面；内容展示为文字+图片一起引导教程
        Preconditions.enter_manager_guide_page()
        mgp = ManagerGuidePage()
        # 进入各个指引页面
        mgp.click_guide_by_name("添加/邀请成员 壮大团队，提高协同办公效率")
        # 2.所有指引页面图文都能正常显示，无异常
        mgp.wait_for_guide_page_load("添加/邀请成员")
        mgp.click_back_button()
        mgp.click_guide_by_name("快速建群 根据组织架构快速建群，方便快捷")
        mgp.wait_for_guide_page_load("快速建群")
        mgp.click_back_button()
        mgp.click_guide_by_name("应用配置 灵活配置应用，打造专属工作台")
        mgp.wait_for_guide_page_load("应用配置")
        mgp.click_back_button()
        mgp.click_guide_by_name("企业认证 官方认证更权威，免费获取更多权益")
        mgp.wait_for_guide_page_load("企业认证")
        mgp.click_back_button()
        mgp.click_guide_by_name("后台登录指引 更多管理功能，登录和飞信企业管理后台")
        mgp.wait_for_guide_page_load("后台登录指引")
        mgp.click_back_button()
        # 点击“帮助中心”，点击各个帮助页面
        mgp.click_guide_by_name("帮助中心")
        # 3.可以正常跳转到帮助中心页面，每个帮助页面都可以正常打开
        mgp.wait_for_guide_page_load("创建团队")
        mgp.click_guide_by_name("员工手册")
        mgp.wait_for_guide_page_load("常见问题")
        mgp.click_guide_by_name("应用大全")
        mgp.wait_for_guide_page_load("和飞信特色通讯套件")
        mgp.click_guide_by_name("开发者文档")
        mgp.wait_for_guide_page_load("开发者接入")
        mgp.click_back_button()
        # 等待管理员指引首页加载
        mgp.wait_for_page_load()
        mgp.click_back_button()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0002(self):
        """点击返回键返回上一级页面"""

        # 进入管理员指引首页
        Preconditions.enter_manager_guide_page()
        mgp = ManagerGuidePage()
        # 进入各个指引页面
        mgp.click_guide_by_name("添加/邀请成员 壮大团队，提高协同办公效率")
        mgp.wait_for_guide_page_load("添加/邀请成员")
        # 点击顶部【<】
        mgp.click_back_button()
        # 1.返回到上一级页面
        mgp.wait_for_page_load()
        mgp.click_guide_by_name("快速建群 根据组织架构快速建群，方便快捷")
        mgp.wait_for_guide_page_load("快速建群")
        mgp.click_back_button()
        mgp.wait_for_page_load()
        mgp.click_guide_by_name("应用配置 灵活配置应用，打造专属工作台")
        mgp.wait_for_guide_page_load("应用配置")
        mgp.click_back_button()
        mgp.wait_for_page_load()
        mgp.click_guide_by_name("企业认证 官方认证更权威，免费获取更多权益")
        mgp.wait_for_guide_page_load("企业认证")
        mgp.click_back_button()
        mgp.wait_for_page_load()
        mgp.click_guide_by_name("后台登录指引 更多管理功能，登录和飞信企业管理后台")
        mgp.wait_for_guide_page_load("后台登录指引")
        mgp.click_back_button()
        # 等待管理员指引首页加载
        mgp.wait_for_page_load()
        mgp.click_back_button()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0003(self):
        """点击关闭按钮返回到工作台页面"""

        # 进入管理员指引首页
        Preconditions.enter_manager_guide_page()
        mgp = ManagerGuidePage()
        wbp = WorkbenchPage()
        # 进入各个指引页面
        mgp.click_guide_by_name("添加/邀请成员 壮大团队，提高协同办公效率")
        mgp.wait_for_guide_page_load("添加/邀请成员")
        # 点击顶部【X】
        mgp.click_close()
        # 1.返回到工作台页面
        wbp.wait_for_page_load()
        wbp.click_manager_guide()
        mgp.wait_for_page_load()
        mgp.click_guide_by_name("快速建群 根据组织架构快速建群，方便快捷")
        mgp.wait_for_guide_page_load("快速建群")
        mgp.click_close()
        wbp.wait_for_page_load()
        wbp.click_manager_guide()
        mgp.wait_for_page_load()
        mgp.click_guide_by_name("应用配置 灵活配置应用，打造专属工作台")
        mgp.wait_for_guide_page_load("应用配置")
        mgp.click_close()
        wbp.wait_for_page_load()
        wbp.click_manager_guide()
        mgp.wait_for_page_load()
        mgp.click_guide_by_name("企业认证 官方认证更权威，免费获取更多权益")
        mgp.wait_for_guide_page_load("企业认证")
        mgp.click_close()
        wbp.wait_for_page_load()
        wbp.click_manager_guide()
        mgp.wait_for_page_load()
        mgp.click_guide_by_name("后台登录指引 更多管理功能，登录和飞信企业管理后台")
        mgp.wait_for_guide_page_load("后台登录指引")
        mgp.click_close()
        # 等待工作台首页加载
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0005(self):
        """点击权益页面可正常打开"""

        # 进入企业权益首页
        Preconditions.enter_enterprise_interests_page()
        eip = EnterpriseInterestsPage()
        # 1.页面可以正常打开 页面展示：图标、企业名称、认证、人数、超级会议剩余时长、群发信使剩余条数、语音通知剩余次数、增值服务
        self.assertEquals(eip.is_exist_element_by_name("图标"), True)
        self.assertEquals(eip.is_exist_element_by_name("企业名称"), True)
        self.assertEquals(eip.is_exist_element_by_name("认证"), True)
        self.assertEquals(eip.is_exist_element_by_name("人数"), True)
        self.assertEquals(eip.is_exist_element_by_name("超级会议剩余时长"), True)
        self.assertEquals(eip.is_exist_element_by_name("群发信使剩余条数"), True)
        self.assertEquals(eip.is_exist_element_by_name("语音通知剩余次数"), True)
        self.assertEquals(eip.is_exist_element_by_name("增值服务"), True)
        eip.click_back_button()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0007(self):
        """和飞信套餐购买"""

        # 进入企业权益首页
        Preconditions.enter_enterprise_interests_page()
        eip = EnterpriseInterestsPage()
        # 点击“增值服务”
        eip.click_service()
        eip.wait_for_service_page_load()
        # 点击“和飞信套餐”（确保进入和飞信套餐购买tab页）
        eip.click_name_attribute_by_name("和飞信套餐")
        # 选择第一个套餐：5元套餐包
        eip.click_accessibility_id_attribute_by_name("5元套餐包")
        time.sleep(2)
        # 勾选“同意为该企业购买，已阅读并确认《增值服务协议》”
        eip.click_agree_button()
        # 点击“确认”
        eip.click_sure()
        # 点击弹窗“确认”
        eip.click_sure_popup()
        # 1.打开支付收银台界面
        eip.wait_for_pay_page_load()
        eip.click_close()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0008(self):
        """和飞信套餐购买- 不勾选同意"""

        # 进入企业权益首页
        Preconditions.enter_enterprise_interests_page()
        eip = EnterpriseInterestsPage()
        # 点击“增值服务”
        eip.click_service()
        eip.wait_for_service_page_load()
        # 点击“和飞信套餐”（确保进入和飞信套餐购买tab页）
        eip.click_name_attribute_by_name("和飞信套餐")
        # 选择第一个套餐：5元套餐包
        eip.click_accessibility_id_attribute_by_name("5元套餐包")
        # 点击“确认”
        eip.click_sure()
        # 1.弹出提示：请先阅读协议内容
        self.assertEquals(eip.is_exists_accessibility_id_attribute_by_name("请先阅读协议内容"), True)
        eip.click_close()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0009(self):
        """和飞信套餐购买"""

        # 进入企业权益首页
        Preconditions.enter_enterprise_interests_page()
        eip = EnterpriseInterestsPage()
        # 点击“增值服务”
        eip.click_service()
        eip.wait_for_service_page_load()
        # 点击“超级会议套餐”（确保进入超级会议套餐购买tab页）
        eip.click_name_attribute_by_name("超级会议套餐")
        # 选择第一个套餐：1200超级会议
        eip.click_accessibility_id_attribute_by_name("1200分钟超级会议")
        time.sleep(2)
        # 勾选“同意为该企业购买，已阅读并确认《增值服务协议》”
        eip.click_agree_button()
        # 点击“确认”
        eip.click_sure()
        # 点击弹窗的“确认”
        eip.click_sure_popup()
        # 1.打开支付收银台界面
        eip.wait_for_pay_page_load()
        eip.click_close()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0010(self):
        """查看增值服务协议"""

        # 进入企业权益首页
        Preconditions.enter_enterprise_interests_page()
        eip = EnterpriseInterestsPage()
        # 点击“增值服务”
        eip.click_service()
        eip.wait_for_service_page_load()
        # 点击“增值服务协议”
        eip.click_service_agreement()
        # 1.打开协议内容
        self.assertEquals(eip.page_should_contain_text2("欢迎您使用中国移动和飞信增值服务"), True)
        eip.click_close()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0011(self):
        """历史记录查看"""

        # 进入企业权益首页
        Preconditions.enter_enterprise_interests_page()
        eip = EnterpriseInterestsPage()
        # 点击“增值服务”
        eip.click_service()
        eip.wait_for_service_page_load()
        # 点击“购买记录”
        eip.click_purchase_record()
        # 1.打开购买记录列表
        eip.wait_for_purchase_record_page_load()
        eip.click_close()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

