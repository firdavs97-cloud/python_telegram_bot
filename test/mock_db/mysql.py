class MockHistory:
    def __init__(self, name):
        self.name = name

    def insert_result(self, history_id, msg):
        print(f'Результат теста {self.name} c параметрами из шаблона №{history_id}')
        print(msg)
