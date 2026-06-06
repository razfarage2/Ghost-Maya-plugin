import maya.cmds as cmds

class ProxySourceResolver:
    @staticmethod
    def resolve(original_root: str, proxy_root: str, source_mode: str) -> str:
        """
        Returns the root path to scan based on source_mode.
        If source_mode="proxy" but proxy_root does not exist, we fall back to "original".
        """
        if source_mode == "proxy":
            if proxy_root and cmds.objExists(proxy_root):
                return proxy_root
            # Fall back to original if proxy missing
            return original_root
            
        return original_root