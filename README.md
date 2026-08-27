# cache/plugins/ukore_advanced_skeleton/

AdvancedSkeleton — a vendored Maya rigging toolset, unchanged internal
layout from the original `add-on/AdvancedSkeleton/` (moved to
`plugins/studio/maya_launcher/AdvancedSkeleton/` during the 2026-07-14
consolidation, then split back out to its own top-level plugin on
2026-07-19, then re-cloned as this standalone `cache/plugins/` repo
plugin). Has no UI of its own inside UkoreHub itself (nothing shows up as
a UkoreHub sidebar tab) — it only contributes env vars/menu wiring for
Maya.

`plugin.py`'s `register(api)` writes a `PYTHONPATH` contribution (pointing
at this folder's `maya-scripts/`) plus an `ADVANCEDSKELETON_ROOT`
contribution (pointing at `maya-scripts/AdvancedSkeleton/`, the folder
containing `AdvancedSkeleton.mel`) into `maya_launcher`'s shared
`maya_launcher_env_bridge` `ProjectPluginConfigStore`, read and merged by
that plugin's `open_maya_file` when it actually launches Maya. No direct
import relationship with `maya_launcher` — just the shared
`PluginConfigStore` id convention (see that plugin's README for the full
bridge shape).
`RepoToolsStore` (owned by `maya_launcher`) is what lets a studio admin
disable this tool per-repo; this plugin always contributes unconditionally.

`ADVANCEDSKELETON_ROOT` is a single-directory value, not a search-path
list like `PYTHONPATH` — `maya_launcher`'s merge still works for it
unchanged since the prepend-onto-existing logic degrades to "just set it"
when nothing else in the base env already defines that var name.
`maya-scripts/UkoreAdvancedSkeleton/__init__.py`'s `run_advanced()`/
`run_advanced_face()` read this env var at call time (via
`os.environ.get("ADVANCEDSKELETON_ROOT")`) to `mel.eval(source ...)` this
plugin's vendored `.mel` files — so a Maya session launched through
UkoreHub's Maya Launcher always has it, no per-machine env var to set by
hand.

## Ukore Tools menu (Rig category) — 2026-08-27

This plugin registers its own "Advanced Skeleton"/"Advanced Skeleton
Face" items into `ukore_menu`'s central "Ukore Tools" menu (Rig > External
Tools submenu) directly, instead of going through `MayaToolkit` — same
pattern as `ShotSplitter`/`UkoreReferenceEditor` (see
`ukore_menu/README.md`'s "ข้อกำหนดบังคับ" section for why the
`launch_hooks` entry below is required, not optional):

- `plugin.py`'s `register(api)` writes a `launch_hooks[TOOL_ID]` entry
  (`order: 20`, `post_open_mel: import UkoreAdvancedSkeleton`) into the
  same `maya_launcher_env_bridge` store — this is what makes
  `maya-scripts/UkoreAdvancedSkeleton/__init__.py`'s module-level
  `registry.register_item()`/`register_reload_handler()` calls actually
  run every Maya session (not just after the user opens the tool once).
  `order` must stay below 99 (`ukore_menu`'s own `rebuild_menu` trigger).
- `UkoreAdvancedSkeleton/__init__.py` owns `run_advanced()`/
  `run_advanced_face()` (moved from `MayaToolkit/maya-scripts/UkoreMaya/
  core/function.py` on 2026-08-27 — see `MayaToolkit/README.md`'s
  changelog entry for that date) and registers both as `MenuItemSpec`s
  with `category="Rig"`, `sub_menu="External Tools"` — same ids
  (`advanced_skeleton`/`advanced_skeleton_face`) and `order` (60/61) as
  before, so the menu position is unchanged for users.

Two bugs in `plugin.py` were fixed in the same change (found while
verifying this menu registration): `tool_root` was computed from
`api.app_root / "plugins" / "studio" / "AdvancedSkeleton"` — a path that
stopped existing once this plugin became its own `cache/plugins/` clone —
instead of `Path(__file__).resolve().parent`; and the bridge was fetched
via `api.plugin_config_store(..., shared=True)` (the studio-wide,
cloud-synced store) instead of `api.project_plugin_config_store(...)` (the
per-project store `maya_launcher`/`MayaToolkit`/`ukore_menu` actually
read from) — so this plugin's `PYTHONPATH`/`ADVANCEDSKELETON_ROOT`
contribution was silently never seen by Maya Launcher at all.
