from core.kernel.feature.feature import Feature
from core.kernel.feature.feature_input import FeatureInput
from core.kernel.feature.feature_output import FeatureOutput


class SynthesizeSpeechFeatureInput(FeatureInput):
    """
    Datos de entrada de la característica de síntesis de voz.

    Atributos:
        - source: Idioma del texto a sintetizar.
        - text: Texto a sintetizar.
    """

    source: str
    text: str


class SynthesizeSpeechFeatureOutput(FeatureOutput):
    """
    Datos de salida de la característica de síntesis de voz.

    Atributos:
        - speech: Audio de la síntesis de voz.

    TODO(davideliseo): Definir el tipo de salida.
    """

    speech: str | None = None


class SynthesizeSpeechFeature(Feature[SynthesizeSpeechFeatureInput, SynthesizeSpeechFeatureOutput]):
    """
    Característica de síntesis de voz.

    TODO(davideliseo): Implementar.
    """

    def execute(self, input: SynthesizeSpeechFeatureInput) -> SynthesizeSpeechFeatureOutput:
        return SynthesizeSpeechFeatureOutput(speech=f"{__class__.__name__}: Not implemented.")
