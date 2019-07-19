import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.workbench.corporate_news.CorporateNews import CorporateNewsPage
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
    def make_already_have_my_picture():
        """确保当前群聊页面已有图片"""
        # 1.点击输入框左上方的相册图标
        gcp = GroupChatPage()
        cpg = ChatPicPage()
        gcp.is_on_this_page()
        if gcp.is_exist_msg_image():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            time.sleep(2)
            gcp.click_picture()
            cpg.wait_for_page_load()
            cpg.select_pic_fk(1)
            cpg.click_send()
            time.sleep(5)

    @staticmethod
    def make_already_have_my_videos():
        """确保当前群聊页面已有视频"""
        # 1.点击输入框左上方的相册图标
        gcp = GroupChatPage()
        cpg = ChatPicPage()
        gcp.wait_for_page_load()
        if gcp.is_exist_msg_videos():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            gcp.click_picture()
            cpg.wait_for_page_load()
            cpg.select_video_fk(1)
            cpg.click_send()
            time.sleep(5)

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
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def make_no_message_send_failed_status():
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()

    @staticmethod
    def if_exists_multiple_enterprises_enter_group_chat(types):
        """选择团队联系人时存在多个团队时返回获取当前团队名，再进入群聊转发图片/视频"""

        shc = SelectHeContactsDetailPage()
        # 测试号码是否存在多个团队
        if not shc.is_exist_corporate_grade():
            mp = MessagePage()
            scg = SelectContactsPage()
            gcp = GroupChatPage()
            shc.click_back()
            scg.wait_for_page_load()
            scg.click_back()
            gcp.wait_for_page_load()
            gcp.click_back()
            mp.wait_for_page_load()
            mp.open_workbench_page()
            wbp = WorkbenchPage()
            wbp.wait_for_page_load()
            time.sleep(2)
            # 获取当前团队名
            workbench_name = wbp.get_workbench_name()
            mp.open_message_page()
            mp.wait_for_page_load()
            group_name = "群聊1"
            Preconditions.get_into_group_chat_page(group_name)
            # 转发图片/视频
            if types == "pic":
                gcp.forward_pic()
            elif types == "video":
                gcp.forward_video()
            scg.wait_for_page_load()
            scg.click_he_contacts()
            shc.wait_for_he_contacts_page_load()
            # 选择当前团队
            shc.click_department_name(workbench_name)

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
            cnitp.click_name_attribute_by_name("完成")
            # 点击发布
            cnitp.click_release()
            # 点击确定
            cnitp.click_sure()
            cnp.wait_for_page_load()
            time.sleep(2)

