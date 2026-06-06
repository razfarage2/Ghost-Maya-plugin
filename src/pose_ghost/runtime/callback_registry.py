from typing import Callable, Dict, Any

class CallbackRegistry:
    def __init__(self):
        self._callbacks: Dict[Any, Callable] = {}

    def register(self, callback_id: Any, remover: Callable):
        self._callbacks[callback_id] = remover

    def clear(self):
        for cb_id, remover in self._callbacks.items():
            remover(cb_id)
        self._callbacks.clear()