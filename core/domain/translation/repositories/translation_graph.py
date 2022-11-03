from typing import Iterator, TypeAlias
from injector import inject
from itertools import chain, pairwise, permutations
from networkx import MultiDiGraph, shortest_path  # pyright: ignore

from core.domain.language.language import LanguageModel
from core.domain.language.repositories.languages_repository import LanguagesRepository
from core.domain.translation.validators.translation_model_validator import (
    ModelNotSupportedByTranslationError,
)


# Arista del grafo de traducción. El primer elemento es el código origen de
# traducción, el segundo es el código destino y el tercero es el modelo de
# traducción.
Edge: TypeAlias = tuple[str, str, LanguageModel]


class TranslationGraph:
    """
    Grafo multidireccional ponderado por modelos de traducción, cuyos nodos
    son los idiomas y las aristas las configuraciones de traducción entre
    ellos.

    TODO(davideliseo): Optimizar almacenando el grafo en el caché. Las
    escrituras al repositorio de lenguajes son mínimas; las lecturas son
    constantes.
    """

    graph: MultiDiGraph
    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository):
        self.graph = MultiDiGraph()
        self.languages_repository = languages_repository
        self.graph.add_edges_from(self.edges())  # pyright: ignore

    def edges(self) -> Iterator[Edge]:
        def greedy_edges(model: LanguageModel) -> Iterator[Edge]:
            """
            Genera las aristas de las configuraciones de modelos de tipo
            greedy, es decir, aquellas que asumen compatibilidad con todos los
            demás idiomas del mismo modelo, exceptuando los que estén excluidos
            explícitamente.
            """
            languages = self.languages_repository.query(model)
            return (
                (source.code, target.code, model)
                for source, target in permutations(languages, 2)
                if source.models[model].includes(target.code)
            )

        def lazy_edges(model: LanguageModel) -> Iterator[Edge]:
            """
            Genera las aristas de las configuraciones de modelos de tipo lazy,
            es decir, aquellas que asumen compatibilidad solo con los idiomas
            del mismo modelo que estén incluidos explícitamente.
            """
            languages = self.languages_repository.query(model)
            return (
                (language.code, target, model)
                for language in languages
                for target in language.models[model].support.targets
            )

        return chain(
            lazy_edges(model=LanguageModel.ML),
            greedy_edges(model=LanguageModel.CLOUD),
        )

    def path(
        self, source: str, target: str, model: LanguageModel | None = None
    ) -> Iterator[Edge]:
        """
        Determina la trayectoria de traducción más corta entre dos idiomas.
        """
        path = list[str](shortest_path(self.graph, source, target))  # pyright: ignore
        return ((*pair, self.fit_model(*pair, model)) for pair in pairwise(path))

    def models(self, source: str, target: str) -> set[LanguageModel]:
        """
        Determina los modelos de traducción compatibles entre dos idiomas.
        """
        return set(self.graph.get_edge_data(source, target).keys())  # pyright: ignore

    def fit_model(
        self, source: str, target: str, model: LanguageModel | None = None
    ) -> LanguageModel:
        """
        Determina el modelo de traducción más adecuado entre dos idiomas.
        """
        models = self.models(source, target)

        if model is None:
            # Si no se especifica un modelo, se elige el de menor precedencia.
            return min(models, key=LanguageModel.precedence)
        elif model in models:
            return model

        raise ModelNotSupportedByTranslationError(model, source, target)
