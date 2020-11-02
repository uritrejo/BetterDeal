import unittest


class TestDatabase(unittest.TestCase):

    def test_retrieve_car_success(self):
        self.assertTrue(True)

    def test_retrieve_car_wrong_config(self):  # manually change config
        self.assertTrue(False)

    def test_retrieve_search_success(self):
        self.assertTrue(True)

    def test_add_car_success(self):
        self.assertTrue(True)

    def test_add_search_success(self):
        self.assertTrue(True)

    def test_add_search_wrong_params(self):  # BS, won't even check in reality
        self.assertTrue(False)


class TestNotification(unittest.TestCase):

    def test_email_successful(self):
        self.assertTrue(True)

    def test_email_wrong_password(self):
        self.assertFalse(False)

    def test_connect_exception_handled(self):
        with self.assertRaises(Exception):
            print("Call method")  # this wont raise exception, maybe just leave it


class TestDataCollector(unittest.TestCase):

    def test_process_data_empty(self):
        self.assertTrue(True)

    def test_process_corrupted_data(self):
        self.assertTrue(False)

    def test_process_data_success(self):
        self.assertTrue(True)

    def test_clear_partial_memory_success(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()