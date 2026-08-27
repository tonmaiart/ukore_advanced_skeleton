from __future__ import annotations

import sys
from pathlib import Path

_PLUGIN_DIR = Path(__file__).resolve().parent
if str(_PLUGIN_DIR) not in sys.path:
    sys.path.insert(0, str(_PLUGIN_DIR))

TOOL_ID = "advanced_skeleton"
TOOL_LABEL = "AdvancedSkeleton"
# Convention-only string match with plugins/repo_internal/maya_launcher/plugin.py
# — both resolve to the same active Project's plugin_data via
# ProjectPluginConfigStore, no coupling API needed. See that plugin's README
# for the full "contributions"/"labels" shape this writes into.
MAYA_ENV_BRIDGE_PLUGIN_ID = "maya_launcher_env_bridge"
ANY_VERSION = "*"


def register(api) -> None:
    tool_root = Path(__file__).resolve().parent

    bridge = api.project_plugin_config_store(MAYA_ENV_BRIDGE_PLUGIN_ID)
    if bridge is None:
        return

    contributions = bridge.get("contributions", {})
    contributions[TOOL_ID] = {
        "PYTHONPATH": {ANY_VERSION: [str(tool_root / "maya-scripts")]},
        "ADVANCEDSKELETON_ROOT": {
            ANY_VERSION: [str(tool_root / "maya-scripts" / "AdvancedSkeleton")]
        },
    }
    bridge.set("contributions", contributions)

    labels = bridge.get("labels", {})
    labels[TOOL_ID] = TOOL_LABEL
    bridge.set("labels", labels)

    # order ต้องน้อยกว่า UkoreMenu เอง (order 99) เพื่อให้ import
    # (และ register_item ของ UkoreAdvancedSkeleton) รันเสร็จก่อน UkoreMenu
    # สั่ง rebuild_menu — เดิมเมนู "Rig" ของเครื่องมือนี้ถูก MayaToolkit เป็นคน
    # register แทน ย้ายมาให้ปลั๊กอินนี้ประกาศ launch_hooks ของตัวเองแทน (ตาม
    # ข้อกำหนดใน ukore_menu's README) เพื่อให้ AdvancedSkeleton เป็นเจ้าของ
    # เมนูของตัวเองแบบเดียวกับ ShotSplitter/UkoreReferenceEditor
    hooks = bridge.get("launch_hooks", {})
    hooks[TOOL_ID] = {
        "order": 20,
        "post_open_mel": 'python("try:\\n    import UkoreAdvancedSkeleton\\nexcept ImportError:\\n    pass");',
    }
    bridge.set("launch_hooks", hooks)
