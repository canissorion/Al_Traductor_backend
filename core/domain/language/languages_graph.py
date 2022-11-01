from typing import Iterator, TypeAlias
from injector import inject
import itertools
import networkx as nx  # pyright: ignore

from core.domain.language.language import LanguageModel
from core.domain.language.repositories.languages_repository import LanguagesRepository


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

            TODO(davideliseo): Contraer las aristas de los subconjuntos de
            nodos cuyo subgrafo inducido sea un grafo completo (clique).
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
        model: LanguageModel | None,
    ) -> Iterator[Edge]:
        def best_model(source: str, target: str) -> LanguageModel:
            models = set[LanguageModel](self.graph.get_edge_data(source, target).keys())  # pyright: ignore
            return model if model in models else LanguageModel.CLOUD

        path = list[str](nx.shortest_path(self.graph, source, target))  # pyright: ignore
        return ((*pair, best_model(*pair)) for pair in itertools.pairwise(path))
    # fmt: on
