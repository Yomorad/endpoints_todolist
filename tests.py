import unittest
from app import app

class TestAppControllers(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_tasks_list_get(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        if response.data != b'[]\n' :  # Проверка, что response.data не пустой
            self.assertTrue(True)
        else:
            self.fail("No data received in response")

    def test_tasks_list_post(self):
        title_dict = {"title": "Test Task"}
        response = self.app.post('/tasks', json=title_dict)
        self.assertEqual(response.status_code, 200)
        # декодируем ответ в строку и проверяем, что данные есть
        data_str = response.data.decode('utf-8')
        if response.data != b'[]' and title_dict['title'] in data_str :  # Проверка, что response.data не пустой
            self.assertTrue(True)
        else:
            self.fail("No data received in response")

    def test_tasks_id_get(self):
        response = self.app.get('/tasks/2')
        self.assertEqual(response.status_code, 200)
        if response.data != b'[]\n' :  # Проверка, что response.data не пустой
            self.assertTrue(True)
        else:
            self.fail("No data received in response")

    def test_tasks_id_put(self):
        response_before = self.app.put('/tasks/2', json={"title": "Old Task"})
        response_after = self.app.put('/tasks/2', json={"title": "Updated Task"})
        self.assertEqual(response_after.status_code, 200)
        self.assertNotEqual(response_before, response_after)

    def test_tasks_id_delete(self):
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)
        expected_message = b'{"message":"Task deleted successfully"}\n'
        actual_message = response.data
        self.assertEqual(actual_message, expected_message)

if __name__ == '__main__':
    unittest.main()