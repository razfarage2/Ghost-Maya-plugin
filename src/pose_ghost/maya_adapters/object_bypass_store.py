class ObjectBypassStore:
    def __init__(self):
        self._bypassed_ids = set()

    def mark_bypassed(self, target_id: str):
        self._bypassed_ids.add(target_id)

    def unmark_bypassed(self, target_id: str):
        self._bypassed_ids.discard(target_id)

    def is_bypassed(self, target_id: str) -> bool:
        return target_id in self._bypassed_ids

    def filter_targets(self, target_ids: list[str]) -> list[str]:
        return [tid for tid in target_ids if tid not in self._bypassed_ids]