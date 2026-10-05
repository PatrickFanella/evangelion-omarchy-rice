#!/usr/bin/env python3
"""Static contract tests for shell notification and OSD motion policy."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ROOT / "omarchy/plugins"


def read(plugin, relative="Service.qml"):
    return (PLUGINS / plugin / relative).read_text()


def main():
    shared = read("subcult.motion", "MotionState.qml")
    for mode in ('mode === "full"', 'mode === "reduced"', 'mode === "off"'):
        assert mode in shared
    assert "standardMs" in shared and "criticalMs: 0" in shared

    participants = (
        "subcult.workspace-osd",
        "subcult.device-osd",
        "subcult.power-sequence",
        "subcult.intrusion",
        "subcult.update-operation",
        "subcult.notifications",
    )
    for plugin in participants:
        source = read(plugin)
        assert 'import "../subcult.motion" as Motion' in source, plugin
        assert "Motion.MotionState" in source, plugin
        assert "subcult-screensaver.json" not in source, plugin

    notifications = read("subcult.notifications")
    card = read("subcult.notifications", "components/NotificationCard.qml")
    assert "popupAnimated: true" in notifications
    assert 'urgency === 2 || motionMode === "off"' in card
    assert 'motionMode === "reduced" ? 80 : 140' in card
    assert "onSummaryChanged: cardSlot.remainingLifetime = 1.0" in notifications
    assert "function invokeLast()" in notifications

    intrusion = read("subcult.intrusion")
    assert "Behavior on width" not in intrusion
    assert "motion.full ? 3200 : 3600" in intrusion

    for plugin in participants[:3]:
        source = read(plugin)
        assert "targetScreen" in source and "Hyprland.focusedMonitor" in source

    print("PASS  unified shell motion policy")


if __name__ == "__main__":
    main()
