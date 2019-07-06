import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.workbench.announcement_message.AnnouncementInformation import AnnouncementInformationPage
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
    def enter_announcement_information_page():
        """进入公告信息首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_announcement_information()

    @staticmethod
    def release_announcement_information_image(titles):
        """发布公告信息(图文发布)"""

        aip = AnnouncementInformationPage()
        aip.wait_for_page_load()
        for title in titles:
            # 点击发布公告
            aip.click_release_announcement()
            aip.wait_for_image_release_page_load()
            # 输入图文公告标题
            aip.input_announcement_image_title(title)
            # 输入图文公告内容
            aip.input_announcement_image_content("123")
            # 收起键盘
            aip.click_name_attribute_by_name("完成")
            # 点击发布
            aip.click_release()
            # 点击确定
            aip.click_sure()
            aip.wait_for_page_load()
            time.sleep(2)

    @staticmethod
    def create_unpublished_announcement_information_image(titles):
        """创建未发公告信息(图文发布)"""

        aip = AnnouncementInformationPage()
        aip.wait_for_page_load()
        for title in titles:
            # 点击发布公告
            aip.click_release_announcement()
            aip.wait_for_image_release_page_load()
            # 输入图文公告标题
            aip.input_announcement_image_title(title)
            # 输入图文公告内容
            aip.input_announcement_image_content("123")
            # 收起键盘
            aip.click_name_attribute_by_name("完成")
            # 点击保存
            aip.click_save()
            # 点击确定
            aip.click_sure()
            aip.wait_for_page_load()
            time.sleep(2)


class AnnouncementInformationAllTest(TestCase):

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在公告信息应用首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_announcement_information_page()
            return
        aip = AnnouncementInformationPage()
        if not aip.is_on_announcement_information_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_announcement_information_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0001(self):
        """检查公告信息入口是否正确"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.正常进入公告信息应用首页
        aip.wait_for_page_load()
        # 确保企业公告信息首页不存在公告信息
        aip.clear_announcement_information()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0002(self):
        """点击返回按钮控件【<】"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        aip.wait_for_page_load()
        wbp = WorkbenchPage()
        # 点击【 < 】
        aip.click_back_button()
        # 2.返回上一级页面
        wbp.wait_for_page_load()
        wbp.click_notice_info()
        aip.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0003(self):
        """检查点击关闭按钮控件【X】"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        aip.wait_for_page_load()
        # 确保有控件【X】
        aip.click_no_announcement()
        time.sleep(2)
        # 点击【x】
        aip.click_close()
        wbp = WorkbenchPage()
        # 2.返回工作台首页
        wbp.wait_for_page_load()
        wbp.click_notice_info()
        aip.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0004(self):
        """管理员进入发布公告，检查初始化页面"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】初始化页面
        aip.wait_for_page_load()
        # 确保企业公告信息首页不存在公告信息
        aip.clear_announcement_information()
        # 3.【公告信息】初始化页面元素有：提示信息“向团队所有成员发布第一份公告信息，及时发布重要信息”、“发布公告”和“未发布公告”按钮
        self.assertEquals(aip.page_should_contain_text2("向团队所有成员发出第一条公告"), True)
        self.assertEquals(aip.is_exist_release_announcement_button(), True)
        self.assertEquals(aip.is_exist_no_announcement_button(), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0005(self):
        """公告列表按发布时间倒序显示"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.管理员成功进入【公告信息】页面
        aip.wait_for_page_load()
        # 清空公告信息列表，确保不影响验证
        aip.clear_announcement_information()
        # 确保存在多条已发布的公告信息
        titles = ["测试公告00051", "测试公告00052", "测试公告00053", "测试公告00054"]
        Preconditions.release_announcement_information_image(titles)
        # 3.公告列表显示，跟发布时间倒序显示(间接验证)
        self.assertEquals(aip.get_announcement_information_titles(), titles)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0006(self):
        """管理员进入发布公告，公告搜索-按中文搜索"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 清空公告信息列表，确保不影响验证
        aip.clear_announcement_information()
        # 确保存在可供搜索的公告信息
        titles = ["你好", "测试公告0006"]
        Preconditions.release_announcement_information_image(titles)
        aip.click_search_icon()
        # aip.click_search_box()
        # 按中文搜索公告信息
        aip.input_search_message(titles[0])
        aip.click_name_attribute_by_name("搜索")
        # 3.检查结果列表是否展示正确
        self.assertEquals(aip.is_search_message_full_match(titles[0]), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0007(self):
        """管理员进入发布公告，公告搜索-按英文搜索"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 清空公告信息列表，确保不影响验证
        aip.clear_announcement_information()
        # 确保存在可供搜索的公告信息
        titles = ["test", "测试公告0007"]
        Preconditions.release_announcement_information_image(titles)
        aip.click_search_icon()
        # aip.click_search_box()
        # 按英文搜索公告信息
        aip.input_search_message(titles[0])
        aip.click_name_attribute_by_name("搜索")
        # 3.检查结果列表是否展示正确
        self.assertEquals(aip.is_search_message_full_match(titles[0]), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0008(self):
        """管理员进入发布公告，公告搜索-按特殊字符搜索"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 清空公告信息列表，确保不影响验证
        aip.clear_announcement_information()
        # 确保存在可供搜索的公告信息
        titles = ["$@%", "测试公告0008"]
        Preconditions.release_announcement_information_image(titles)
        aip.click_search_icon()
        # aip.click_search_box()
        # 按特殊字符搜索公告信息
        aip.input_search_message(titles[0])
        aip.click_name_attribute_by_name("搜索")
        # 3.检查结果列表是否展示正确
        self.assertEquals(aip.is_search_message_full_match(titles[0]), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0009(self):
        """管理员进入发布公告，公告搜索-空格搜索"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 清空公告信息列表，确保不影响验证
        aip.clear_announcement_information()
        # 确保存在可供搜索的公告信息
        titles = ["我 马上", "测试公告0009"]
        Preconditions.release_announcement_information_image(titles)
        aip.click_search_icon()
        # aip.click_search_box()
        # 带空格搜索公告信息
        aip.input_search_message(" 马上")
        aip.click_name_attribute_by_name("搜索")
        # 3.检查结果列表是否展示正确
        self.assertEquals(aip.is_search_message_full_match(titles[0]), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0010(self):
        """管理员进入发布公告，公告搜索-XSS安全"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 清空公告信息列表，确保不影响验证
        aip.clear_announcement_information()
        # 确保存在可供搜索的公告信息
        titles = ["测试公告00101", "测试公告00102"]
        Preconditions.release_announcement_information_image(titles)
        aip.click_search_icon()
        # aip.click_search_box()
        # 在搜索框输入<img src=1 onmouseover=alert(1) />
        aip.input_search_message("<img src=1 onmouseover=alert(1) />")
        aip.click_name_attribute_by_name("搜索")
        # 3.检查结果列表是否展示正确
        self.assertEquals(aip.page_should_contain_text2("未查询到公告数据"), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0011(self):
        """管理员进入发布公告，公告搜索-按数字搜索"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 清空公告信息列表，确保不影响验证
        aip.clear_announcement_information()
        # 确保存在可供搜索的公告信息
        titles = ["654321", "测试公告0011"]
        Preconditions.release_announcement_information_image(titles)
        aip.click_search_icon()
        # aip.click_search_box()
        # 按数字搜索公告信息
        aip.input_search_message(titles[0])
        aip.click_name_attribute_by_name("搜索")
        # 3.检查结果列表是否展示正确
        self.assertEquals(aip.is_search_message_full_match(titles[0]), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0012(self):
        """管理员检查搜索页面元素"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 确保存在可供搜索的公告信息
        titles = ["测试公告00121", "测试公告00122"]
        Preconditions.release_announcement_information_image(titles)
        aip.click_search_icon()
        # aip.click_search_box()
        # 按数字搜索公告信息
        aip.input_search_message("测试公告")
        aip.click_name_attribute_by_name("搜索")
        # 3.搜索页面元素有：公告列表（公告标题、创建公告人、创建时间、浏览人数）
        self.assertEquals(aip.is_exists_announcement_title(), True)
        self.assertEquals(aip.is_exists_create_announcer(), True)
        self.assertEquals(aip.is_exists_create_time(), True)
        self.assertEquals(aip.is_exists_visitors(), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0013(self):
        """发布公告页面元素检查"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 点击【发布公告】
        aip.click_release_announcement()
        # 3.进入【发布公告】页面，页面元素有：图文发布、链接发布、消息推送、保存、发布
        aip.wait_for_image_release_page_load()
        self.assertEquals(aip.page_should_contain_text2("图文发布"), True)
        self.assertEquals(aip.page_should_contain_text2("链接发布"), True)
        self.assertEquals(aip.page_should_contain_text2("消息推送"), True)
        self.assertEquals(aip.page_should_contain_text2("保存"), True)
        self.assertEquals(aip.page_should_contain_text2("发布"), True)
        # 4.默认选择图文方式
        self.assertEquals(aip.page_should_contain_text2("公告内容"), True)
        # 5.消息推送默认不推送(间接验证)
        aip.click_back_button()
        aip.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0018(self):
        """管理员发布公告成功"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 点击【发布公告】
        aip.click_release_announcement()
        # 3.进入【发布公告】页面
        aip.wait_for_image_release_page_load()
        # 选择发布方式
        aip.click_link_publishing()
        # 4.成功选择发布方式
        aip.wait_for_link_release_page_load()
        # 5.页面消息填写正确
        aip.input_announcement_link_title("测试公告0018")
        aip.input_announcement_link_url("https://10086.com")
        # 收起键盘
        aip.click_name_attribute_by_name("完成")
        # 点击【发布】按钮
        aip.click_release()
        # 6.页面弹出确定和取消对话弹框
        self.assertEquals(aip.page_should_contain_text2("确定"), True)
        # 点击【确定】按钮
        aip.click_sure()
        # 7.确认发布，发布成功
        self.assertEquals(aip.page_should_contain_text2("发布成功"), True)
        aip.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0019(self):
        """管理员发布公告，取消发布，不发布公告"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 点击【发布公告】
        aip.click_release_announcement()
        # 3.进入【发布公告】页面
        aip.wait_for_image_release_page_load()
        # 选择发布方式
        aip.click_link_publishing()
        # 4.成功选择发布方式
        aip.wait_for_link_release_page_load()
        # 5.页面消息填写正确
        aip.input_announcement_link_title("测试公告0019")
        aip.input_announcement_link_url("https://10086.com")
        # 收起键盘
        aip.click_name_attribute_by_name("完成")
        # 点击【发布】按钮
        aip.click_release()
        # 6.页面弹出确定和取消对话弹框
        self.assertEquals(aip.page_should_contain_text2("取消"), True)
        # 点击【取消】按钮
        aip.click_cancel()
        # 7.取消发布，不发布公告
        aip.wait_for_link_release_page_load()
        aip.click_back_button()
        aip.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0020(self):
        """管理员删除未发布公告，删除成功"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 点击【未发公告】
        aip.click_no_announcement()
        # 3.进入【未发公告】页面
        self.assertEquals(aip.page_should_contain_text2("未发公告"), True)
        # 确保有未发布的公告信息
        if not aip.is_exist_announcement_information():
            aip.click_back_button()
            aip.wait_for_page_load()
            titles = ["测试公告0020"]
            Preconditions.create_unpublished_announcement_information_image(titles)
            aip.click_no_announcement()
            time.sleep(2)
        # 选中一条未发布公告
        aip.click_announcement_by_number(0)
        # 4.进入未发布公告详情页
        aip.wait_for_detail_page_load()
        # 点击【删除】按钮
        aip.click_delete()
        # 5.页面弹出确定和取消对话弹框
        self.assertEquals(aip.page_should_contain_text2("确定"), True)
        # 点击【确定】按钮
        aip.click_sure()
        # 6.成功删除未发布公告
        self.assertEquals(aip.page_should_contain_text2("删除成功"), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0021(self):
        """管理员发布未发布公告，发布成功"""

        aip = AnnouncementInformationPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 点击【未发布公告】
        aip.click_no_announcement()
        # 3.进入【未发布公告】页面
        self.assertEquals(aip.page_should_contain_text2("未发公告"), True)
        # 确保有未发布的公告信息
        if not aip.is_exist_announcement_information():
            aip.click_back_button()
            aip.wait_for_page_load()
            titles = ["测试公告0021"]
            Preconditions.create_unpublished_announcement_information_image(titles)
            aip.click_no_announcement()
            time.sleep(2)
        # 选中一条未发布公告
        aip.click_announcement_by_number(0)
        # 4.进入未发布公告详情页
        aip.wait_for_detail_page_load()
        # 点击【发布】按钮
        aip.click_release()
        # 5.页面弹出确定和取消对话弹框
        self.assertEquals(aip.page_should_contain_text2("确定"), True)
        # 点击【确定】按钮
        aip.click_sure()
        # 6.成功发布未发布公告
        self.assertEquals(aip.page_should_contain_text2("发布成功"), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0022(self):
        """验证未发公告页搜索是否正确"""

        aip = AnnouncementInformationPage()
        aip.wait_for_page_load()
        # 点击【未发布公告】
        aip.click_no_announcement()
        time.sleep(2)
        # 确保存在可供搜索的公告信息
        titles = ["测试公告00221", "测试公告00222"]
        Preconditions.create_unpublished_announcement_information_image(titles)
        # 点击右上角放大镜图标
        aip.click_search_icon()
        # 1.展开搜索栏
        self.assertEquals(aip.page_should_contain_text2("取消"), True)
        # aip.click_search_box()
        # 点击搜索栏，输入存在的关键字
        aip.input_search_message(titles[0])
        # 点击搜索
        aip.click_name_attribute_by_name("搜索")
        # 2.列举标题包含关键字的信息
        self.assertEquals(aip.is_search_message_full_match(titles[0]), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0023(self):
        """已发布公告下线"""

        aip = AnnouncementInformationPage()
        aip.wait_for_page_load()
        # 清空公告信息列表，确保不影响验证
        aip.clear_announcement_information()
        # 确保有公告信息下线
        titles = ["测试公告0023"]
        Preconditions.release_announcement_information_image(titles)
        # 点击公告列表的一条公告
        aip.click_announcement_by_number(0)
        aip.wait_for_detail_page_load()
        # 在详情界面，点击底部“下线”
        aip.click_offline()
        # 点击下线提示框弹窗“确定”
        aip.click_sure()
        # 1.下线成功
        self.assertEquals(aip.page_should_contain_text2("下线成功"), True)
        aip.wait_for_page_load()
        # 2.下线公告从已发布列表消失
        self.assertEquals(aip.page_should_contain_text2(titles[0]), False)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_GGXX_0033(self):
        """检验统计浏览人数功能是否正确"""

        aip = AnnouncementInformationPage()
        # 1.用户成功登录移动端和飞信工作台
        # 2.进入【公告信息】页面
        aip.wait_for_page_load()
        # 确保存在多条已发布的公告信息
        titles = ["测试公告00331", "测试公告00332"]
        Preconditions.release_announcement_information_image(titles)
        number = 0
        # 访问前的浏览量
        amount = aip.get_announcement_view_by_number(number)
        aip.click_announcement_by_number(number)
        aip.wait_for_detail_page_load()
        # 查看之后返回到列表
        aip.click_back_button()
        aip.wait_for_page_load()
        # 访问后的浏览量
        new_amount = aip.get_announcement_view_by_number(number)
        # 3.每次用户查看公告详情再返回到列表之后，浏览数量+1
        self.assertEquals(amount + 1, new_amount)
        # 查看浏览人数
        aip.click_announcement_by_number(number)
        aip.wait_for_detail_page_load()
        details_amount = aip.get_announcement_detail_view()
        # 4.再点进去里面的浏览数量外面的数量保持一致
        self.assertEquals(new_amount, details_amount)
        aip.click_back_button()
        aip.wait_for_page_load()
