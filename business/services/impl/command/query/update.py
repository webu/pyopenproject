import json

from api_connection.exceptions.request_exception import RequestError
from api_connection.requests.patch_request import PatchRequest
from business.exception.business_error import BusinessError
from business.services.impl.command.query.query_command import QueryCommand
from model.query import Query


class Update(QueryCommand):

    def __init__(self, connection, query):
        super().__init__(connection)
        self.query = query

    def execute(self):
        try:
            # TODO: We need to review this request for an update
            json_obj = PatchRequest(connection=self.connection,
                                    context=f"{self.CONTEXT}/{self.query.id}",
                                    json=json.dumps(self.project.__dict__)).execute()
            return Query(json_obj)
        except RequestError as re:
            raise BusinessError(f"Error updating query by id: {self.query.id}") from re