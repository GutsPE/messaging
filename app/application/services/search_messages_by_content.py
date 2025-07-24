from app.domain.repositories.message_repository import MessageRepository

class SearchMessagesByContent:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    def execute(
        self, 
        query: str, 
        limit: int = 10, 
        offset: int = 0
    ):
        return self.repository.search_by_content(query, limit, offset)