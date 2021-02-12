import model.version as v
from api_connection.exceptions.request_exception import RequestError
from api_connection.requests.patch_request import PatchRequest
from business.exception.business_error import BusinessError
from business.services.impl.command.version.version_command import VersionCommand


class Update(VersionCommand):

    def __init__(self, connection, version):
        super().__init__(connection)
        self.version = version

    def execute(self):
        try:
            version_id = self.version.id
            self.__remove_readonly_attributes()
            json_obj = PatchRequest(connection=self.connection,
                                    context=f"{self.CONTEXT}/{version_id}",
                                    json=self.version.__dict__,
                                    headers={"Content-Type": "application/json"}).execute()
            return v.Version(json_obj)
        except RequestError as re:
            raise BusinessError(f"Error updating version: {self.version.id}") from re

    def __remove_readonly_attributes(self):
        del self.version.__dict__["_links"]
        del self.version.__dict__["id"]
        del self.version.__dict__["createdAt"]
        del self.version.__dict__["updatedAt"]
