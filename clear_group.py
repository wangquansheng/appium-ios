from pages import ContactsPage
from pages import GroupListPage
from pages import MessagePage
from preconditions.BasePreconditions import WorkbenchPreconditions


def delete_all_group_chat():
    """删除所有群聊"""
    WorkbenchPreconditions.select_mobile('IOS-移动')
    try:
        mp = MessagePage()
        mp.open_contacts_page()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.open_group_chat_list()
        glp = GroupListPage()
        glp.wait_for_page_load()
        glp.delete_all_group_chat()
    finally:
        WorkbenchPreconditions.disconnect_mobile('IOS-移动')


if __name__ == '__main__':
    delete_all_group_chat()
