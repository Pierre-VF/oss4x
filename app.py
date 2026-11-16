"""
FastAPI app to operate a search
"""

from uvicorn import run

from oss4x.app import AppConfig, create_app

app = create_app(AppConfig())

if __name__ == "__main__":
    # For local testing
    from oss4x.app import mark_test_mode

    mark_test_mode()
    run(app, host="127.0.0.1", port=8080)
