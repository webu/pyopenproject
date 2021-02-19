from business.services.impl.command.post.add_attachment import AddAttachment
from business.services.impl.command.wiki_page.find import Find
from business.services.impl.command.wiki_page.find_attachments import FindAttachments
from business.services.wiki_page_service import WikiPageService


class WikiPageServiceImpl(WikiPageService):

    def __init__(self, connection):
        super().__init__(connection)

    def find(self, wiki_page):
        return Find(self.connection, wiki_page).execute()

    def find_attachments(self, wiki):
        return list(FindAttachments(self.connection, wiki).execute())

    def add_attachment(self, wiki, attachment):
        return AddAttachment(self.connection, wiki, attachment).execute()