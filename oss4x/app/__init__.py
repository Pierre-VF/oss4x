import os
from contextlib import asynccontextmanager
from datetime import datetime
from importlib.metadata import version

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from oss4x.app.src import mcp_server
from oss4x.app.src.app_config import AppConfig
from oss4x.app.src.config import (
    FILE_OUTPUT_LISTING_FEATHER,
    STATIC_FILES_PATH,
    set_current_config,
)
from oss4x.app.src.data_io import download_listing_data_for_app
from oss4x.app.src.log_activity import log_landing
from oss4x.app.src.mcp_server import mcp
from oss4x.app.src.routers import api, ui
from oss4x.app.src.templates import render_template
from oss4x.app.src.theme import (
    Theme,
    ThemeColors,
    ThemeShadows,
    ThemeSpacing,
    ThemeTransitions,
    ThemeTypography,
)
from oss4x.src.config import SETTINGS as _DEFAULT_SETTINGS
from oss4x.src.config import Settings
from oss4x.src.log import log_info

_ENV_TEST_MODE = "OSS4X_TEST_MODE"


def mark_test_mode():
    os.environ[_ENV_TEST_MODE] = "1"


def initialise_error_logging():
    if os.environ.get(_ENV_TEST_MODE):
        log_info("Skipping error logging initialisation in test mode")
        return
    from oss4x.app.src import config

    sentry_dsn = config.SETTINGS.SENTRY_DSN_URL
    if sentry_dsn and len(sentry_dsn) > 1:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.starlette import StarletteIntegration

        sentry_sdk.init(
            sentry_dsn,
            traces_sample_rate=0,
            integrations=[
                StarletteIntegration(
                    transaction_style="endpoint",
                    failed_request_status_codes={403, *range(500, 599)},
                    http_methods_to_capture=("GET", "POST"),
                ),
                FastApiIntegration(
                    transaction_style="endpoint",
                    failed_request_status_codes={403, *range(500, 599)},
                    http_methods_to_capture=("GET", "POST"),
                ),
            ],
        )
        log_info("Initialised error logging in Sentry")
    else:
        log_info("Skipping error logging in Sentry")


def create_app(app_config: AppConfig, settings: Settings | None = None) -> FastAPI:
    """
    Create and configure a FastAPI application for a specific deployment.

    :param app_config: The application configuration for this deployment
    :param settings: Infrastructure settings (defaults to the module-level Settings instance)
    :return: Configured FastAPI application
    """
    load_dotenv(override=True)

    if settings is None:
        settings = _DEFAULT_SETTINGS

    set_current_config(app_config, settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Initialising error logging at app start
        initialise_error_logging()

        # Ensure that context data is available
        download_listing_data_for_app(force_refresh=False)

        log_info("Starting app")
        if True:
            ui.repository_index_characteristics_from_documents()
        log_info(" -- All metrics loaded")
        yield
        log_info("Exiting app")

    if app_config.APP_PROXY_PATH is not None:
        kwargs = dict(root_path=app_config.APP_PROXY_PATH)
    else:
        kwargs = dict()

    app = FastAPI(
        title="OSS4x",
        description="""
A search engine for open-source code for any applications
""",
        version=version("oss4x"),
        lifespan=lifespan,
        openapi_url=None,
        redoc_url=None,
        **kwargs,
    )

    # Store config on app.state for route handlers
    app.state.app_config = app_config
    app.state.settings = settings

    def get_top_urls(scores_dict: dict, n: int):
        sorted_urls = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
        top_n_urls = sorted_urls[:n]
        top_n_dict = dict(top_n_urls)
        return top_n_dict

    @app.get("/")
    async def base_landing(request: Request, channel: str | None = None):
        log_landing(request=request, channel=channel)
        return RedirectResponse("ui/search")

    @app.head("/", include_in_schema=False, status_code=204)
    def _head_base(request: Request):
        pass

    @app.get("/favicon.ico")
    def _favicon():
        url = app_config.APP_URL_FAVICON
        if url:
            return RedirectResponse(url)
        else:
            return JSONResponse(content={"favicon": "not defined"}, status_code=404)

    # ----------------------------------------------------------------------------------
    # For SEO of the app
    # ----------------------------------------------------------------------------------

    @app.get("/sitemap.xml")
    def _sitemap_xml(request: Request):
        content = dict(
            BASE_URL=app_config.full_url_base,
            UPDATE_FREQUENCY="weekly",
            UI_ENDPOINTS=["ui/search", "ui/about", "ui/results"],
            LAST_UPDATE=str(datetime.now().date()),
        )
        return render_template(
            request,
            template_file="sitemap.xml",
            content=content,
        )

    @app.get("/robots.txt")
    def _robots_txt(request: Request):
        content = dict(
            BASE_URL=app_config.full_url_base,
        )
        return render_template(
            request,
            template_file="robots.txt",
            content=content,
        )

    # Adding routes
    app.mount("/api", api.app)
    app.mount("/ui", ui.app)
    app.mount("/static", StaticFiles(directory=str(STATIC_FILES_PATH)), name="static")

    # Adding MCP
    app.mount("/mcp", app=mcp_server.mcp.http_app(transport="sse"))

    return app


# Convenience exposure
__all__ = [
    "FILE_OUTPUT_LISTING_FEATHER",
    "Theme",
    "ThemeColors",
    "ThemeShadows",
    "ThemeSpacing",
    "ThemeTransitions",
    "ThemeTypography",
    "create_app",
    "mark_test_mode",
    "mcp",
]
