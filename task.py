import sys
import toml

class ConfigTransformer:
    def __init__(self):
        self.constants = {}

    def parse_toml(self, toml_data):
        try:
            return toml.loads(toml_data)
        except toml.TomlDecodeError as e:
            sys.stderr.write(f"Синтаксическая ошибка TOML: {e}\n")
            sys.exit(1)

    def transform_value(self, value):
        if isinstance(value, str):
            return f"q({value})"
        elif isinstance(value, int) or isinstance(value, float):
            return str(value)
        elif isinstance(value, list):
            return "{ " + ", ".join(self.transform_value(v) for v in value) + " }"
        else:
            sys.stderr.write(f"Неподдерживаемый тип значения: {value}\n")
            sys.exit(1)

    def transform_dict(self, data):
        lines = []
        for key, value in data.items():
            if key.startswith("max_"):
                lines.append(f"def {key} = {self.transform_value(value)};")
            else:
                lines.append(f"{key} = {self.transform_value(value)}")
        return "\n".join(lines)
    
    def transform(self, toml_data):
        parsed_data = self.parse_toml(toml_data)
        return self.transform_dict(parsed_data)

if __name__ == "__main__":
    input_data = sys.stdin.read()
    transformer = ConfigTransformer()
    output_data = transformer.transform(input_data)
    print(output_data)
