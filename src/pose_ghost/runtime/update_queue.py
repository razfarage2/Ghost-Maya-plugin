from typing import Any, Optional

class UpdateQueue:
    def __init__(self):
        self._pending_request: Optional[Any] = None

    def enqueue(self, request: Any):
        """
        Overwrites any pending request with the latest one.
        """
        self._pending_request = request

    def has_pending(self) -> bool:
        return self._pending_request is not None

    def drain_latest(self) -> Optional[Any]:
        req = self._pending_request
        self._pending_request = None
        return req

    def clear(self):
        self._pending_request = None