from injector import Injector

from api.controller import Controller
from api.tts.adapters.tts_port import TTSPort
from api.tts.adapters.tts_request import TTSRequest
from api.tts.adapters.tts_response import TTSResponse
from core.domain.tts.features.synthesize_speech_feature import SynthesizeSpeechFeature


class TTSController(Controller):
    def register(self) -> None:
        @self.app.post("/tts", response_model=TTSResponse)
        def _(request: TTSRequest) -> TTSResponse:
            injector = Injector()
            synthesize = injector.get(SynthesizeSpeechFeature)
            port = injector.get(TTSPort)
            speech = synthesize.execute(input=port.input(request))
            return port.output(output=speech)
