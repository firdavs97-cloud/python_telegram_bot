from telebot.types import Message, Chat


class User:
    def __init__(self, id):
        self.id = id


class MockMessage(Message):
    def __init__(self, message_id, mock_user_id):
        super().__init__(message_id, User(id=mock_user_id), None, Chat(id="test", type="test"), None, {}, None)

