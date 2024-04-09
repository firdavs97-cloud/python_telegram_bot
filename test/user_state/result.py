import states.user_state as mock_user_state
from test.mock_data.info_send_dict import samples as data
from test.mock_data.data_properties import data_properties
from test.mock_db.mysql import MockHistory
from test.mock_model.bot import MockBot
from test.mock_model.message import MockMessage

mock_user_state.bot = MockBot('user_state__result')
mock_user_state.reset = lambda x: x
mock_user_state.history = MockHistory("user_state__result")


def mock_result():
    for i, info_send_dict in enumerate(data):
        mock_user_state.info_hotels_properties = lambda x: data_properties[i]
        message = MockMessage(f'test_case{i+1}', "mock_result")
        mock_user_state.result(message, info_send_dict)


if __name__ == '__main__':
    mock_result()
