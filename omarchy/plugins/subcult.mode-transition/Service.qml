import QtQuick
import Quickshell
import Quickshell.Hyprland
import Quickshell.Io
import Quickshell.Wayland
import "../subcult.motion" as Motion

Item {
  id: root
  property var shell: null
  property bool opened: false
  property string modeName: "SUBCULT"
  property string phase: "ACTIVE"
  property string detail: "OPERATING PARAMETERS SYNCHRONIZED"
  property color accent: "#00ff88"
  property int eventCount: 0
  property var contextSurface: ({active:false,status:"baseline"})
  Motion.MotionState { id: motion }
  readonly property var targetScreen: {
    var focused=Hyprland.focusedMonitor, screens=Quickshell.screens||[]
    if(focused) for(var i=0;i<screens.length;i++) if(screens[i].name===focused.name) return screens[i]
    return screens.length?screens[0]:null
  }

  function copy(name) {
    var events={"workspace-kit":["WORKSPACE KIT","TOOLS READY","#62d8ff"],"desktop-recipe":["DESKTOP RECIPE","SETTINGS APPLIED","#a78bfa"],"mission":["MISSION","FOCUS CYCLES COMPLETED","#00ff88"],"session":["LOCAL SESSION","JOURNAL SUMMARY","#f0ece4"]}
    if(events[name]) return events[name]
    var values={"presentation":["SUBCULT PRESENTATION","VISUAL TELEMETRY CHANNEL","#62d8ff"],"deployment":["SUBCULT DEPLOYMENT","MISSION WORKSPACE","#f6a52f"],"closed-door":["CLOSED DOOR","COMMUNICATION BARRIER","#ffd166"],"intrusion":["INTRUSION DRILL","CONDITION ONE SIMULATION","#ff4055"],"docked":["DOCK LINK","EXTERNAL OPERATIONS PROFILE","#62d8ff"],"mobile":["MOBILE OPERATIONS","INTERNAL SYSTEM PROFILE","#00ff88"],"terminal-context":["TERMINAL CONTEXT","ISOLATED PROFILE","#a78bfa"]}
    return values[name]||[String(name||"SUBCULT").toUpperCase(),"OPERATING MODE","#00ff88"]
  }
  function show(name,nextPhase,nextDetail) {
    var words=copy(name)
    modeName=words[0]; phase=String(nextPhase||"active").toUpperCase()
    detail=String(nextDetail||words[1]).toUpperCase().slice(0,64); accent=contextAccent(words[2])
    opened=true; eventCount++; retire.restart()
  }
  function contextAccent(fallback) {
    if (!contextSurface.active) return fallback
    var colors={critical:"#ff4055",constrained:"#f6d447",offline:"#f6d447",docked:"#62d8ff",mobile:"#00ff88","media-active":"#a78bfa"}
    return colors[contextSurface.status]||fallback
  }
  function refreshContext() { if (!contextProbe.running) contextProbe.running=true }
  FileView { path:Quickshell.env("HOME")+"/.local/state/subcult-rice/context/state.json"; watchChanges:true; printErrors:false; onFileChanged:root.refreshContext() }
  Process { id:contextProbe; running:true; command:["subcult-context","surface","--json","--compact"]; stdout:StdioCollector { onStreamFinished:{ try { root.contextSurface=JSON.parse(text) } catch(error) { root.contextSurface={active:false,status:"baseline"} } } } }
  function hide() { opened=false; retire.stop() }
  Timer { id: retire; interval: motion.full?1800:(motion.reduced?1400:1100); onTriggered:root.opened=false }
  IpcHandler {
    target:"mode-transition"
    function show(name:string,phase:string,detail:string):string { root.show(name,phase,detail); return root.modeName+" // "+root.phase }
    function hide():string { root.hide(); return "hidden" }
    function state():string { return JSON.stringify({visible:root.opened,mode:root.modeName,phase:root.phase,detail:root.detail,motionMode:motion.mode,eventCount:root.eventCount}) }
  }
  PanelWindow {
    visible:root.opened; screen:root.targetScreen
    anchors{top:true;right:true;bottom:true;left:true}
    color:"transparent"; exclusionMode:ExclusionMode.Ignore; mask:Region{}
    WlrLayershell.namespace:"subcult-mode-transition"; WlrLayershell.layer:WlrLayer.Overlay; WlrLayershell.keyboardFocus:WlrKeyboardFocus.None
    Rectangle {
      id:card; width:Math.min(440,parent.width-32); height:104
      anchors.left:parent.left; anchors.leftMargin:Math.min(Math.max(16,parent.width*0.045),(parent.width-width)/2)
      anchors.bottom:parent.bottom; anchors.bottomMargin:Math.max(20,parent.height*0.07)
      color:"#ed080710"; radius:3; border.width:2; border.color:root.accent
      opacity:root.opened?1:0
      transform:Translate{x:root.opened||!motion.full?0:-10}
      Behavior on opacity{enabled:!motion.off;NumberAnimation{duration:motion.standardMs}}
      Rectangle {
        width: 8
        anchors { top: parent.top; bottom: parent.bottom; left: parent.left }
        color: root.accent
      }
      Column {
        anchors {
          left: parent.left
          right: parent.right
          verticalCenter: parent.verticalCenter
          leftMargin: 30
          rightMargin: 20
        }
        spacing: 7
        Text{width:parent.width;text:root.modeName+" // "+root.phase;color:root.accent;elide:Text.ElideRight;font.family:"JetBrainsMono Nerd Font";font.pixelSize:18;font.bold:true;font.letterSpacing:1}
        Rectangle{width:parent.width;height:1;color:"#7c5ce0"}
        Text{width:parent.width;text:root.detail;color:"#f0ece4";elide:Text.ElideRight;font.family:"JetBrainsMono Nerd Font";font.pixelSize:11;font.bold:true;font.letterSpacing:.6}
      }
    }
  }
}
