import unittest

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.workbench.corporate_news.CorporateNews import CorporateNewsPage
import time

from pages.workbench.corporate_news.CorporateNewsDetails import CorporateNewsDetailsPage
from pages.workbench.corporate_news.CorporateNewsImageText import CorporateNewsImageTextPage
from pages.workbench.corporate_news.CorporateNewsLink import CorporateNewsLinkPage
from pages.workbench.corporate_news.CorporateNewsNoNews import CorporateNewsNoNewsPage
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
    def enter_corporate_news_page():
        """进入企业新闻首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_add_corporate_news()

    @staticmethod
    def create_unpublished_image_news(news):
        """创建未发新闻(图文新闻)"""

        cnp = CorporateNewsPage()
        cnp.wait_for_page_load()
        for title, content in news:
            # 点击发布新闻
            cnp.click_release_news()
            cnitp = CorporateNewsImageTextPage()
            cnitp.wait_for_page_load()
            # 输入图文新闻标题
            cnitp.input_news_title(title)
            # 输入图文新闻内容
            cnitp.input_news_content(content)
            # 收起键盘
            cnitp.click_name_attribute_by_name("完成")
            # 点击保存
            cnitp.click_save()
            # 点击确定
            cnitp.click_sure()
            cnp.wait_for_page_load()
            time.sleep(2)

    @staticmethod
    def release_corporate_image_news(titles):
        """发布企业新闻(图文新闻)"""

        cnp = CorporateNewsPage()
        cnp.wait_for_page_load()
        for title in titles:
            # 点击发布新闻
            cnp.click_release_news()
            cnitp = CorporateNewsImageTextPage()
            cnitp.wait_for_page_load()
            # 输入图文新闻标题
            cnitp.input_news_title(title)
            # 输入图文新闻内容
            cnitp.input_news_content("123")
            # 收起键盘
            cnitp.click_name_attribute_by_name("完成")
            # 点击发布
            cnitp.click_release()
            # 点击确定
            cnitp.click_sure()
            cnp.wait_for_page_load()
            time.sleep(2)


class CorporateNewsAllTest(TestCase):

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在企业新闻应用首页
        """

        Preconditions.select_mobile('IOS-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_corporate_news_page()
            return
        cnp = CorporateNewsPage()
        if not cnp.is_on_corporate_news_page():
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_corporate_news_page()

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0001(self):
        """检查企业新闻入口是否正确进入企业新闻首页"""

        cnp = CorporateNewsPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.正常进入企业新闻应用首页
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0002(self):
        """检查点击返回按钮控件【<】"""

        cnp = CorporateNewsPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.正常进入企业新闻应用首页
        cnp.wait_for_page_load()
        wbp = WorkbenchPage()
        if cnp.is_exist_close_button():
            cnp.click_close()
            wbp.wait_for_page_load()
            wbp.click_company_news()
            cnp.wait_for_page_load()
        # 点击【<】
        cnp.click_back_button()
        # 3.返回上一级页面
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0003(self):
        """检查点击关闭按钮控件【X】"""

        cnp = CorporateNewsPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.正常进入企业新闻应用首页
        cnp.wait_for_page_load()
        # 确保有控件【X】
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        cnnp.wait_for_page_load()
        # 点击【X】
        cnnp.click_close()
        # 3.返回工作台首页
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0004(self):
        """管理员进入企业新闻初始页，检查页面元素"""

        cnp = CorporateNewsPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【企业新闻】页面
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()
        # 3.企业新闻页面元素有：提示语“向团队所有成员发布第一份新闻，及时发布重要信息”、新建新闻入口“发布新闻”、未发新闻
        self.assertEquals(cnp.page_should_contain_text2("向团队所有成员发出第一条新闻"), True)
        self.assertEquals(cnp.is_exist_release_news_button(), True)
        self.assertEquals(cnp.is_exist_no_news_button(), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0005(self):
        """管理员进入企业新闻页，新闻列表按发布时间倒序排序"""

        cnp = CorporateNewsPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【企业新闻】页面
        cnp.wait_for_page_load()
        # 清空新闻列表，确保不影响验证
        cnp.clear_corporate_news()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00051", "测试新闻00052", "测试新闻00053", "测试新闻00054"]
        Preconditions.release_corporate_image_news(titles)
        # 3.企业新闻列表按发布时间倒序排序(间接验证)
        self.assertEquals(cnp.get_corporate_news_titles(), titles)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0006(self):
        """管理员下线自己发布的企业新闻，下线成功"""

        cnp = CorporateNewsPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【企业新闻】页面
        cnp.wait_for_page_load()
        # 确保存在已发布的企业新闻
        if not cnp.is_exist_corporate_news():
            titles = ["测试新闻0006"]
            Preconditions.release_corporate_image_news(titles)
        # 3.选中一条管理员自己发布的企业新闻
        cnp.click_corporate_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 点击【下线】按钮
        cndp.click_offline()
        # 4.弹出确定和取消对话框
        self.assertEquals(cndp.page_should_contain_text2("确定"), True)
        # 点击【确定】按钮
        cndp.click_sure()
        # 5.确认下线，下线成功
        self.assertEquals(cndp.is_exist_offline_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @unittest.skip("暂时难以实现,跳过")
    def test_QYXW_0008(self):
        """管理员按英文搜索企业新闻"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        cnp.clear_corporate_news()
        # 确保存在多条已发布的企业新闻
        titles = ["testnews", "测试新闻0008", "news"]
        Preconditions.release_corporate_image_news(titles)
        cnp.click_search_icon()
        cnp.input_search_content("testnews")
        cnp.click_search_button()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0017(self):
        """管理员发布新闻成功"""

        cnp = CorporateNewsPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【企业新闻】页面
        cnp.wait_for_page_load()
        # 点击【发布新闻】按钮
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        # 3.成功进入【发布】页面
        cnitp.wait_for_page_load()
        time.sleep(10)
        # 4.正确选择发布方式
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 5.发布内容填写正确
        cnlp.input_news_title("测试新闻0017")
        cnlp.input_link_url("https://10086.com")
        # 收起键盘
        cnlp.click_name_attribute_by_name("完成")
        # 点击【发布】按钮
        cnlp.click_release()
        # 6.弹出确定和取消对话框
        self.assertEquals(cnlp.page_should_contain_text2("确定"), True)
        # 点击【确定】按钮
        cnlp.click_sure()
        # 7.确定发布新闻成功
        self.assertEquals(cnlp.is_exist_release_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0018(self):
        """管理员取消发布新闻成功"""

        cnp = CorporateNewsPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【企业新闻】页面
        cnp.wait_for_page_load()
        # 点击【发布新闻】按钮
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        # 3.成功进入【发布】页面
        cnitp.wait_for_page_load()
        time.sleep(10)
        # 4.正确选择发布方式
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 5.发布内容填写正确
        cnlp.input_news_title("测试新闻0018")
        cnlp.input_link_url("https://10086.com")
        # 收起键盘
        cnlp.click_name_attribute_by_name("完成")
        # 点击【发布】按钮
        cnlp.click_release()
        # 6.弹出确定和取消对话框
        self.assertEquals(cnlp.page_should_contain_text2("取消"), True)
        # 点击【取消】按钮
        cnlp.click_cancel()
        # 7.取消发布新闻，不发布新闻
        cnlp.wait_for_page_load()
        cnlp.click_back_button()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0019(self):
        """管理员删除未发布新闻，删除成功"""

        cnp = CorporateNewsPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【企业新闻】页面
        cnp.wait_for_page_load()
        # 点击【未发新闻】按钮
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        # 3.成功进入【未发布】页面
        cnnp.wait_for_page_load()
        cnnp.clear_no_news()
        # 确保未发新闻列表存在数据
        news = [("测试新闻0019", "测试内容0019")]
        cnnp.click_close()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_company_news()
        Preconditions.create_unpublished_image_news(news)
        cnp.click_no_news()
        cnnp.wait_for_page_load()
        # 选中一条未发布新闻
        title = cnnp.click_no_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 4.进入未发布新闻详情页
        cndp.wait_for_page_load()
        # 点击【删除】按钮
        cndp.click_delete()
        # 5.弹出确定和取消对话框
        self.assertEquals(cndp.page_should_contain_text2("确定"), True)
        # 点击【确定】按钮
        cndp.click_sure()
        # 6.确认删除未发布新闻，删除成功
        self.assertEquals(cndp.is_exist_delete_successfully(), True)
        cnnp.wait_for_page_load()
        self.assertEquals(cnnp.is_exist_no_news_by_name(title), False)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0020(self):
        """管理员发布未发布新闻，发布成功"""

        cnp = CorporateNewsPage()
        # 1.管理员成功登录移动端和飞信工作台
        # 2.进入【企业新闻】页面
        cnp.wait_for_page_load()
        # 点击【未发新闻】按钮
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        # 3.成功进入【未发布】页面
        cnnp.wait_for_page_load()
        # 确保存在未发布的企业新闻
        if not cnnp.is_exist_no_news():
            cnnp.click_back_button()
            cnp.wait_for_page_load()
            news = [("测试新闻0020", "测试内容0020")]
            Preconditions.create_unpublished_image_news(news)
            cnp.click_no_news()
            cnnp.wait_for_page_load()
        # 选中一条未发布新闻
        cnnp.click_no_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 4.进入未发布新闻详情页
        cndp.wait_for_page_load()
        # 点击【发布】按钮
        cndp.click_release()
        # 5.弹出确定和取消对话框
        self.assertEquals(cndp.page_should_contain_text2("确定"), True)
        # 点击【确定】按钮
        cndp.click_sure()
        # 6.确认发布未发布新闻，发布成功
        self.assertEquals(cndp.is_exist_release_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0030(self):
        """检验统计新闻浏览人数功能是否正确"""

        cnp = CorporateNewsPage()
        # 1.用户成功登录移动端和飞信工作台
        # 2.进入【企业新闻】页面
        cnp.wait_for_page_load()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00301", "测试新闻00302"]
        Preconditions.release_corporate_image_news(titles)
        number = 0
        # 访问前的浏览量
        amount = cnp.get_corporate_news_page_view_by_number(number)
        # 点击一条新闻
        cnp.click_corporate_news_by_number(number)
        cndp = CorporateNewsDetailsPage()
        # 3.进入新闻详情页
        cndp.wait_for_page_load()
        # 查看之后返回到列表
        cndp.click_back_button()
        cnp.wait_for_page_load()
        # 访问后的浏览量
        news_amount = cnp.get_corporate_news_page_view_by_number(number)
        # 4.每次用户查看新闻详情再返回到列表之后，浏览数量+1
        self.assertEquals(amount + 1, news_amount)
        # 查看浏览人数
        cnp.click_corporate_news_by_number(number)
        cndp.wait_for_page_load()
        news_details_amount = cndp.get_corporate_news_detail_view()
        # 5.再点进去里面的浏览数量外面的数量保持一致
        self.assertEquals(news_amount, news_details_amount)
        cndp.click_back_button()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0034(self):
        """保存新闻"""

        cnp = CorporateNewsPage()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        cnitp.wait_for_page_load()
        time.sleep(10)
        # 点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 输入新闻标题、链接新闻
        cnlp.input_news_title("测试新闻0034")
        cnlp.input_link_url("https://10086.com")
        # 收起键盘
        cnlp.click_name_attribute_by_name("完成")
        # 其它项保存发布
        cnlp.click_save()
        # 点击确定
        cnlp.click_sure()
        # 1.保存成功，页面跳转到企业新闻首页
        self.assertEquals(cnlp.is_exist_save_successfully(), True)
        cnp.wait_for_page_load()
