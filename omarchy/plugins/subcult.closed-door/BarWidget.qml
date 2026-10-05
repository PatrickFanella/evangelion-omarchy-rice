import QtQuick
import Quickshell
import Quickshell.Io
import qs.Ui
import qs.Commons
import "../subcult.motion" as Motion

BarWidget {
  id: root
  moduleName: "subcult.closed-door"
  property bool fieldActive: false

  visible: fieldActive
  implicitWidth: fieldActive ? row.implicitWidth + Style.space(14) : 0
  implicitHeight: barSize

  function refresh() {
    if (!probe.running) probe.running = true
  }

  Process {
    id: probe
    running: true
    command: ["bash", "-c", "[[ -f $HOME/.local/state/subcult-rice/closed-door/active ]] && echo active || echo inactive"]
    stdout: SplitParser { onRead: function(line) { root.fieldActive = String(line).trim() === "active" } }
  }

  FileView {
    path: Quickshell.env("HOME") + "/.local/state/subcult-rice/closed-door"
    watchChanges: true
    printErrors: false
    onFileChanged: root.refresh()
  }

  Row {
    id: row
    anchors.centerIn: parent
    spacing: Style.space(5)

    Text {
      anchors.verticalCenter: parent.verticalCenter
      text: "󰭟"
      color: "#F6A52F"
      font.family: root.bar.fontFamily
      font.pixelSize: Style.font.body
    }
    Text {
      anchors.verticalCenter: parent.verticalCenter
      text: "CLOSED DOOR // ACTIVE"
      color: "#FFD166"
      font.family: root.bar.fontFamily
      font.pixelSize: Style.font.caption
      font.bold: true
      font.letterSpacing: 0.5
      visible: !root.bar.vertical
    }
  }

  Motion.StateCue {
    anchors { left: parent.left; top: parent.top; bottom: parent.bottom }
    active: root.fieldActive
    cueColor: "#F6A52F"
  }

  MouseArea {
    anchors.fill: parent
    hoverEnabled: true
    cursorShape: Qt.PointingHandCursor
    onClicked: root.bar.run("subcult-focus off")
    onEntered: root.bar.showTooltip(root, "Release Closed Door and restore notifications")
    onExited: root.bar.hideTooltip(root)
  }
}
