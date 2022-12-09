from functools import partial
import uvicorn  # pyright: ignore
from app import create_app
from settings import AppEnv, get_settings

app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    env = settings.app_env
    run = partial(uvicorn.run, "main:app", host="0.0.0.0", port=8000)  # pyright: ignore

    if env == AppEnv.PRODUCTION:
        run()
    else:
        run(debug=True, reload=True, log_level="info")
