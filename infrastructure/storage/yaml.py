from typing import Any
import yaml


class YAMLStorage:
    filename: str

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def read(self) -> dict[str, Any] | None:
        with open(self.filename, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError:
                return None

    def write(self, data: Any) -> None:
        with open(self.filename, "w+") as handle:
            yaml.dump(data, handle)

    def close(self) -> None:
        pass
