from typing import Iterator, TypeAlias
from injector import inject
import itertools
import networkx as nx  # pyright: ignore

from core.domain.language.language import LanguageModel
from core.domain.language.repositories.languages_repository import LanguagesRepository
from core.domain.translation.validators.translation_model_validator import (
    ModelNotSupportedByTranslationError,
)


Edge: TypeAlias = tuple[str, str, LanguageModel]


class LanguagesGraph:
    graph: nx.classes.MultiDiGraph
    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository):
        self.graph = nx.MultiDiGraph()
        self.languages_repository = languages_repository
        self.graph.add_edges_from(self.edges())  # pyright: ignore

    def edges(self) -> Iterator[Edge]:
        def greedy_edges(model: LanguageModel) -> Iterator[Edge]:
            """
            Generas las aristas de aquellas configuraciones de modelos de tipo
            greedy. La configuración de modelo de tipo greedy de un idioma es
            aquella que asume compatibilidad con todos los demás idiomas del
            mismo modelo, exceptuando aquellos que estén excluidos
            explícitamente.
            """
            languages = self.languages_repository.query(model)
            for source, target in itertools.permutations(languages, 2):
                if source.models[model].includes(target.code):
                    yield (source.code, target.code, model)

        def lazy_edges(model: LanguageModel) -> Iterator[Edge]:
            """
            Generas las aristas de aquellas configuraciones de modelos de tipo
            lazy. La configuración de modelo de tipo lazy de un idioma es
            aquella que asume compatibilidad solo con los idiomas del mismo
            modelo que estén incluidos explícitamente.
            """
            languages = self.languages_repository.query(model)
            for language in languages:
                settings = language.models[model]
                for target in settings.support.targets:
                    yield (language.code, target, model)

        return itertools.chain(
            lazy_edges(model=LanguageModel.ML),
            greedy_edges(model=LanguageModel.CLOUD),
        )

    # fmt: off
    def path(
        self,
        source: str,
        target: str,
        model: LanguageModel | None = None,
    ) -> Iterator[Edge]:
        path = list[str](nx.shortest_path(self.graph, source, target))  # pyright: ignore
        return ((*pair, self.fit_model(*pair, model)) for pair in itertools.pairwise(path))

    def models(self, source: str, target: str) -> set[LanguageModel]:
        return set[LanguageModel](self.graph.get_edge_data(source, target).keys())  # pyright: ignore

    def fit_model(
        self,
        source: str,
        target: str,
        model: LanguageModel | None = None,
    ) -> LanguageModel:
        models = self.models(source, target)

        if model is None:
            return min(models, key=LanguageModel.precedence)
        elif model in models:
            return model

        raise ModelNotSupportedByTranslationError(model, source, target)
    # fmt: on
