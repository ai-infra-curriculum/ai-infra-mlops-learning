"""
API module for model serving platform

Provides FastAPI-based REST API for model inference and management.
"""

from .server import app, create_app

__all__ = ["app", "create_app"]
