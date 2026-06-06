from .callback_registry import CallbackRegistry
from .update_queue import UpdateQueue

class Lifecycle:
    def __init__(self, registry: CallbackRegistry, queue: UpdateQueue, renderer_seam=None):
        self._registry = registry
        self._queue = queue
        self._renderer = renderer_seam

    def startup(self):
        # Initialization logic (e.g., register Maya callbacks via adapters) goes here
        pass

    def shutdown(self):
        # Clear Maya callbacks
        self._registry.clear()
        
        # Clear pending rebuilds
        self._queue.clear()
        
        # Cleanup renderer (clear ghosts)
        if self._renderer and hasattr(self._renderer, 'cleanup'):
            self._renderer.cleanup()