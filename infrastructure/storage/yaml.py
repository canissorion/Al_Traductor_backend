from typing import Any
import yaml


class YAMLStorage:
    """
    Driver de almacenamiento en YAML.

    Atributos:
        - filename: Nombre del archivo.
    """

    filename: str

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def read(self) -> dict[str, Any] | None:
        """
        Lee los datos del archivo.
        """
        with open(self.filename, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError:
                return None

    def write(self, data: Any) -> None:
        """
        Escribe los datos en el archivo.
        """
        with open(self.filename, "w+") as handle:
            yaml.dump(data, handle)

    def close(self) -> None:
        """
        Cierra el archivo.
        """
        pass
