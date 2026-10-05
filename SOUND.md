# SUBCULT sound policy

SUBCULT sound is opt-in and synthesized locally. The shipped policy is globally
disabled, every category starts disabled, and lock/login cues therefore remain
silent until the operator explicitly enables both the global channel and the
relevant category. Visual notifications and overlays continue regardless of
audio state.

The preserved `~/.config/omarchy/sound.json` policy provides `session`
(lock/unlock), `system` (power), `workflow` (completion), and `critical`
(alerts). Each has a 0–100% stream-volume ceiling. Quiet hours default to
22:00–07:00 and suppress every non-preview cue.

```bash
subcult-sound status --json
subcult-sound enable                    # global authority only
subcult-sound category critical enable
subcult-sound volume critical 20
subcult-sound quiet-hours 22 7
subcult-sound quiet-hours off
subcult-sound preview critical          # explicit preview bypasses policy
subcult-sound kill                      # immediate persistent global silence
```

Precedence is global kill switch → category/scene permission → quiet hours →
provider availability → cue rate limit. The active affinity scene can override a
category without changing its baseline preference:

```bash
subcult-sound scene ink workflow enabled
subcult-sound scene ink workflow inherit
```

Scene overrides never bypass the global switch or quiet hours. Missing PipeWire
support is silent and non-blocking. `preview` is the only policy-bypassing path;
it is always an explicit user action and still observes the category ceiling.
