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
            if key.startswith("def "):
                const_name = key.split(" ")[1]
                self.constants[const_name] = value
                lines.append(f"def {const_name} = {self.transform_value(value)};")
            elif key.startswith("@"):
                const_name = key[1:]
                if const_name in self.constants:
                    lines.append(f"@[ {const_name} ]")
                else:
                    sys.stderr.write(f"Ошибка: Константа '{const_name}' не определена.\n")
                    sys.exit(1)
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
