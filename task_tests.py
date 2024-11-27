import unittest
from task import ConfigTransformer

class TestConfigTransformer(unittest.TestCase):
    def setUp(self):
        # Инициализация объекта для тестов
        self.transformer = ConfigTransformer()

    def test_simple_string(self):
        # Тест на простую строку
        toml_data = 'server = "localhost"'
        expected_output = 'server = q(localhost)'
        self.assertEqual(self.transformer.transform(toml_data), expected_output)

    def test_simple_number(self):
        # Тест на число
        toml_data = 'port = 8080'
        expected_output = 'port = 8080'
        self.assertEqual(self.transformer.transform(toml_data), expected_output)

    def test_array(self):
        # Тест на массив
        toml_data = 'routes = ["home", "about", "contact"]'
        expected_output = 'routes = { q(home), q(about), q(contact) }'
        self.assertEqual(self.transformer.transform(toml_data), expected_output)

    def test_constant(self):
        # Тест на константу
        toml_data = 'max_connections = 100'
        expected_output = 'def max_connections = 100;'
        self.assertEqual(self.transformer.transform(toml_data), expected_output)

    def test_complex_config(self):
        # Тест на сложную конфигурацию
        toml_data = '''
        server = "localhost"
        port = 8080
        routes = ["home", "about", "contact"]
        max_connections = 100
        '''
        expected_output = (
            'server = q(localhost)\n'
            'port = 8080\n'
            'routes = { q(home), q(about), q(contact) }\n'
            'def max_connections = 100;'
        )
        self.assertEqual(self.transformer.transform(toml_data), expected_output)

    def test_invalid_toml(self):
        invalid_toml_data = 'server = "localhost'
        with self.assertRaises(SystemExit): 
            self.transformer.transform(invalid_toml_data)

if __name__ == "__main__":
    unittest.main()

#python -m unittest task_tests.py