import QtQuick
import Quickshell
import Quickshell.Io
import Quickshell.Hyprland
import "AdaptivePolicy.js" as Policy

Item {
  id: root
  property string widget: ""
  property bool activity: false
  property var policy: ({enabled:false})
  readonly property int workspace: Hyprland.focusedWorkspace ? Hyprland.focusedWorkspace.id : 0
  readonly property var decision: Policy.decision(policy,widget,workspace,activity)
  readonly property bool shown: decision.shown
  function accept(raw) { try { var value=JSON.parse(String(raw)); root.policy=value.schema_version===1?value:({enabled:false}) } catch(error) { root.policy=({enabled:false}) } }
  FileView {
    path:Quickshell.env("HOME")+"/.config/omarchy/adaptive-bar.json"
    watchChanges:true; printErrors:false
    onLoaded:root.accept(text())
    onFileChanged:reload()
    onLoadFailed:root.accept("{}")
  }
}
