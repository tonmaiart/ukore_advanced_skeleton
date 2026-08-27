import os

import maya.cmds as cmds
import maya.mel as mel

from UkoreMenu import registry, MenuItemSpec, ReloadHandlerSpec, reload_package


def _advanced_skeleton_root():
    root = os.environ.get("ADVANCEDSKELETON_ROOT")
    if not root:
        cmds.warning(
            "ADVANCEDSKELETON_ROOT is not set. Set it to your AdvancedSkeleton "
            "folder (the one containing AdvancedSkeleton.mel) to use this tool."
        )
        return None
    return root


def run_advanced():
    root = _advanced_skeleton_root()
    if not root:
        return

    mel_file = os.path.join(root, "AdvancedSkeleton.mel").replace("\\", "/")
    if not os.path.exists(mel_file):
        cmds.warning(f"AdvancedSkeleton.mel not found: {mel_file}")
        return

    mel.eval(f'source "{mel_file}";')
    mel.eval("AdvancedSkeleton;")


def run_advanced_face():
    root = _advanced_skeleton_root()
    if not root:
        return

    mel_file = os.path.join(
        root, "AdvancedSkeletonFiles", "Selector", "face.mel"
    ).replace("\\", "/")
    if not os.path.exists(mel_file):
        cmds.warning(f"face.mel not found: {mel_file}")
        return

    mel.eval(f'source "{mel_file}";')


registry.register_item(
    MenuItemSpec(
        id="advanced_skeleton",
        label="Advanced Skeleton",
        category="Rig",
        sub_menu="External Tools",
        command="import UkoreAdvancedSkeleton; UkoreAdvancedSkeleton.run_advanced()",
        order=60,
    )
)
registry.register_item(
    MenuItemSpec(
        id="advanced_skeleton_face",
        label="Advanced Skeleton Face",
        category="Rig",
        sub_menu="External Tools",
        command="import UkoreAdvancedSkeleton; UkoreAdvancedSkeleton.run_advanced_face()",
        order=61,
    )
)

registry.register_reload_handler(
    ReloadHandlerSpec(
        id="advanced_skeleton",
        label="AdvancedSkeleton",
        callback=lambda: reload_package("UkoreAdvancedSkeleton"),
        order=20,
    )
)

__all__ = ["run_advanced", "run_advanced_face"]
