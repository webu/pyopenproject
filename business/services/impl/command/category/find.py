from api_connection.connection import Connection
from api_connection.exceptions.request_exception import RequestError
from business.exception.business_error import BusinessError
from business.services.impl.command.category.category_command import CategoryCommand
from model.category import Category


class Find(CategoryCommand):

    def __init__(self, category):
        self.category = category

    def execute(self):
        try:
            json_obj = Connection().get(f"{self.CONTEXT}/{self.category.id}")
            return Category(json_obj)
        except RequestError as re:
            raise BusinessError(f"Error finding category by id: {self.category.id}") from re
