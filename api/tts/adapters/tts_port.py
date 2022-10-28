from core.kernel.port import Port
from api.tts.adapters.tts_request import TTSRequest
from api.tts.adapters.tts_response import TTSResponse
from core.domain.tts.features.synthesize_speech_feature import (
    SynthesizeSpeechFeatureInput,
    SynthesizeSpeechFeatureOutput,
)


class TTSPort(
    Port[
        TTSRequest,
        TTSResponse,
        SynthesizeSpeechFeatureInput,
        SynthesizeSpeechFeatureOutput,
    ]
):
    def input(self, request: TTSRequest) -> SynthesizeSpeechFeatureInput:
        return SynthesizeSpeechFeatureInput(**dict(request))

    def output(self, output: SynthesizeSpeechFeatureOutput | None) -> TTSResponse:
        return TTSResponse(speech=str(output.value) if output is not None else None)
