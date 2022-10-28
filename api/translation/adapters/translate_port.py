from core.domain.translation.features.translate_feature import (
    TranslateFeatureInput,
    TranslateFeatureOutput,
)
from core.kernel.port import Port
from api.translation.adapters.translate_request import TranslateRequest
from api.translation.adapters.translate_response import TranslateResponse


class TranslatePort(
    Port[
        TranslateRequest,
        TranslateResponse,
        TranslateFeatureInput,
        TranslateFeatureOutput,
    ]
):
    def input(self, request: TranslateRequest) -> TranslateFeatureInput:
        return TranslateFeatureInput(**dict(request))

    def output(self, output: TranslateFeatureOutput | None) -> TranslateResponse:
        return TranslateResponse(
            translation=str(output.value) if output is not None else None
        )
