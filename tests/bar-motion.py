#!/usr/bin/env python3
"""Contracts for quiet, stateful SUBCULT bar microinteractions."""
import json, re, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=Path(sys.argv[1]) if len(sys.argv)>1 else root/"test-results/bar-motion.json"
motion=root/"omarchy/plugins/subcult.motion"
cue=(motion/"StateCue.qml").read_text()
widgets={name:(root/path).read_text() for name,path in {
 "workspace":"omarchy/plugins/subcult.workspaces/Workspaces.qml",
 "media":"omarchy/plugins/subcult.media/BarWidget.qml",
 "mission":"omarchy/plugins/subcult.mission/BarWidget.qml",
 "privacy":"omarchy/plugins/subcult.privacy/BarWidget.qml",
 "health":"omarchy/plugins/subcult.health/BarWidget.qml",
 "cava":"omarchy/plugins/subcult.cava/BarWidget.qml",
 "communications":"omarchy/plugins/subcult.communications/BarWidget.qml",
 "power":"omarchy/plugins/subcult.power/Panel.qml",
 "closed-door":"omarchy/plugins/subcult.closed-door/BarWidget.qml",
 "context":"omarchy/plugins/subcult.context/BarWidget.qml",
}.items()}
checks={
 "shared_fixed_geometry":'width: cueWidth' in cue and 'Behavior on opacity' in cue,
 "full_reduced_off":all(x in cue for x in ('motion.reduced','motion.off','140')),
 "no_repeating_or_travel":'loops:' not in cue and not re.search(r'Behavior on (?:x|y|scale|width|height)',cue),
 "all_required_widgets":all('Motion.StateCue' in source for source in widgets.values()),
 "workspace_selection":'active: focused' in widgets['workspace'],
 "media_state":'player.isPlaying' in widgets['media'],
 "mission_state":'active: root.active' in widgets['mission'],
 "privacy_immediate":'critical: true' in widgets['privacy'],
 "health_immediate":'level === "critical" || root.status.level === "warning"' in widgets['health'],
 "communications_offline_immediate":'critical: root.status.link === "offline"' in widgets['communications'],
 "battery_immediate":'critical: root.reservePower || root.internalPower' in widgets['power'],
 "cava_optional":'active: root.shouldRun' in widgets['cava'] and 'running: root.shouldRun' in widgets['cava'],
 "affinity_has_no_width":'cueWidth: 2' in widgets['workspace'] and 'cueColor: Color.accent' in widgets['workspace'],
 "no_layout_animation":all(not re.search(r'Behavior on (?:implicitWidth|implicitHeight|text)',s) for s in widgets.values()),
 "bounded_labels":'ElideRight' in widgets['media'] and 'root.bar.width >= 1600' in widgets['mission'] and 'root.bar.width >= 1600' in widgets['communications'],
 "qml_group_syntax_guard":all('};color:' not in s and '};spacing:' not in s for s in [cue,*widgets.values()]),
}
failed=[k for k,v in checks.items() if not v]
if failed: raise AssertionError(', '.join(failed))
report={"schema_version":1,"suite":"bar-motion","status":"passed","checks":checks,"widgets":list(widgets)}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+"\n");print(json.dumps(report))
