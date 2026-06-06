from .update_queue import UpdateQueue
from .callback_registry import CallbackRegistry
from .controller import Controller
from .lifecycle import Lifecycle

class CompositionRoot:
    """
    Central assembly point for all dependencies.
    """
    def __init__(self):
        self.queue = UpdateQueue()
        self.registry = CallbackRegistry()
        self.controller = Controller(self.queue)
        
        # In the future, pass the real renderer here
        self.lifecycle = Lifecycle(self.registry, self.queue, renderer_seam=None)