from pages.api.base_api import BaseAPI


class NotesAPI(BaseAPI):

    def create_note(self, token: str, payload: dict):
        return self.post(
            '/notes/api/notes',
            data=payload,
            headers={'x-auth-token': token},
        )

    def get_all(self, token: str):
        return self.get(
            '/notes/api/notes',
            headers={'x-auth-token': token},
        )

    def get_by_id(self, token: str, note_id: int):
        return self.get(
            f'/notes/api/notes/{note_id}',
            headers={'x-auth-token': token},
        )
