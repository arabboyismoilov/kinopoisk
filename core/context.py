import contextvars


request_id = contextvars.ContextVar("requestId", default="no-id")