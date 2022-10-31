from core.kernel.feature.feature import Feature
from core.kernel.feature.feature_input import FeatureInput
from core.kernel.feature.feature_output import FeatureOutput


class SynthesizeSpeechFeatureInput(FeatureInput):
    source: str
    text: str


class SynthesizeSpeechFeatureOutput(FeatureOutput):
    pass


# TODO(davideliseo): Implementar.
class SynthesizeSpeechFeature(
    Feature[SynthesizeSpeechFeatureInput, SynthesizeSpeechFeatureOutput]
):
    def execute(
        self,
        input: SynthesizeSpeechFeatureInput,
    ) -> SynthesizeSpeechFeatureOutput:
        return SynthesizeSpeechFeatureOutput(
            value=f"{__class__.__name__}: Not implemented."
        )
