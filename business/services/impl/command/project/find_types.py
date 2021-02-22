
from api_connection.exceptions.request_exception import RequestError
from api_connection.requests.get_request import GetRequest
from business.exception.business_error import BusinessError
from business.services.impl.command.project.project_command import ProjectCommand
from model.type import Type


class FindTypes(ProjectCommand):

    def __init__(self, connection, project):
        """Constructor for class FindTypes, from ProjectCommand

        :param connection: The connection data
        :param project: The project to get its types
        """
        super().__init__(connection)
        self.project = project

    def execute(self):
        try:
            json_obj = GetRequest(self.connection, f"{self.CONTEXT}/{self.project.id}/types").execute()
            for tEntry in json_obj["_embedded"]["elements"]:
                yield Type(tEntry)
        except RequestError as re:
            raise BusinessError("Error finding work package types") from re
