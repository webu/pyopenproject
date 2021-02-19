import json

import business.service_factory as service_factory


class Attachment:

    def __init__(self, json_obj):
        self.__dict__ = json_obj

    def get_container(self):
        if self._links.workPackage.href is not None:
            return service_factory.ServiceFactory.get_work_package_service()\
                .find_by_context(self._link.container.href)
        return None

    def get_author(self):
        if self._links.author.href is not None:
            return service_factory.ServiceFactory.get_user_service()\
                .find_by_context(self._links.author.href)
        return None

    def static_download_location(self):
        if self._links.staticDownloadLocation.href is not None:
            return service_factory.ServiceFactory.get_attachment_service()\
                .download_by_context(self._links.staticDownloadLocation.href)
        return None

    def download_location(self):
        if self.__dict__["_links"]["downloadLocation"]["href"] is not None:
            return service_factory.ServiceFactory.get_attachment_service() \
                .download_by_context(self.__dict__["_links"]["downloadLocation"]["href"])
        return None

    def __str__(self):
        return json.dumps(self.__dict__)