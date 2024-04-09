from pathlib import Path


class MockBot:
    def __init__(self, output_file):
        self.output_file = output_file
        self.output_path = Path(f'../output/{self.output_file}.txt')
        self.output_path.parent.mkdir(exist_ok=True, parents=True)

    def send_message(self, chat_id, msg):
        with open(self.output_path, "a") as f:
            f.write(msg + '\n')

    def send_photo(self, chat_id, url):
        with open(self.output_path, "a") as f:
            f.write(url + '\n')
