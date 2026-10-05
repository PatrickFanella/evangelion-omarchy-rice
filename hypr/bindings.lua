-- Keep only personal keybinding overrides here.

-- Preserve Omarchy's stock capture keys while adding SUBCULT telemetry.
hl.unbind("PRINT")
hl.unbind("ALT + PRINT")
o.bind("PRINT", "Screenshot with SUBCULT confirmation", "subcult-capture screenshot")
o.bind("ALT + PRINT", "Screenrecording with SUBCULT telemetry", "subcult-capture recording --stop-recording || omarchy-menu toggle trigger.capture.screenrecord")

-- Use Right Ctrl as the dictation push-to-talk key instead of F9.
hl.unbind("F9")
hl.unbind("code:105")
hl.unbind("CTRL + Control_R")
o.bind("code:105", "Start dictation (push-to-talk)", "voxtype record start")
o.bind("CTRL + Control_R", "Stop dictation (push-to-talk)", "voxtype record stop", { release = true })

-- Assemble or dismiss the showcase on workspace 05.
o.bind("SUPER + SHIFT + F12", "Toggle SUBCULT presentation", "subcult-presentation")

-- Engage or release the distraction-free Closed Door focus envelope.
o.bind("SUPER + ALT + A", "Toggle Closed Door focus mode", "subcult-focus toggle")
o.bind("SUPER + ALT + V", "Inspect SUBCULT privacy activity", "omarchy-shell subcult-privacy toggle")
o.bind("SUPER + ALT + T", "Open SUBCULT mission timer", "omarchy-shell subcult-mission toggle")
o.bind("SUPER + ALT + H", "Open SUBCULT system health", "omarchy-shell subcult-health toggle")
o.bind("SUPER + ALT + C", "Open SUBCULT world clock", "omarchy-shell subcult-clock toggle")
o.bind("SUPER + CTRL + ALT + G", "Open SUBCULT context inspector", "omarchy-shell subcult-context-inspector toggle")
o.bind("SUPER + CTRL + ALT + F", "Toggle SUBCULT developer performance overlay", "subcult-performance toggle")
o.bind("SUPER + CTRL + ALT + S", "Open SUBCULT control center", "omarchy-shell subcult-settings toggle")

-- Open the unified SUBCULT command interface. SUPER + SPACE remains Omarchy's
-- standard root menu, so both launch paths stay available.
o.bind("SUPER + M", "SUBCULT command interface", "omarchy-menu toggle subcult")
o.bind("SUPER + CTRL + ALT + M", "Global SUBCULT command palette", "omarchy-shell subcult-command-palette toggle")
o.bind("SUPER + CTRL + ALT + O", "Search SUBCULT operations log", "omarchy-shell subcult-operations-log toggle")

-- Recovery remains CLI/TTY-first; this chord is the convenient live path.
o.bind("SUPER + ALT + R", "Toggle static SUBCULT recovery", "subcult-recovery toggle")

-- Preserve Omarchy's system/power menu keys while adding a restrained cue.
hl.unbind("SUPER + ESCAPE")
hl.unbind("XF86PowerOff")
o.bind("SUPER + ESCAPE", "SUBCULT session control", "setsid -f subcult-sound power; omarchy-menu toggle system")
o.bind("XF86PowerOff", "SUBCULT session control", "setsid -f subcult-sound power; omarchy-menu toggle system", { locked = true })

-- Secondary media controls; the laptop's standard XF86 media keys remain
-- available through Omarchy's built-in bindings.
o.bind("SUPER + ALT + P", "Media play/pause", "subcult-media play-pause", { locked = true })
o.bind("SUPER + ALT + N", "Media next track", "subcult-media next", { locked = true })
o.bind("SUPER + ALT + B", "Media previous track", "subcult-media previous", { locked = true })
o.bind("SUPER + ALT + X", "Media stop", "subcult-media stop", { locked = true })

-- Assemble or recover the deterministic SUBCULT development mission on workspace 04.
o.bind("SUPER + ALT + D", "Toggle SUBCULT deployment workspace", "subcult-deployment toggle")

-- This simulation is manual-only; the same chord is always the safe exit.
o.bind("SUPER + ALT + I", "Toggle Intrusion drill simulation", "subcult-intrusion toggle")

-- Inspect recent downloads through the classified intake before opening them.
o.bind("SUPER + ALT + L", "SUBCULT classified downloads", "omarchy-launch-terminal -- subcult-downloads open")
