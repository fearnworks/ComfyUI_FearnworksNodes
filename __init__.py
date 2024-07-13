import os
from .node_mappings import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

DEBUG_MODE = os.getenv("DEBUG_MODE", False)
# Add logging to confirm nodes are loaded
print("\033[34mFearnworks Custom Nodes: \033[92mLoading...\033[0m")

if DEBUG_MODE:
    for node_name, node_class in NODE_CLASS_MAPPINGS.items():
        print(f"\033[34m  - Loaded: \033[92m{node_name}\033[0m")

print("\033[34m FEARNWORKS CUSTOM NODES: \033[92mAll nodes loaded successfully\033[0m")
