import unittest
from task import ConfigTransformer

class TestConfigTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = ConfigTransformer()

    def test_simple_config(self):
        toml_data = """
        server = "localhost"
        port = 8080
        """
        expected_output = "server = q(localhost)\nport = 8080"
        self.assertEqual(self.transformer.transform(toml_data), expected_output)

    def test_constants(self):
        toml_data = """
        def max_connections = 100
        @max_connections
        """
        expected_output = "def max_connections = 100;\n@[ max_connections ]"
        self.assertEqual(self.transformer.transform(toml_data), expected_output)

    def test_arrays(self):
        toml_data = """
        routes = ["home", "about", "contact"]
        """
        expected_output = "routes = { q(home), q(about), q(contact) }"
        self.assertEqual(self.transformer.transform(toml_data), expected_output)

if __name__ == "__main__":
    unittest.main()
