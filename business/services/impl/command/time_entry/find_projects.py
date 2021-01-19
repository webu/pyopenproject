import json

from api_connection.exceptions.request_exception import RequestError
from api_connection.requests.get_request import GetRequest
from business.exception.business_error import BusinessError
from business.services.impl.command.time_entry.time_entry_command import TimeEntryCommand
from model.project import Project


class FindProjects(TimeEntryCommand):

    def __init__(self, connection):
        self.connection = connection

    def execute(self):
        try:
            json_obj = GetRequest(self.connection, f"{self.CONTEXT}/available_projects").execute()
            for tEntry in json.loads(json_obj):
                yield Project(tEntry)
        except RequestError as re:
            raise BusinessError(f"Error finding all projects by context: {self.context}") from re