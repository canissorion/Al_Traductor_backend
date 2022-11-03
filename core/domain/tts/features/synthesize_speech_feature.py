from core.kernel.feature.feature import Feature
from core.kernel.feature.feature_input import FeatureInput
from core.kernel.feature.feature_output import FeatureOutput


class SynthesizeSpeechFeatureInput(FeatureInput):
    source: str
    text: str


class SynthesizeSpeechFeatureOutput(FeatureOutput):
    speech: str | None = None


# TODO(davideliseo): Implementar.
class SynthesizeSpeechFeature(
    Feature[SynthesizeSpeechFeatureInput, SynthesizeSpeechFeatureOutput]
):
    def execute(
        self,
        input: SynthesizeSpeechFeatureInput,
    ) -> SynthesizeSpeechFeatureOutput:
        return SynthesizeSpeechFeatureOutput(
            speech=f"{__class__.__name__}: Not implemented."
        )
