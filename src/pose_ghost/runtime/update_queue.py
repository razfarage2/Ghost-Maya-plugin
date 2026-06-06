from typing import Any, Optional

class UpdateQueue:
    def __init__(self):
        self._requests = []

    def enqueue(self, request: Any):
        """
        Appends the request. If it's a heavy operation (rebuild, appearance, clear),
        removes previous heavy operations to prevent storms.
        """
        action = request.get("action")
        if action in ("rebuild", "appearance", "clear"):
            self._requests = [r for r in self._requests if r.get("action") not in ("rebuild", "appearance", "clear")]
        
        self._requests.append(request)

    def has_pending(self) -> bool:
        return len(self._requests) > 0

    def drain_all(self) -> list[Any]:
        reqs = self._requests[:]
        self._requests.clear()
        return reqs

    def drain_latest(self) -> Optional[Any]:
        # For backward compatibility during refactor, returns a 'multi' action or single action
        if not self._requests:
            return None
        reqs = self.drain_all()
        return {"action": "multi", "requests": reqs}

    def clear(self):
        self._requests.clear()