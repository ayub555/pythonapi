import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.logging_config import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        client_host = request.client.host if request.client else "unknown"

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.exception(
                "method=%s path=%s client=%s status=500 duration_ms=%.2f unhandled_exception",
                request.method,
                request.url.path,
                client_host,
                duration_ms,
            )
            raise

        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "method=%s path=%s client=%s status=%d duration_ms=%.2f",
            request.method,
            request.url.path,
            client_host,
            response.status_code,
            duration_ms,
        )
        return response
