from injector import Injector
from core.domain.language.validators.language_validator import (
    LanguageValidator,
    ValidateLanguageData,
)

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
    """
    Puertos de entrada y salida para la síntesis de voz.
    """

    def input(self, request: TTSRequest) -> SynthesizeSpeechFeatureInput:
        """
        Transforma y valida la petición de un controlador en una entrada para
        la característica de síntesis de voz.
        """
        injector = Injector()
        validator = injector.get(LanguageValidator)

        validator.validate(ValidateLanguageData(code=request.source))
        return SynthesizeSpeechFeatureInput(**dict(request))

    def output(self, output: SynthesizeSpeechFeatureOutput | None) -> TTSResponse:
        """
        Transforma la salida de la característica de síntesis de voz en una
        respuesta para un controlador.
        """
        return TTSResponse(speech=str(output.speech) if output is not None else None)