# lxd_debug2
class MsgGroupChatVideoPicAllTest(TestCase):

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
                current_mobile().hide_keyboard_if_display()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
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

        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        # 确保有企业群
        fail_time3 = 0
        flag3 = False
        while fail_time3 < 5:
            try:
                Preconditions.make_already_in_message_page()
                Preconditions.ensure_have_enterprise_group()
                flag3 = True
            except:
                fail_time3 += 1
            if flag3:
                break

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、确保当前页面在群聊聊天会话页面
        """

        Preconditions.select_mobile('IOS-移动')
        # mp = MessagePage()
        # name = "群聊1"
        # if mp.is_on_this_page():
        #     Preconditions.get_into_group_chat_page(name)
        #     return
        # gcp = GroupChatPage()
        # if not gcp.is_on_this_page():
        #     current_mobile().launch_app()
        #     Preconditions.make_already_in_message_page()
        #     Preconditions.get_into_group_chat_page(name)
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

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0021(self):
        """群聊会话页面，打开拍照，立刻返回会话窗口"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0041(self):
        """群聊会话页面,转发自己发送的图片到当前会话窗口"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        wbp = WorkbenchPage()
        if cnp.is_exist_close_button():
            cnp.click_close()
            wbp.wait_for_page_load()
            wbp.click_company_news()
            cnp.wait_for_page_load()
        # 点击【<】
        cnp.click_back_button()
        # 3.等待工作台页面加载
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0042(self):
        """群聊会话页面，转发自己发送的图片到当前会话窗口时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保有控件【X】
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        cnnp.wait_for_page_load()
        # 点击【X】
        cnnp.click_close()
        # 3.等待工作台页面加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0043(self):
        """群聊会话页面，转发自己发送的图片到当前会话窗口时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()
        # 3.是否存在提示语,“发布新闻”、“未发新闻”按钮
        self.assertEquals(cnp.page_should_contain_text2("向团队所有成员发出第一条新闻"), True)
        self.assertEquals(cnp.is_exist_release_news_button(), True)
        self.assertEquals(cnp.is_exist_no_news_button(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0044(self):
        """群聊会话页面，转发自己发送的图片给手机联系人"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        cnp.clear_corporate_news()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00051", "测试新闻00052", "测试新闻00053", "测试新闻00054"]
        Preconditions.release_corporate_image_news(titles)
        # 3.企业新闻列表是否按发布时间倒序排序
        self.assertEquals(cnp.get_corporate_news_titles(), titles)

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0045(self):
        """群聊会话页面，转发自己发送的图片到手机联系人时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保存在已发布的企业新闻
        if not cnp.is_exist_corporate_news():
            titles = ["测试新闻0006"]
            Preconditions.release_corporate_image_news(titles)
        # 3.选择一条企业新闻
        cnp.click_corporate_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 4.点击下线
        cndp.click_offline()
        # 5.点击确定，是否提示下线成功(部分验证点变动)
        cndp.click_sure()
        # self.assertEquals(cndp.is_exist_offline_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0046(self):
        """群聊会话页面，转发自己发送的图片到手机联系人时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        # 3.等待发布新闻-图文发布页加载
        cnitp.wait_for_page_load()
        # 4.点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 5.输入链接新闻标题、内容
        cnlp.input_news_title("测试新闻0017")
        cnlp.input_link_url("https://10086.com")
        cnlp.click_name_attribute_by_name("完成")
        # 6.点击发布
        cnlp.click_release()
        # 点击确定
        cnlp.click_sure()
        # 7.是否提示发布成功(部分验证点变动)
        # self.assertEquals(cnlp.is_exist_release_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0047(self):
        """群聊会话页面，转发自己发送的图片给团队联系人"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        # 3.等待发布新闻-图文发布页加载
        cnitp.wait_for_page_load()
        # 4.点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 5.输入链接新闻标题、内容
        cnlp.input_news_title("测试新闻0018")
        cnlp.input_link_url("https://10086.com")
        cnlp.click_name_attribute_by_name("完成")
        # 6.点击发布
        cnlp.click_release()
        # 7.取消发布新闻
        cnlp.click_cancel()
        cnlp.click_back_button()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0048(self):
        """群聊会话页面，转发自己发送的图片到团队联系人时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击未发新闻
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        # 3.等待未发新闻页加载
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
        # 点击未发新闻
        title = cnnp.click_no_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 4.等待未发布新闻详情页加载
        cndp.wait_for_page_load()
        # 点击删除
        cndp.click_delete()
        # 5.点击确定
        cndp.click_sure()
        # 6.是否提示删除成功，未发新闻列表不存在该记录信息(部分验证点变动)
        # self.assertEquals(cndp.is_exist_delete_successfully(), True)
        cnnp.wait_for_page_load()
        self.assertEquals(cnnp.is_exist_no_news_by_name(title), False)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0049(self):
        """群聊会话页面，转发自己发送的图片到团队联系人时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击未发新闻
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        # 3.等待未发新闻页加载
        cnnp.wait_for_page_load()
        # 确保存在未发布的企业新闻
        if not cnnp.is_exist_no_news():
            cnnp.click_back_button()
            cnp.wait_for_page_load()
            news = [("测试新闻0020", "测试内容0020")]
            Preconditions.create_unpublished_image_news(news)
            cnp.click_no_news()
            cnnp.wait_for_page_load()
        # 点击一条未发新闻
        cnnp.click_no_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 4.等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 5.点击发布
        cndp.click_release()
        # 6.点击确定，是否提示发布成功(部分验证点变动)
        cndp.click_sure()
        # self.assertEquals(cndp.is_exist_release_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0050(self):
        """群聊会话页面，转发自己发送的图片给陌生人"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00301", "测试新闻00302"]
        Preconditions.release_corporate_image_news(titles)
        number = 0
        # 访问前的浏览量
        amount = cnp.get_corporate_news_page_view_by_number(number)
        # 3.进入新闻详情页
        cnp.click_corporate_news_by_number(number)
        cndp = CorporateNewsDetailsPage()
        cndp.wait_for_page_load()
        cndp.click_back_button()
        cnp.wait_for_page_load()
        # 访问后的浏览量
        news_amount = cnp.get_corporate_news_page_view_by_number(number)
        # 4.验证每次用户查看新闻详情再返回到列表之后，浏览数量是否+1
        self.assertEquals(amount + 1, news_amount)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0051(self):
        """群聊会话页面，转发自己发送的图片到陌生人时失败"""

        cnp = CorporateNewsPage()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        cnitp.wait_for_page_load()
        # 点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 输入链接新闻标题
        cnlp.input_news_title("测试新闻0034")
        # 输入链接新闻网址
        cnlp.input_link_url("https://10086.com")
        cnlp.click_name_attribute_by_name("完成")
        # 点击保存
        cnlp.click_save()
        # 点击确定
        cnlp.click_sure()
        # 1.是否提示保存成功,等待企业新闻首页加载(部分验证点变动)
        # self.assertEquals(cnlp.is_exist_save_successfully(), True)
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0052(self):
        """群聊会话页面，转发自己发送的图片到陌生人时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0053(self):
        """群聊会话页面，转发自己发送的图片到普通群"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        wbp = WorkbenchPage()
        if cnp.is_exist_close_button():
            cnp.click_close()
            wbp.wait_for_page_load()
            wbp.click_company_news()
            cnp.wait_for_page_load()
        # 点击【<】
        cnp.click_back_button()
        # 3.等待工作台页面加载
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0054(self):
        """群聊会话页面，转发自己发送的图片到普通群时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保有控件【X】
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        cnnp.wait_for_page_load()
        # 点击【X】
        cnnp.click_close()
        # 3.等待工作台页面加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0055(self):
        """群聊会话页面，转发自己发送的图片到普通群时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()
        # 3.是否存在提示语,“发布新闻”、“未发新闻”按钮
        self.assertEquals(cnp.page_should_contain_text2("向团队所有成员发出第一条新闻"), True)
        self.assertEquals(cnp.is_exist_release_news_button(), True)
        self.assertEquals(cnp.is_exist_no_news_button(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0056(self):
        """群聊会话页面，转发自己发送的图片到企业群"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        cnp.clear_corporate_news()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00051", "测试新闻00052", "测试新闻00053", "测试新闻00054"]
        Preconditions.release_corporate_image_news(titles)
        # 3.企业新闻列表是否按发布时间倒序排序
        self.assertEquals(cnp.get_corporate_news_titles(), titles)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0057(self):
        """群聊会话页面，转发自己发送的图片到企业群时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保存在已发布的企业新闻
        if not cnp.is_exist_corporate_news():
            titles = ["测试新闻0006"]
            Preconditions.release_corporate_image_news(titles)
        # 3.选择一条企业新闻
        cnp.click_corporate_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 4.点击下线
        cndp.click_offline()
        # 5.点击确定，是否提示下线成功(部分验证点变动)
        cndp.click_sure()
        # self.assertEquals(cndp.is_exist_offline_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0058(self):
        """群聊会话页面，转发自己发送的图片到企业群时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        # 3.等待发布新闻-图文发布页加载
        cnitp.wait_for_page_load()
        # 4.点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 5.输入链接新闻标题、内容
        cnlp.input_news_title("测试新闻0017")
        cnlp.input_link_url("https://10086.com")
        cnlp.click_name_attribute_by_name("完成")
        # 6.点击发布
        cnlp.click_release()
        # 点击确定
        cnlp.click_sure()
        # 7.是否提示发布成功(部分验证点变动)
        # self.assertEquals(cnlp.is_exist_release_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0069(self):
        """群聊会话页面，转发自己发送的视频给手机联系人"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        # 3.等待发布新闻-图文发布页加载
        cnitp.wait_for_page_load()
        # 4.点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 5.输入链接新闻标题、内容
        cnlp.input_news_title("测试新闻0018")
        cnlp.input_link_url("https://10086.com")
        cnlp.click_name_attribute_by_name("完成")
        # 6.点击发布
        cnlp.click_release()
        # 7.取消发布新闻
        cnlp.click_cancel()
        cnlp.click_back_button()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0070(self):
        """群聊会话页面，转发自己发送的视频给手机联系人时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击未发新闻
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        # 3.等待未发新闻页加载
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
        # 点击未发新闻
        title = cnnp.click_no_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 4.等待未发布新闻详情页加载
        cndp.wait_for_page_load()
        # 点击删除
        cndp.click_delete()
        # 5.点击确定
        cndp.click_sure()
        # 6.是否提示删除成功，未发新闻列表不存在该记录信息(部分验证点变动)
        # self.assertEquals(cndp.is_exist_delete_successfully(), True)
        cnnp.wait_for_page_load()
        self.assertEquals(cnnp.is_exist_no_news_by_name(title), False)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0071(self):
        """群聊会话页面，转发自己发送的视频给手机联系人时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击未发新闻
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        # 3.等待未发新闻页加载
        cnnp.wait_for_page_load()
        # 确保存在未发布的企业新闻
        if not cnnp.is_exist_no_news():
            cnnp.click_back_button()
            cnp.wait_for_page_load()
            news = [("测试新闻0020", "测试内容0020")]
            Preconditions.create_unpublished_image_news(news)
            cnp.click_no_news()
            cnnp.wait_for_page_load()
        # 点击一条未发新闻
        cnnp.click_no_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 4.等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 5.点击发布
        cndp.click_release()
        # 6.点击确定，是否提示发布成功(部分验证点变动)
        cndp.click_sure()
        # self.assertEquals(cndp.is_exist_release_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0072(self):
        """群聊会话页面，转发自己发送的视频给团队联系人"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00301", "测试新闻00302"]
        Preconditions.release_corporate_image_news(titles)
        number = 0
        # 访问前的浏览量
        amount = cnp.get_corporate_news_page_view_by_number(number)
        # 3.进入新闻详情页
        cnp.click_corporate_news_by_number(number)
        cndp = CorporateNewsDetailsPage()
        cndp.wait_for_page_load()
        cndp.click_back_button()
        cnp.wait_for_page_load()
        # 访问后的浏览量
        news_amount = cnp.get_corporate_news_page_view_by_number(number)
        # 4.验证每次用户查看新闻详情再返回到列表之后，浏览数量是否+1
        self.assertEquals(amount + 1, news_amount)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0073(self):
        """群聊会话页面，转发自己发送的视频给团队联系人时失败"""

        cnp = CorporateNewsPage()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        cnitp.wait_for_page_load()
        # 点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 输入链接新闻标题
        cnlp.input_news_title("测试新闻0034")
        # 输入链接新闻网址
        cnlp.input_link_url("https://10086.com")
        cnlp.click_name_attribute_by_name("完成")
        # 点击保存
        cnlp.click_save()
        # 点击确定
        cnlp.click_sure()
        # 1.是否提示保存成功,等待企业新闻首页加载(部分验证点变动)
        # self.assertEquals(cnlp.is_exist_save_successfully(), True)
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0074(self):
        """群聊会话页面，转发自己发送的视频给团队联系人时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保有控件【X】
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        cnnp.wait_for_page_load()
        # 点击【X】
        cnnp.click_close()
        # 3.等待工作台页面加载
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD', 'high')
    def test_msg_xiaoliping_D_0075(self):
        """群聊会话页面，转发自己发送的视频给陌生人"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()
        # 3.是否存在提示语,“发布新闻”、“未发新闻”按钮
        self.assertEquals(cnp.page_should_contain_text2("向团队所有成员发出第一条新闻"), True)
        self.assertEquals(cnp.is_exist_release_news_button(), True)
        self.assertEquals(cnp.is_exist_no_news_button(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0076(self):
        """群聊会话页面，转发自己发送的视频给陌生人时失败"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        cnp.clear_corporate_news()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00051", "测试新闻00052", "测试新闻00053", "测试新闻00054"]
        Preconditions.release_corporate_image_news(titles)
        # 3.企业新闻列表是否按发布时间倒序排序
        self.assertEquals(cnp.get_corporate_news_titles(), titles)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_D_0077(self):
        """群聊会话页面，转发自己发送的视频给陌生人时点击取消转发"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保存在已发布的企业新闻
        if not cnp.is_exist_corporate_news():
            titles = ["测试新闻0006"]
            Preconditions.release_corporate_image_news(titles)
        # 3.选择一条企业新闻
        cnp.click_corporate_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 4.点击下线
        cndp.click_offline()
        # 5.点击确定，是否提示下线成功(部分验证点变动)
        cndp.click_sure()
        # self.assertEquals(cndp.is_exist_offline_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()


class MsgGroupChatTest(TestCase):

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

    def default_tearDown(self):

        Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0001(self):
        """群聊会话页面，不勾选相册内图片点击发送按钮"""

        mp = MessagePage()
        mp.wait_for_page_load()
        #在消息页面等待页面加载
        mp.click_add_icon()
        #点击加号
        mp.click_group_chat()
        #点击发起群聊
        sccp = SelectContactsPage()
        #选择联系人页面
        sccp.wait_for_page_load()
        #等待选择联系人页面加载
        sccp.click_select_one_group()
        #点击选择一个群按钮
        sog = SelectOneGroupPage()
        #选择一个群界面
        sog.selecting_one_group_by_name("群聊1")
        #通过名称找到群聊1
        gcp = GroupChatPage()
        #群聊1界面
        gcp.wait_for_page_load()
        #等待页面加载
        gcp.click_picture()
        #点击图片按钮
        cpp = ChatPicPage()
        #选择图片页面
        cpp.wait_for_page_load()
        #等待页面加载
        self.assertEquals(cpp.send_btn_is_enabled(), False)
        #判断发送按钮enabled是否为false

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0002(self):
        '''群聊会话页面，勾选相册内一张图片发送'''
        mp = MessagePage()
        #等待页面加载
        mp.wait_for_page_load()
        #点击加号
        mp.click_add_icon()
        #点击发起群聊按钮
        mp.click_group_chat()
        #选择联系人界面
        scp = SelectContactsPage()
        #等待页面加载
        scp.wait_for_page_load()
        #点击选择一个群按钮
        scp.click_select_one_group()
        #选择一个群界面
        sog = SelectOneGroupPage()
        #等待页面加载
        sog.wait_for_page_load()
        #通过名称找到群聊'啊测测试试'
        sog.selecting_one_group_by_name('啊测测试试')
        #群聊页面
        gcp = GroupChatPage()
        #等待页面加载
        gcp.wait_for_page_load()
        #点击图片按钮
        gcp.click_picture()
        #选择图片界面
        cpp = ChatPicPage()
        #等待页面加载
        cpp.wait_for_page_load()
        #选择第一张照片
        cpp.select_picture()
        #点击发送 按钮中有发送就可以点击
        cpp.click_name_attribute_by_name("发送")
        #等待页面加载
        gcp.wait_for_page_load()
        #点击返回按钮
        gcp.click_back_button()
        #等待页面加载
        mp.wait_for_page_load()
        #验证第一条消息是否为图片
        self.assertEquals(mp.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0003(self):
        """群聊会话页面，预览相册内图片"""
        # 消息界面
        mp = MessagePage()
        # 等待界面加载
        mp.wait_for_page_load()
        # 点击加号
        mp.click_add_icon()
        # 点击发起群聊按钮
        mp.click_group_chat()
        # 选择联系人界面
        scp = SelectContactsPage()
        # 等待页面加载
        scp.wait_for_page_load()
        # 点击选择一个群
        scp.click_select_one_group()
        # 选择一个群界面
        sogp = SelectOneGroupPage()
        # 等待页面加载
        sogp.wait_for_page_load()
        # 通过名称选择'群聊1'群聊
        sogp.selecting_one_group_by_name('群聊1')
        # 群聊界面
        gcp = GroupChatPage()
        # 等待页面加载
        gcp.wait_for_page_load()
        # 点击图片按钮
        gcp.click_picture()
        # 选择图片界面
        cpp = ChatPicPage()
        # 等待界面加载
        cpp.wait_for_page_load()
        # 选择第一张图片
        cpp.select_picture()
        # 点击预览按钮
        cpp.click_preview()
        # 预览界面
        cpg = ChatPicPreviewPage()
        # 等待界面加载
        cpg.wait_for_page_load()

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0004(self):
        '''群聊会话页面，预览相册内图片，不勾选原图发送'''
        #消息界面
        message_page = MessagePage()
        #等待页面加载
        message_page.wait_for_page_load()
        #点击加号
        message_page.click_add_icon()
        #点击发起群聊按钮
        message_page.click_group_chat()
        #选择联系人界面
        select_contacts_page = SelectContactsPage()
        #等待界面加载
        select_contacts_page.wait_for_page_load()
        #选择一个群按钮
        select_contacts_page.click_select_one_group()
        #选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        #通过名称找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        #群聊界面
        group_chat_page = GroupChatPage()
        #等待界面加载
        group_chat_page.wait_for_page_load()
        #点击选择图片按钮
        group_chat_page.click_picture()
        #选择图片界面
        chat_pic_page = ChatPicPage()
        #等待界面加载
        chat_pic_page.wait_for_page_load()
        #选择第一张图片
        chat_pic_page.select_picture()
        #点击预览
        chat_pic_page.click_preview()
        #预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        #等待页面加载
        chat_pic_preview_page.wait_for_page_load()
        #点击发送
        chat_pic_preview_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（图片无法选中间接验证）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0005(self):
        '''群聊会话页面，预览相册数量与发送按钮数量一致'''
        #消息界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        #点击加号
        message_page.click_add_icon()
        #点击发起群聊
        message_page.click_group_chat()
        #选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        #选择一个群
        select_contacts_page.click_select_one_group()
        #选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        #通过名称找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        #群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        #点击选择照片
        group_chat_page.click_picture()
        #选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        #选择多张照片
        chat_pic_page.select_pictures(3)
        #点击预览
        chat_pic_page.click_preview()
        #预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        #获取预览数文本
        text1 = chat_pic_preview_page.get_preview_text()
        #获取发送按钮文本
        text2 = chat_pic_preview_page.get_send_text()
        #判断预览数与发送数是否相等
        self.assertEquals(text1, text2)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0006(self):
        """群聊会话页面，编辑图片发送"""
        #消息界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        #点击加号
        message_page.click_add_icon()
        #点击发起群聊
        message_page.click_group_chat()
        #选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        #点击选择一个群
        select_contacts_page.click_select_one_group()
        #选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        #通过群名找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        #群聊1界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        #点击图片按钮
        group_chat_page.click_picture()
        #选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        #选择一张图片
        chat_pic_page.select_pictures(1)
        #点击预览
        chat_pic_page.click_preview()
        #图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        #点击编辑
        chat_pic_preview_page.click_edit()
        #图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        #点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        #滑动进行涂鸦
        chat_pic_edit_page.do_doodle()
        #点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        #滑动进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        #点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        #文本编辑
        chat_pic_edit_page.input_pic_text()
        #点击完成
        chat_pic_edit_page.click_done()
        #点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0007(self):
        """群聊会话页面，编辑图片不保存发送"""
        #消息界面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        #点击加号
        message_page.click_add_icon()
        #点击发起群聊
        message_page.click_group_chat()
        #选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        #点击选择一个群
        select_contacts_page.click_select_one_group()
        #选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        #按名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        #群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        #点击图片按钮
        group_chat_page.click_picture()
        #选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        #选择一张图片
        chat_pic_page.select_pictures(1)
        #点击预览按钮
        chat_pic_page.click_preview()
        #图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        #点击编辑按钮
        chat_pic_preview_page.click_edit()
        #图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        #点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        #进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        #点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        #进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        #点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        #进行文本编辑
        chat_pic_edit_page.input_pic_text()
        #点击完成
        chat_pic_edit_page.click_done()
        #点击保存
        chat_pic_edit_page.click_save()
        chat_pic_edit_page.wait_for_page_load()
        #点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0008(self):
        """群聊会话页面，编辑图片中途直接发送"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        # 点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        # 进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        # 点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        # 进行文本编辑
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0009(self):
        """群聊会话页面，编辑图片保存"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        # 点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        # 进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        # 点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        # 进行文本编辑
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击保存
        chat_pic_edit_page.click_save()
        # 判断保存之后是否有文字提示已保存至系统相册
        self.assertEquals(chat_pic_edit_page.page_should_contain_text2("已保存至系统相册", 20), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0012(self):
        """群聊会话页面，发送相册内的图片 """
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击选择照片
        group_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        numbers = chat_pic_page.get_pic_numbers()
        # 直接点击图片
        chat_pic_page.click_picture_just()
        chat_pic_edit_page = ChatPicEditPage()
        self.assertEquals(chat_pic_edit_page.page_should_contain_text2('预览(1/' + str(numbers)), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0014(self):
        """群聊会话页面，勾选9张相册内图片发送"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择九张图片
        chat_pic_page.select_pictures(9)
        # 点击发送
        chat_pic_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0015(self):
        """群聊会话页面，勾选超9张相册内图片发送"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择九张图片
        chat_pic_page.select_pictures(9)
        # 判断第十个图片的点击按钮是否不可点击
        self.assertEquals(chat_pic_page.picture_btn_is_enabled(10), False)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0016(self):
        """群聊会话页面，同时发送相册中的图片和视频"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 获取发送按钮文本1
        text1 = chat_pic_page.get_send_text()
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 获取点击视频后发送按钮文本2
        text2 = chat_pic_page.get_send_text()
        # 比较文本1和2是否相同（发送按钮没有变化说明无法同时选取照片和视频）
        self.assertEquals(text1, text2)
        # # 判断点击图片之后是否有文字提示不能同时选择照片和视频（有时会抓不到文本信息 不稳定）
        # self.assertEquals(chat_pic_page.page_should_contain_text2("不能同时选择照片和视频", 20), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0017(self):
        """群聊会话页面，使用拍照功能并发送照片"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        # 点击发送
        chat_photo_page.send_photo()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0110(self):
        """在群聊会话窗，验证点击趣图搜搜入口"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        # 判断当前页面时候有关闭gif按钮
        self.assertEquals(group_chat_page.is_exist_closegif_page(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0111(self):
        """在群聊会话窗，网络正常发送表情搜搜"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        # 点击发送GIF图片
        group_chat_page.click_send_gif()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 判断第一条消息是否为表情
        self.assertEquals(message_page.is_first_message_expression(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0082(self):
        """群聊会话页面，发送相册内的视频"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        self.assertEquals(chat_pic_page.send_btn_is_enabled(), False)
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 判断视频时长文本是否包含'：'
        self.assertEquals(chat_pic_page.get_video_text(), True)
        # 判断发送按钮enabled是否为false
        self.assertEquals(chat_pic_page.send_btn_is_enabled(), True)

    @tags('ALL', 'CMCC')
    def test_msg_weifenglian_qun_0013(self):
        """勾选本地照片内任意相册的图片点击发送按钮"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击文件按钮
        group_chat_page.click_file_button()
        # 选择文件界面
        chat_select_file_page = ChatSelectFilePage()
        chat_select_file_page.wait_for_page_load()
        # 选择本地照片
        chat_select_file_page.click_pic()
        chat_select_file_page.wait_for_local_photo_page_load()
        # 选择相机胶卷
        chat_select_file_page.click_camera()
        chat_select_file_page.wait_for_local_photo_page_load()
        # 点击本地照片的图片
        chat_select_file_page.click_picture()
        # 点击发送
        chat_select_file_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_weifenglian_qun_0027(self):
        """勾选本地视频内任意视频点击发送按钮"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击文件按钮
        group_chat_page.click_file_button()
        # 选择文件界面
        chat_select_file_page = ChatSelectFilePage()
        chat_select_file_page.wait_for_page_load()
        # 点击本地视频
        chat_select_file_page.click_video()
        chat_select_file_page.wait_for_local_video_page_load()
        # 选择视频
        chat_select_file_page.click_local_video()
        # 点击确定
        chat_select_file_page.click_sure()
        # 等待群聊页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 判断第一条消息是否为视频
        self.assertEquals(message_page.is_first_message_video(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0001(self):
        """消息列表——发起群聊——选择已有群--模糊搜索"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        # 点击搜索群组
        select_one_group_page.click_search_box()
        # 输入搜索内容模糊搜索'群'
        select_one_group_page.input_search_keyword('群')
        # 判断当前页面是否存在'群聊1'
        self.assertEquals(select_contacts_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0002(self):
        """消息列表——发起群聊——选择已有群--模糊搜索无搜索结果"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        # 点击搜索群组
        select_one_group_page.click_search_box()
        # 输入搜索内容模糊搜索'没有这个群'
        select_one_group_page.input_search_keyword('没有这个群')
        # 判断当前页面是否存在'无搜索结果'
        self.assertEquals(select_contacts_page.page_should_contain_text2('无搜索结果'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0003(self):
        """群聊列表展示页面——中文精确搜索"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        # 点击搜索群组
        select_one_group_page.click_search_box()
        # 输入搜索内容精确搜索'群聊1'
        select_one_group_page.input_search_keyword('群聊1')
        # 判断搜索群名是否匹配
        self.assertEquals(select_one_group_page.page_should_contain_text2("群聊1"), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0018(self):
        """在群聊天会话页面，发送一条字符长度，大于1的文本消息"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击聊天输入框
        group_chat_page.get_input_box()
        # 判断语音按钮是否存在
        group_chat_page.is_exist_voice_button()
        # 输入十个字符
        group_chat_page.input_text_message('1234567890')
        group_chat_page.wait_for_page_load()
        # 判断发送按钮是否存在
        group_chat_page.is_exist_send_button()

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0101(self):
        """在群聊会话窗口，点击输入框上方的图片ICON，进入到图片展示列表"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures()
        # 点击发送
        chat_pic_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0102(self):
        """在群聊会话窗口，点击输入框上方的相机ICON，进入到相机拍摄页"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        # 点击发送
        chat_photo_page.send_photo()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0106(self):
        """点击输入框上方的+号——展示隐藏的：文件、群短信（群主）、位置、红包"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击更多加号按钮
        group_chat_page.click_add_button()
        group_chat_page.wait_for_page_load()
        # 确认当前页面有无群短信，位置，红包元素以及文件按钮
        self.assertEquals(select_one_group_page.page_should_contain_text2("群短信"), True)
        self.assertEquals(select_one_group_page.page_should_contain_text2("位置"), True)
        self.assertEquals(select_one_group_page.page_should_contain_text2("红包"), True)
        self.assertEquals(group_chat_page.is_exist_file_button(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0124(self):
        """普通群——群主——添加一个成员"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 获取当前页面图片元素数量1
        text1 = group_chat_page.get_picture_nums()
        # 点击设置按钮
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_load()
        # 点击添加成员按钮
        group_chat_page.click_add_member_button()
        group_chat_page.wait_for_page_setting_load()
        # 通过文本点击'大佬1'
        group_chat_page.click_accessibility_id_attribute_by_name('大佬1')
        # 点击确定按钮
        group_chat_page.click_add_member_confirm_button()
        # # 判断当前页面是否存在文本'添加成功'  有概率抓取不到 暂时不使用
        # self.assertEquals(group_chat_page.page_should_contain_text2('添加成功'), True)
        group_chat_page.wait_for_page_load()
        # 获取当前页面图片元素数量2
        text2 = group_chat_page.get_picture_nums()
        # 比较两次图片元素数量
        self.assertEquals(int(text1) < int(text2), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0125(self):
        """普通群——群主——添加2个成员"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 获取当前页面图片元素数量1
        text1 = group_chat_page.get_picture_nums()
        # 点击设置按钮
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 点击添加成员按钮
        group_chat_page.click_add_member_button()
        group_chat_page.wait_for_page_setting_load()
        # 通过文本点击'大佬1'
        group_chat_page.click_accessibility_id_attribute_by_name('大佬1')
        # 通过文本点击'大佬2'
        group_chat_page.click_accessibility_id_attribute_by_name('大佬2')
        # 点击确定按钮
        group_chat_page.click_add_member_confirm_button()
        # # 判断当前页面是否存在文本'添加成功'  有概率抓取不到 暂时不使用
        # self.assertEquals(group_chat_page.page_should_contain_text2('添加成功'), True)
        group_chat_page.wait_for_page_load()
        # 获取当前页面图片元素数量2
        text2 = group_chat_page.get_picture_nums()
        # 比较两次图片元素数量
        self.assertEquals(int(text1) < int(text2), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0135(self):
        """无群成员时——点击移除成员按钮"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置按钮
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 点击删除按钮
        group_chat_page.click_delete_member_button()
        time.sleep(2)
        # 判断当前界面是否有'群聊设置'文本
        group_chat_page.wait_for_page_setting_load()
        self.assertEquals(group_chat_page.page_should_contain_text2('群聊设置'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0242(self):
        """消息草稿-聊天列表显示-输入文本信息"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框
        group_chat_page.get_input_box()
        # 输入文本'测试文本'
        group_chat_page.input_text_message('测试文本')
        # 点击返回
        group_chat_page.click_back()
        # 等待消息界面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否包含[草稿]（间接验证，无法验证标红）
        self.assertEquals(message_page.is_first_message_draft(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0247(self):
        """消息草稿-聊天列表显示-草稿信息发送成功"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框
        group_chat_page.get_input_box()
        # 输入文本'测试文本'
        group_chat_page.input_text_message('这是一条特别长的测试文本足够出现省略号')
        # 点击返回
        group_chat_page.click_back()
        # 等待消息界面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否包含[草稿]（间接验证，无法验证标红）
        self.assertEquals(message_page.is_first_message_draft(), True)
        # 验证第一条消息是否包含'...'(无法抓取到省略号 简介验证窗口显示消息是否和整个文本一致)
        self.assertEquals(message_page.is_first_message_content('[草稿] 这是一条特别长的测试文本足够出现省略号'), True)
        # 点击'群聊1'
        message_page.choose_chat_by_name('群聊1')
        group_chat_page.wait_for_page_load()
        # 点击发送
        group_chat_page.click_send_button()
        # 点击返回
        group_chat_page.click_back()
        # 等待消息界面加载
        message_page.wait_for_page_load()
        # 验证第一条消息是否包含[草稿]
        self.assertEquals(message_page.is_first_message_draft(), False)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0044(self):
        """发送一组数字：12345678900，发送成功后，是否会被识别为号码"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()

        # 输入类似电话号码的数字确认是否点击到该行数字
        group_chat_page.input_text_message('13588888888')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫'), True)
        # 通过名字属性点击'取消'按钮
        group_chat_page.click_name_attribute_by_name("取消")

        # 输入数字'12345678900'
        group_chat_page.input_text_message('12345678900')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫', 2), False)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0045(self):
        """发送一组数字：123456，发送成功后，是否会被识别为号码"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 输入数字'123456'
        group_chat_page.input_text_message('123456')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫', 2), False)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0278(self):
        """通讯录——群聊——搜索——选择一个群"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        # 点击搜索群组
        select_one_group_page.click_search_box()
        # 输入搜索内容模糊搜索'群'
        select_one_group_page.input_search_keyword('群')
        # 判断当前页面是否存在'群聊1'
        self.assertEquals(select_contacts_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0279(self):
        """通讯录-群聊-中文模糊搜索——搜索结果展示"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.wait_for_page_load()
        # 点击搜索群组
        select_one_group_page.click_search_box()
        # 输入搜索内容模糊搜索'没有这个群'
        select_one_group_page.input_search_keyword('没有这个群')
        time.sleep(2)
        # 判断当前页面是否存在'无搜索结果'
        self.assertEquals(select_contacts_page.page_should_contain_text2('无搜索结果'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0605(self):
        """开启免打扰后，在聊天页面在输入框输入内容-返回到消息列表页时，该消息列表窗口直接展示：草稿"""
        # 消息页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择一个群
        select_contacts_page.click_select_one_group()
        # 选择一个群界面
        select_one_group_page = SelectOneGroupPage()
        # 通过名字找到'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 群聊界面
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置按钮
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 点击群消息免打扰开关
        if group_chat_page.get_no_disturbing_btn_text() == "0":
            group_chat_page.click_no_disturbing_button()
        # 返回群聊界面
        group_chat_page.click_back()
        group_chat_page.wait_for_page_load()
        # 输入文本
        group_chat_page.input_text_message('1234567890')
        # 点击返回
        group_chat_page.click_back()
        message_page.wait_for_page_load()
        # 判断第一条消息是否显示为草稿(开启免打扰后在消息页面显示是[草稿]+文本... )
        self.assertEquals(message_page.is_first_message_draft(), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0605():
        """恢复环境，将用例开启的消息免打扰开关关闭"""

        try:
            # 确认当前界面在消息界面然后进入到群聊1
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("群聊1")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 判断消息免打扰按钮状态 如果是开启状态点击将其关闭
            if group_chat_page.get_no_disturbing_btn_text() == "1":
                group_chat_page.click_no_disturbing_button()
            group_chat_page.click_back()
            group_chat_page.wait_for_page_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0413(self):
        """群主在群设置页面——点击群名称——修改群名称"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 获取当前页面图片元素数量1(修改群名称前群聊页面图片数量)
        text1 = group_chat_page.get_picture_nums()
        # 点击设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 点击群名称
        group_chat_page.click_group_name()
        # 修改群名称为'已经将群名称修改'
        group_chat_page.input_group_name_message('已经将群名称修改')
        # 点击完成
        group_chat_page.click_group_name_complete()
        group_chat_page.wait_for_page_setting_load()
        # # 判断当前页面是否存在文本'修改成功'  有概率抓取不到 暂时不使用
        # self.assertEquals(group_chat_page.page_should_contain_text2('修改成功'), True)
        # 点击返回
        group_chat_page.click_back()
        group_chat_page.wait_for_page_load()
        # 获取当前页面图片元素数量2(修改群名称后群聊页面图片数量)
        text2 = group_chat_page.get_picture_nums()
        # 比较两次图片元素数量(修改成功提示为图片，无法捕捉文本，判断修改后的图片数量增加)
        self.assertEquals(int(text1) < int(text2), True)
        # 判断当前页面是否有'已经将群名称修改'文本
        self.assertEquals(group_chat_page.page_should_contain_text2('已经将群名称修改'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0413():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""

        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("已经将群名称修改")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0414(self):
        """群主在设置页面——点击群管理——点击解散群按钮"""
        # 前置条件在消息界面进入'群聊1'界面
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 获取当前界面图片数量1
        text1 = group_chat_page.get_picture_nums()
        # 点击设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 点击群管理
        group_chat_page.click_group_control()
        # 点击解散群
        group_chat_page.click_group_dissolve()
        # 点击确认解散
        group_chat_page.click_group_dissolve_confirm()
        time.sleep(2)
        # 获取当前页面图片数量2
        text2 = group_chat_page.get_picture_nums()
        # 比较两次图片数量(该群已解散为图片无法捕捉文本，用图片增加替代)
        self.assertEquals(int(text1) < int(text2), True)
        # 点击返回
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 判断当前页面是否有文本 '系统消息该群已解散'
        self.assertEquals(message_page.page_should_contain_text2('该群已解散'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0414():
        """恢复环境，将用例解散的'群聊1'重新建立"""

        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            message_page = MessagePage()
            message_page.wait_for_page_load()
            # 点击加号
            message_page.click_add_icon()
            # 点击发起群聊
            message_page.click_group_chat()
            # 选择联系人界面
            select_contacts_page = SelectContactsPage()
            select_contacts_page.wait_for_page_load()
            # 点击选择手机联系人
            select_contacts_page.click_phone_contacts()
            # 通过文本点击添加(大佬1，大佬2)
            select_contacts_page.click_accessibility_id_attribute_by_name('大佬1')
            select_contacts_page.click_accessibility_id_attribute_by_name('大佬2')
            # 点击确定
            select_contacts_page.click_confirm_button()
            # 修改群聊名称
            select_contacts_page.input_group_name_message('群聊1')
            # 点击创建
            select_contacts_page.click_create_button()
            time.sleep(3)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0548(self):
        """ 普通群，分享群聊邀请口令"""
        # 前置条件在消息界面,进入'群聊1'界面
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击邀请微信或QQ好友进群
        group_chat_set_page.click_invite_friend()
        group_chat_set_page.wait_for_page_load(15)
        # 判断当前页面是否有'分享群口令邀请好友进群'文本
        self.assertEquals(group_chat_set_page.page_should_contain_text2('分享群口令邀请好友进群'), True)
        # 点击下次再说
        group_chat_set_page.click_next_time()
        group_chat_set_page.wait_for_page_load()
        # 判断当前页面是否没有'分享群口令邀请好友进群'文本
        self.assertEquals(group_chat_set_page.page_should_contain_text2('分享群口令邀请好友进群'), False)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0551(self):
        """普通群，点击口令弹窗的立即分享按钮，分享群口令-QQ"""
        # 前置条件在消息界面,进入'群聊1'界面
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击邀请微信或QQ好友进群
        group_chat_set_page.click_invite_friend()
        self.assertEquals(group_chat_set_page.page_should_contain_text2('分享群口令邀请好友进群', 15), True)
        # 点击立即分享
        group_chat_set_page.click_sharing()
        # 点击分享到QQ
        group_chat_set_page.click_share_qq()
        # (无法抓去到弹窗文本，暂不使用)判断当前界面是否包含文本'该应用尚未安装，请安装后重试'
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('该应用尚未安装'), True)
        # 间接验证：点击分享到qq之后当前界面没有取消按钮
        self.assertEquals(group_chat_set_page.is_exist_cancel_button(), False)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0555(self):
        """普通群，点击口令弹窗的立即分享按钮，分享群口令-微信"""
        # 前置条件在消息界面,进入'群聊1'界面
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        group_chat_page.wait_for_page_setting_load()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击邀请微信或QQ好友进群
        group_chat_set_page.click_invite_friend()
        group_chat_set_page.wait_for_page_load(15)
        # 点击立即分享
        group_chat_set_page.click_sharing()
        # 点击分享到微信
        group_chat_set_page.click_share_wechat()
        # (无法抓去到弹窗文本，暂不使用)判断当前界面是否包含文本'该应用尚未安装，请安装后重试'
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('该应用尚未安装'), True)
        # 间接验证：点击分享到微信之后当前界面没有取消按钮
        self.assertEquals(group_chat_set_page.is_exist_cancel_button(), False)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0189(self):
        """群聊设置页面——进入到群管理详情页"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群管理
        group_chat_set_page.click_group_control()
        # 点击群主管理权转让
        group_chat_set_page.click_group_manage_transfer_button()
        # 判断当前页面是否为空页面
        self.assertEquals(group_chat_set_page.is_exist_empty_list(), True)
        time.sleep(2)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0141(self):
        """群主——清除旧名称——录入一个汉字"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群名称
        group_chat_page.click_group_name()
        # 修改群名称为'改'
        group_chat_page.input_group_name_message('改')
        # 点击完成
        group_chat_page.click_group_name_complete()
        group_chat_page.wait_for_page_setting_load()
        # 判断当前页面是否有'已经将群名称修改'文本
        self.assertEquals(group_chat_page.page_should_contain_text2('改'), True)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0141():
        """恢复环境，将用例修改的群聊名称修改为初始名称"""

        try:
            # 确认当前界面在消息界面然后进入到群聊'已经将群名称修改'
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page("改")
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群名称
            group_chat_page.click_group_name()
            # 修改群名称为'群聊1'
            group_chat_page.input_group_name_message('群聊1')
            # 点击完成
            group_chat_page.click_group_name_complete()
            group_chat_page.wait_for_page_setting_load()
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0173(self):
        """分享群二维码——搜索选择一个群"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群二维码
        group_chat_set_page.click_group_code()
        # 点击二维码转发按钮
        group_chat_set_page.click_code_forward()
        # 点击选择一个群
        select_contacts_page = SelectContactsPage()
        select_contacts_page.click_select_one_group()
        # 点击搜索群组
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.click_search_box()
        # 输入搜索内容搜索'群聊1'
        select_one_group_page.input_search_keyword('群聊1')
        # 点击'群聊1'
        select_one_group_page.selecting_one_group_by_name('群聊1 (1)')
        # 确认当前界面是否与取消按钮弹窗
        self.assertEquals(select_one_group_page.page_should_contain_text2('取消'), True)
        # 点击取消
        select_one_group_page.click_cancel_forward()
        # 确认当前界面是否在选择一个群界面
        self.assertEquals(select_one_group_page.page_should_contain_text2('群聊1'), True)
        # 再次点击'群聊1'
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.selecting_one_group_by_name('群聊1 (1)')
        # 点击发送
        select_one_group_page.click_sure_forward()
        # # 判断能否捕捉到'已分享'文本
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('已分享'), True)
        # 间接验证，无法捕捉到文本，验证是否返回群二维码界面
        self.assertEquals(group_chat_set_page.page_should_contain_text2('群二维码'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0174(self):
        """分享群二维码到——选择一个群"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群二维码
        group_chat_set_page.click_group_code()
        # 点击二维码转发按钮
        group_chat_set_page.click_code_forward()
        # 点击选择一个群
        select_contacts_page = SelectContactsPage()
        select_contacts_page.click_select_one_group()
        # 根据群名选择'群聊1'
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 确认当前界面是否与取消按钮弹窗
        self.assertEquals(select_one_group_page.page_should_contain_text2('取消'), True)
        # 点击取消
        select_one_group_page.click_cancel_forward()
        # 确认当前界面是否在选择一个群界面
        self.assertEquals(select_one_group_page.page_should_contain_text2('选择一个群'), True)
        # 再次点击'群聊1'
        select_one_group_page = SelectOneGroupPage()
        select_one_group_page.selecting_one_group_by_name('群聊1')
        # 点击发送
        select_one_group_page.click_sure_forward()
        # # 判断能否捕捉到'已分享'文本
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('已分享'), True)
        # 间接验证，无法捕捉到文本，验证是否返回群二维码界面
        self.assertEquals(group_chat_set_page.page_should_contain_text2('群二维码'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0179(self):
        """分享群二维码到——选择最近聊天"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('确保群聊出现在最近聊天列表中')
        group_chat_page.click_send_button()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击群二维码
        group_chat_set_page.click_group_code()
        # 点击二维码转发按钮
        group_chat_set_page.click_code_forward()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 通过名字找到'群聊1'
        select_contacts_page.selecting_one_group_by_name('群聊1')
        # 确认当前界面是否与取消按钮弹窗
        self.assertEquals(select_contacts_page.page_should_contain_text2('取消'), True)
        # 点击取消
        select_contacts_page.click_cancel_forward()
        # 确认当前界面是否在选择一个群界面
        self.assertEquals(select_contacts_page.page_should_contain_text2('选择联系人'), True)
        # 再次点击'群聊1'
        select_contacts_page.selecting_one_group_by_name('群聊1')
        # 点击发送
        select_contacts_page.click_send()
        # # 判断能否捕捉到'已分享'文本
        # self.assertEquals(group_chat_set_page.page_should_contain_text2('已分享'), True)
        # 间接验证，无法捕捉到文本，验证是否返回群二维码界面
        self.assertEquals(group_chat_set_page.page_should_contain_text2('群二维码'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0074(self):
        """仅语音模式，录制时长大于10秒——发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击语音按钮，等待十秒
        group_chat_page.click_voice_button()
        # 判断当前界面是否有文本'语音录制中'
        self.assertEquals(group_chat_page.page_should_contain_text2('语音录制中'), True)
        time.sleep(10)
        # 点击退出按钮
        group_chat_page.click_exit_voice()
        # 判断当前界面是否有'语音录制中'文本，
        self.assertEquals(group_chat_page.page_should_contain_text2('语音录制中'), False)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0109(self):
        """在群聊会话页，点击输入框——调起小键盘"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框
        group_chat_page.input_text_message(' ')
        # 判断当前界面是否有小键盘的麦克风标志
        self.assertEquals(group_chat_page.is_exist_msg_dictation(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0195(self):
        """群聊设置页面——查找聊天内容——是否可以调起小键盘"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_chat_record()
        # 判断界面是否有小键盘麦克风标志
        self.assertEquals(group_chat_set_page.is_exist_msg_dictation(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0269(self):
        """普通群——聊天会话页面——未进群联系人展示"""
        # 确认当前界面在消息界面
        Preconditions.make_already_in_message_page()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 点击加号
        message_page.click_add_icon()
        # 点击发起群聊
        message_page.click_group_chat()
        # 选择联系人界面
        select_contacts_page = SelectContactsPage()
        select_contacts_page.wait_for_page_load()
        # 点击选择手机联系人
        select_contacts_page.click_phone_contacts()
        # 通过文本点击添加(大佬1，大佬2)
        select_contacts_page.click_accessibility_id_attribute_by_name('大佬1')
        select_contacts_page.click_accessibility_id_attribute_by_name('大佬2')
        # 点击确定
        select_contacts_page.click_confirm_button()
        # 修改群聊名称
        select_contacts_page.input_group_name_message('测试1')
        # 点击创建
        select_contacts_page.click_create_button()
        time.sleep(3)
        # 点击输入框输入'测试文本第一次输入'
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        group_chat_page.input_text_message('测试文本第一次输入')
        # 获取当前页面图片数量1
        text1 = group_chat_page.get_picture_nums()
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 获取当前页面图片数量2看是否比上次获取图片数量多2
        text2 = group_chat_page.get_picture_nums()
        self.assertEquals(int(text2) - int(text1) == 2, True)
        # 输入文本并发送'测试文本第二次输入'
        group_chat_page.input_text_message('测试文本第二次输入')
        group_chat_page.click_send_button()
        time.sleep(2)
        # 获取当前页面图片数量3看是否比上次获取图片数量多2
        text3 = group_chat_page.get_picture_nums()
        self.assertEquals(int(text3) - int(text2) == 2, True)
        # 输入文本并发送'测试文本第三次输入'
        group_chat_page.input_text_message('测试文本第三次输入')
        group_chat_page.click_send_button()
        time.sleep(2)
        # 获取当前页面图片数量4看是否比上次获取图片数量多2
        text4 = group_chat_page.get_picture_nums()
        self.assertEquals(int(text4) - int(text3) == 2, True)
        # 输入文本并发送'测试文本第四次输入'
        group_chat_page.input_text_message('测试文本第四次输入')
        group_chat_page.click_send_button()
        time.sleep(2)
        # 获取当前页面图片数量5与上次图片数量比较不为2
        text5 = group_chat_page.get_picture_nums()
        self.assertEquals(int(text5) - int(text4) == 2, False)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0269():
        """恢复环境，将用例新建的群聊'测试1'解散"""
        # 前置条件在消息界面进入'测试1'界面
        try:
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page('测试1')
            group_chat_page = GroupChatPage()
            group_chat_page.wait_for_page_load()
            # 点击设置
            group_chat_page.click_setting()
            group_chat_page.wait_for_page_setting_load()
            # 点击群管理
            group_chat_page.click_group_control()
            # 点击解散群
            group_chat_page.click_group_dissolve()
            # 点击确认解散
            group_chat_page.click_group_dissolve_confirm()
            group_chat_page.click_back()
            time.sleep(2)
        finally:
            Preconditions.disconnect_mobile('IOS-移动')

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0196(self):
        """群聊设置页面——查找聊天内容——中文搜索——搜索结果展示"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('确保当前群聊有聊天内容存在')
        group_chat_page.click_send_button()
        # 点击设置
        group_chat_page.click_setting()
        # 群聊设置界面
        group_chat_set_page = GroupChatSetPage()
        group_chat_set_page.wait_for_page_load()
        # 点击查找聊天内容
        group_chat_set_page.click_find_message_records()
        time.sleep(2)
        find_chat_record_page = FindChatRecordPage()
        find_chat_record_page.wait_for_page_loads()
        # 输入搜索信息
        find_chat_record_page.input_search_message('确保当前群聊有聊天内容存在')
        # 判断是否有头像名称时间消息记录存在
        self.assertEquals(find_chat_record_page.is_exist_find_content(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_portrait(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_name(), True)
        self.assertEquals(find_chat_record_page.is_exist_find_time(), True)
        # 点击聊天记录
        find_chat_record_page.click_chat_records()
        group_chat_page.wait_for_page_load()
        # 判断当前是否在群聊页面
        self.assertEquals(group_chat_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0021(self):
        """在群聊天会话页面，输入框中录入1个字符，使用缩小功能发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入文字并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('A')
        group_chat_page.click_send_button()
        # 发送两次 第一次消息截取不到
        group_chat_page.input_text_message('A')
        group_chat_page.click_send_button()
        # 获取文本框大小1
        w1 = group_chat_page.get_width_of_last_msg()
        h1 = group_chat_page.get_height_of_last_msg()
        # 输入'1' 点击发送并向下滑动缩小文本并发送
        group_chat_page.input_text_message('A')
        group_chat_page.click_send_slide_down()
        # 获取文本大小2
        w2 = group_chat_page.get_width_of_last_msg()
        h2 = group_chat_page.get_height_of_last_msg()
        # 比较文本框大小 文本框1>文本框2
        self.assertEquals(int(w1) > int(w2), True)
        self.assertEquals(int(h1) > int(h2), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0027(self):
        """在群聊天会话页面，输入框中录入1个表情，使用缩小功能发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框点击表情按钮点击微笑表情并发送
        group_chat_page.get_input_box()
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_wx()
        group_chat_page.click_send_button()
        # 发送两次 第一次消息截取不到 发送窃喜表情
        group_chat_page.click_expression_qx()
        group_chat_page.click_send_button()
        # 获取文本框大小1
        w1 = group_chat_page.get_width_of_last_msg()
        h1 = group_chat_page.get_height_of_last_msg()
        # 输入流鼻涕表情点击发送并向下滑动缩小表情并发送
        group_chat_page.click_expression_lbt()
        group_chat_page.click_send_slide_down()
        # 获取文本大小2
        w2 = group_chat_page.get_width_of_last_msg()
        h2 = group_chat_page.get_height_of_last_msg()
        # 比较文本框大小 文本框1>文本框2
        self.assertEquals(int(w1) > int(w2), True)
        self.assertEquals(int(h1) > int(h2), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0031(self):
        """在群聊天会话页面，输入框中录入1个表情，使用放大功能发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框点击表情按钮点击微笑表情并发送
        group_chat_page.get_input_box()
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_wx()
        group_chat_page.click_send_button()
        # 发送两次 第一次消息截取不到 发送窃喜表情
        group_chat_page.click_expression_qx()
        group_chat_page.click_send_button()
        # 获取文本框大小1
        w1 = group_chat_page.get_width_of_last_msg()
        h1 = group_chat_page.get_height_of_last_msg()
        # 输入流鼻涕表情点击发送并向上滑动放大表情并发送
        group_chat_page.click_expression_lbt()
        group_chat_page.click_send_slide_up()
        # 获取文本大小2
        w2 = group_chat_page.get_width_of_last_msg()
        h2 = group_chat_page.get_height_of_last_msg()
        # 比较文本框大小 文本框1>文本框2
        self.assertEquals(int(w1) < int(w2), True)
        self.assertEquals(int(h1) < int(h2), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0035(self):
        """在群聊天会话页面，输入框中录入1个表情，使用放大功能发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入'我'点击表情按钮点击微笑表情并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我')
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_wx()
        group_chat_page.click_send_button()
        # 发送两次 第一次消息截取不到 发送窃喜表情
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我')
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_qx()
        group_chat_page.click_send_button()
        # 获取文本框大小1
        w1 = group_chat_page.get_width_of_last_msg()
        h1 = group_chat_page.get_height_of_last_msg()
        # 输入流鼻涕表情点击发送并向上滑动放大表情并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我')
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_lbt()
        group_chat_page.click_send_slide_up()
        # 获取文本大小2
        w2 = group_chat_page.get_width_of_last_msg()
        h2 = group_chat_page.get_height_of_last_msg()
        # 比较文本框大小 文本框1>文本框2
        self.assertEquals(int(w1) < int(w2), True)
        self.assertEquals(int(h1) < int(h2), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0036(self):
        """在群聊天会话页面，输入框中录入1个表情，使用缩小功能发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击输入框输入'我'点击表情按钮点击微笑表情并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我')
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_wx()
        group_chat_page.click_send_button()
        # 发送两次 第一次消息截取不到 发送窃喜表情
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我')
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_qx()
        group_chat_page.click_send_button()
        # 获取文本框大小1
        w1 = group_chat_page.get_width_of_last_msg()
        h1 = group_chat_page.get_height_of_last_msg()
        # 输入流鼻涕表情点击发送并向下滑动缩小表情并发送
        group_chat_page.get_input_box()
        group_chat_page.input_text_message('我')
        group_chat_page.click_expression_button()
        group_chat_page.click_expression_lbt()
        group_chat_page.click_send_slide_down()
        # 获取文本大小2
        w2 = group_chat_page.get_width_of_last_msg()
        h2 = group_chat_page.get_height_of_last_msg()
        # 比较文本框大小 文本框1>文本框2
        self.assertEquals(int(w1) > int(w2), True)
        self.assertEquals(int(h1) > int(h2), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0018(self):
        """群聊会话页面，使用拍照功能拍照编辑后发送照片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        message_page = MessagePage()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        time.sleep(2)
        chat_photo_page.click_edit_pic()
        # 编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        # 点击发送
        chat_pic_edit_page.click_send()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('图片'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0019(self):
        """群聊会话页面，使用拍照功能拍照之后编辑并保存"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        message_page = MessagePage()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        time.sleep(2)
        chat_photo_page.click_edit_pic()
        # 编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        # 点击保存
        chat_pic_edit_page.click_save()
        #  文本抓取不到
        # self.assertEquals(chat_pic_edit_page.page_should_contain_text2('已保存至系统相册'))
        time.sleep(2)
        # 点击发送
        chat_pic_edit_page.click_send()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('图片'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0020(self):
        """群聊会话页面，使用拍照功能拍照编辑图片，再取消编辑并发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        message_page = MessagePage()
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        time.sleep(2)
        chat_photo_page.click_edit_pic()
        # 编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 进行涂鸦操作
        chat_pic_edit_page.do_doodle()
        # 点击取消
        chat_pic_edit_page.click_cancle()
        # 点击发送
        chat_photo_page.send_photo()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('图片'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0022(self):
        """群聊会话页面，打开拍照，拍照之后返回会话窗口"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击返回
        chat_photo_page.take_photo_back()
        group_chat_page.wait_for_page_load()
        self.assertEquals(group_chat_page.page_should_contain_text2('群聊1'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0083(self):
        """群聊会话页面，发送相册内一个视频"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 先发送一条文本
        group_chat_page.input_text_message('测试文本')
        group_chat_page.click_send_button()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 点击发送
        chat_pic_page.click_send()
        time.sleep(10)
        group_chat_page.wait_for_page_load()
        # 判断是否有视频播放按钮
        self.assertEquals(group_chat_page.is_exist_video_play_button(), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0084(self):
        """群聊会话页面，发送相册内多个视频"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 获取点击视频后发送按钮文本1
        text1 = chat_pic_page.get_send_video_text()
        time.sleep(1)
        chat_pic_page.select_one_video(1)
        # 获取点击视频后发送按钮文本2
        text2 = chat_pic_page.get_send_video_text()
        # 比较文本1和2是否相同（间接验证发送按钮没有变化说明无法同时选取照片和视频）
        self.assertEquals(text1, text2)
        # # 判断是否有文本'只能选中一个视频'  文本捕捉不到暂不使用
        # self.assertEquals(chat_pic_page.page_should_contain_text2('只能选中一个视频'), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0085(self):
        """群聊会话页面，同时发送相册内视频和图片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 获取发送按钮文本1
        text1 = chat_pic_page.get_send_text()
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 获取点击视频后发送按钮文本2
        text2 = chat_pic_page.get_send_text()
        # 比较文本1和2是否相同（发送按钮没有变化说明无法同时选取照片和视频）
        self.assertEquals(text1, text2)
        # # 判断点击图片之后是否有文字提示不能同时选择照片和视频（有时会抓不到文本信息 不稳定）
        # self.assertEquals(chat_pic_page.page_should_contain_text2("不能同时选择照片和视频", 20), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoliping_D_0086(self):
        """群聊会话页面，发送视频时预览视频"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一个视频
        chat_pic_page.select_one_video()
        chat_pic_page.click_preview()
        # 判断是否有预览(1/1)文本
        self.assertEquals(chat_pic_page.page_should_contain_text2('预览(1/1)'), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0024(self):
        """我的电脑会话页面，不勾选相册内图片点击发送按钮"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 判断发送按钮enabled是否为false
        self.assertEquals(chat_pic_page.send_btn_is_enabled(), False)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0025(self):
        """我的电脑会话页面，勾选相册内一张图片发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        chat_pic_page.click_send()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('图片'), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0026(self):
        """我的电脑会话页面，预览相册内图片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        chat_pic_page.click_preview()
        self.assertEquals(chat_pic_page.page_should_contain_text2('预览(1/1)'), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0027(self):
        """我的电脑会话页面，预览相册内图片，不勾选原图发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_pictures(1)
        chat_pic_page.click_preview()
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.click_send()
        # 群聊界面
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('图片'), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0028(self):
        """我的电脑会话页面，预览相册数量与发送按钮数量一致"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击选择照片
        group_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择多张照片
        chat_pic_page.select_pictures(3)
        # 点击预览
        chat_pic_page.click_preview()
        # 预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 获取预览数文本
        text1 = chat_pic_preview_page.get_preview_text()
        # 获取发送按钮文本
        text2 = chat_pic_preview_page.get_send_text()
        # 判断预览数与发送数是否相等
        self.assertEquals(text1, text2)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0029(self):
        """我的电脑会话页面，编辑图片发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 滑动进行涂鸦
        chat_pic_edit_page.do_doodle()
        # 点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        # 滑动进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        # 点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        # 文本编辑
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0030(self):
        """我的电脑会话页面，编辑图片不保存发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击保存
        chat_pic_edit_page.click_save()
        self.assertEquals(chat_pic_edit_page.page_should_contain_text2('已保存至系统相册'), True)
        # 点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0031(self):
        """我的电脑会话页面，编辑图片中途直接发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        # 滑动进行涂鸦
        chat_pic_edit_page.do_doodle()
        # 点击马赛克按钮
        chat_pic_edit_page.click_mosaic()
        # 滑动进行马赛克操作
        chat_pic_edit_page.do_mosaic()
        # 点击文本编辑按钮
        chat_pic_edit_page.click_text_edit_btn()
        # 文本编辑
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0032(self):
        """我的电脑会话页面，编辑图片保存"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        # 点击完成
        chat_pic_edit_page.click_done()
        # 点击保存
        chat_pic_edit_page.click_save()
        self.assertEquals(chat_pic_edit_page.page_should_contain_text2('已保存至系统相册'), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0033(self):
        """我的电脑会话页面，取消编辑图片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        chat_pic_edit_page.click_done()
        # 点击取消
        chat_pic_edit_page.click_cancle()
        time.sleep(2)
        self.assertEquals(chat_pic_preview_page.page_should_contain_text2('预览(1/1)'), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0034(self):
        """我的电脑会话页面，取消编辑图片，点击发送按钮"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击图片按钮
        group_chat_page.click_picture()
        # 选择图片界面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 点击预览
        chat_pic_page.click_preview()
        # 图片预览界面
        chat_pic_preview_page = ChatPicPreviewPage()
        chat_pic_preview_page.wait_for_page_load()
        # 点击编辑
        chat_pic_preview_page.click_edit()
        # 图片编辑界面
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        chat_pic_edit_page.click_done()
        # 点击取消
        chat_pic_edit_page.click_cancle()
        time.sleep(2)
        # 点击发送
        chat_pic_preview_page.click_send()
        group_chat_page.wait_for_page_load()
        group_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertEquals(message_page.is_first_message_content('图片'), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0035(self):
        """我的电脑会话页面，发送相册内的图片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击选择照片
        group_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 获取当前页面图片数量
        numbers = chat_pic_page.get_pic_numbers()
        # 直接点击图片
        chat_pic_page.click_picture_just()
        chat_pic_edit_page = ChatPicEditPage()
        self.assertEquals(chat_pic_edit_page.page_should_contain_text2('预览(1/' + str(numbers)), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0037(self):
        """我的电脑会话页面，勾选9张相册内图片发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击选择照片
        group_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择九张图片
        chat_pic_page.select_pictures(9)
        # 点击发送
        chat_pic_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0038(self):
        """我的电脑会话页面，勾选9张相册内图片发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击选择照片
        group_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择九张图片
        chat_pic_page.select_pictures(9)
        # 判断第十个图片的点击按钮是否不可点击
        self.assertEquals(chat_pic_page.picture_btn_is_enabled(10), False)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0039(self):
        """我的电脑会话页面，同时发送相册中的图片和视频"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击选择照片
        group_chat_page.click_picture()
        # 选择图片页面
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        # 选择一张图片
        chat_pic_page.select_pictures(1)
        # 获取发送按钮文本1
        text1 = chat_pic_page.get_send_text()
        # 选择一个视频
        chat_pic_page.select_one_video()
        # 获取点击视频后发送按钮文本2
        text2 = chat_pic_page.get_send_text()
        # 比较文本1和2是否相同（发送按钮没有变化说明无法同时选取照片和视频）
        self.assertEquals(text1, text2)
        # # 判断点击图片之后是否有文字提示不能同时选择照片和视频（有时会抓不到文本信息 不稳定）
        # self.assertEquals(chat_pic_page.page_should_contain_text2("不能同时选择照片和视频", 20), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0040(self):
        """我的电脑会话页面，使用拍照功能并发送照片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        # 点击发送
        chat_photo_page.send_photo()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（发送图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0041(self):
        """我的电脑会话页面，使用拍照功能拍照编辑后发送照片"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        chat_photo_page.click_edit_pic()
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        chat_pic_edit_page.click_done()
        # 点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0042(self):
        """我的电脑会话页面，使用拍照功能拍照之后编辑并保存"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        chat_photo_page.click_edit_pic()
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        chat_pic_edit_page.click_done()
        # 点击保存
        chat_pic_edit_page.click_save()
        self.assertEquals(chat_pic_edit_page.page_should_contain_text2('已保存至系统相册'), True)
        # 点击发送
        chat_pic_edit_page.click_send()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0043(self):
        """我的电脑会话页面，使用拍照功能拍照编辑图片，再取消编辑并发送"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        # 点击拍照
        chat_photo_page.take_photo()
        chat_photo_page.click_edit_pic()
        chat_pic_edit_page = ChatPicEditPage()
        chat_pic_edit_page.wait_for_page_load()
        # 点击涂鸦按钮
        chat_pic_edit_page.click_doodle()
        chat_pic_edit_page.do_doodle()
        chat_pic_edit_page.click_mosaic()
        chat_pic_edit_page.do_mosaic()
        chat_pic_edit_page.click_text_edit_btn()
        chat_pic_edit_page.input_pic_text()
        chat_pic_edit_page.click_done()
        # 点击取消
        chat_pic_edit_page.click_cancle()
        # 点击发送
        chat_photo_page.send_photo()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 验证第一条消息是否为图片（编辑后图片无法验证，间接验证最后记录为图片）
        self.assertEquals(message_page.is_first_message_image(), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0044(self):
        """我的电脑会话页面，打开拍照，立刻返回会话窗口"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        chat_photo_page.take_photo_back()
        group_chat_page.wait_for_page_load()

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0045(self):
        """我的电脑会话页面，打开拍照，拍照之后返回会话窗口"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击富媒体拍照图标
        group_chat_page.click_take_picture()
        # 拍照页面
        chat_photo_page = ChatPhotoPage()
        chat_photo_page.wait_for_page_load()
        chat_photo_page.take_photo_back()
        group_chat_page.wait_for_page_load()

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0048(self):
        """在我的电脑会话窗，验证点击趣图搜搜入口"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        # 判断当前页面时候有关闭gif按钮
        self.assertEquals(group_chat_page.is_exist_closegif_page(), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0049(self):
        """在我的电脑会话窗，网络正常发送表情搜搜"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        # 点击发送GIF图片
        group_chat_page.click_send_gif()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 判断第一条消息是否为表情
        self.assertEquals(message_page.is_first_message_expression(), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0051(self):
        """在我的电脑会话窗，搜索数字关键字选择发送趣图"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        group_chat_page.input_text_message('1')
        time.sleep(1)
        # 点击发送GIF图片
        group_chat_page.click_send_gif()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 判断第一条消息是否为表情
        self.assertEquals(message_page.is_first_message_expression(), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0052(self):
        """在我的电脑会话窗，搜索特殊字符关键字发送趣图"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        group_chat_page.input_text_message('!')
        time.sleep(1)
        # 点击发送GIF图片
        group_chat_page.click_send_gif()
        # 等待页面加载
        group_chat_page.wait_for_page_load()
        # 点击返回按钮
        group_chat_page.click_back_button()
        # 等待页面加载
        message_page = MessagePage()
        message_page.wait_for_page_load()
        # 判断第一条消息是否为表情
        self.assertEquals(message_page.is_first_message_expression(), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0053(self):
        """在我的电脑会话窗，搜索无结果的趣图"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        group_chat_page.wait_for_page_load()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.wait_for_page_load()
        group_chat_page.input_text_message('！！！')
        # 判断是否有'无搜索结果'文本
        self.assertEquals(group_chat_page.page_should_contain_text2('无搜索结果'), True)

    @tags('ALL', 'CMCC')
    def test_msg_huangcaizui_D_0057(self):
        """在我的电脑会话窗，关闭GIF搜索框"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 点击表情按钮
        group_chat_page.click_expression_button()
        # 点击gif按钮
        group_chat_page.click_gif_button()
        group_chat_page.click_close_gif()
        # 判断当前页面是否还有关闭gif按钮，
        self.assertEquals(group_chat_page.is_exist_close_gif(), False)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0046(self):
        """发送一组数字：18431931414，发送成功后，是否会被识别为号码"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 输入数字'18431931414'
        group_chat_page.input_text_message('18431931414')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 输入数字'18431931414' 发送第一次文本无法捕捉需要发送两次
        group_chat_page.input_text_message('18431931414')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫', 2), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0047(self):
        """发送一组数字：+85267656003，发送成功后，是否会被识别为号码"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 输入数字'18431931414'
        group_chat_page.input_text_message('+85267656003')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 输入数字'18431931414' 发送第一次文本无法捕捉需要发送两次
        group_chat_page.input_text_message('+85267656003')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫', 2), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0048(self):
        """发送一组数字：67656003，发送成功后，是否会被识别为号码"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 输入数字'18431931414'
        group_chat_page.input_text_message('67656003')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 输入数字'18431931414' 发送第一次文本无法捕捉需要发送两次
        group_chat_page.input_text_message('67656003')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫', 2), True)

    @tags('ALL', 'CMCC')
    def test_msg_xiaoqiu_0049(self):
        """发送一组数字：95533，发送成功后，是否会被识别为号码"""
        # 确认当前界面在消息界面 然后进入群聊1
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page('群聊1')
        group_chat_page = GroupChatPage()
        group_chat_page.wait_for_page_load()
        # 输入数字'18431931414'
        group_chat_page.input_text_message('95533')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 输入数字'18431931414' 发送第一次文本无法捕捉需要发送两次
        group_chat_page.input_text_message('95533')
        # 点击发送
        group_chat_page.click_send_button()
        time.sleep(2)
        # 点击该行数字
        group_chat_page.click_text_message_by_number(-1)
        # 判断点击之后是否出现呼叫按钮
        self.assertEquals(group_chat_page.page_should_contain_text2('呼叫', 2), True)


















