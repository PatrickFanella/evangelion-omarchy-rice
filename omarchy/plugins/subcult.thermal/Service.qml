import QtQuick
import Quickshell.Io

Item {
  property var shell: null
  Process { running: true; command: ["subcult-thermal-alert", "monitor"] }
}
