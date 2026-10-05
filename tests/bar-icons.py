#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
plugins = root / "omarchy/plugins"
shell = json.loads((root / "omarchy/shell.json").read_text())
frame = (plugins / "subcult.icon-theme/UpstreamIconFrame.qml").read_text()
docs = (root / "BAR_ICONS.md").read_text()
bar_theme = (root / "theme/shell.bar.toml").read_text()

adapters = {
    "subcult.agents": ("omarchy.agents", "/shell/plugins/agents/Panel.qml"),
    "subcult.bluetooth": ("omarchy.bluetooth", "/shell/plugins/panels/bluetooth/Panel.qml"),
    "subcult.dropbox": ("omarchy.dropbox", "/shell/plugins/panels/dropbox/Panel.qml"),
    "subcult.tailscale": ("omarchy.tailscale", "/shell/plugins/panels/tailscale/Panel.qml"),
}

right = [entry["id"] for entry in shell["bar"]["layout"]["right"]]
assert "omarchy.tray" in right
assert all(adapter in right for adapter in adapters)
assert all(native not in right for native, _ in adapters.values())
assert any(item["id"] == "subcult.icon-theme" for item in shell["plugins"])

for adapter, (native, source_path) in adapters.items():
    directory = plugins / adapter
    manifest = json.loads((directory / "manifest.json").read_text())
    source = (directory / "BarWidget.qml").read_text()
    assert manifest["id"] == adapter
    assert 'import "../subcult.icon-theme" as Subcult' in source
    assert f'upstreamModule: "{native}"' in source
    assert f'upstreamSource: "{source_path}"' in source
    assert adapter in docs and native in docs

for contract in (
    'Quickshell.env("OMARCHY_PATH")',
    'nativeItem.bar = root.bar',
    'nativeItem.settings = root.settings',
    'nativeItem.moduleName = root.upstreamModule',
    'typeof nativeItem.open === "function"',
    'typeof nativeItem.close === "function"',
    'typeof nativeItem.toggle === "function"',
    'implicitWidth: Math.max',
):
    assert contract in frame, contract

for forbidden_chrome in ("Rectangle {", "HoverHandler", "border.color", "stateColor"):
    assert forbidden_chrome not in frame, forbidden_chrome

assert 'text             = "#B79ACB"' in bar_theme
affinity = (root / "bin/subcult-affinity").read_text()
assert 'text = "#$bar_icon"' in affinity
variant_registry = json.loads((root / "omarchy/theme-variants.json").read_text())
assert {row["bar_icon"] for row in variant_registry["affinities"].values()} == {
    "A995B8", "D8B84E", "79BFE3", "B79ACB", "D77A64"
}
assert '"bar_icon"' in affinity and "subcult-theme-variant" in affinity

for forbidden in ("/home/", "so1omon", "Screen.name"):
    assert forbidden not in frame

assert "full-color" in docs
assert "Symbolic icons" in docs
assert "#B79ACB" in docs
assert "no per-widget frames" in docs
assert "Acid Block" in docs and "Ink" in docs
assert "fallback" in docs.lower()

print("bar icon unification contracts passed")
