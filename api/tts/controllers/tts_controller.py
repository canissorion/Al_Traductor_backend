from api.controller import Controller
from api.tts.adapters.tts_request import TTSRequest
from api.tts.adapters.tts_response import TTSResponse
from core.tts.features.synthesize_speech_feature import SynthesizeSpeechFeature


class TTSController(Controller):
    def register(self) -> None:
        @self.app.post("/tts", response_model=TTSResponse)
        def post(request: TTSRequest) -> TTSResponse:
            synthesize = SynthesizeSpeechFeature()
            speech = synthesize(*request.dict().values())
            return TTSResponse(speech=speech)
