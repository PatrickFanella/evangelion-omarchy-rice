# Release media

Presentation assets for the project README and releases. Their SHA-256 digests
are recorded in `release-media.sha256`, and validation rejects any unreviewed
replacement.

| File | Source |
|---|---|
| `wallpaper-gallery.png` | Contact sheet of the seven wallpapers in `theme/backgrounds/`, built with `magick montage ... -strip` |
| `context-states.png` | Deterministic `rsvg-convert` export of `context-states.svg`; four fictional context states and no live telemetry |
| `context-states.svg` | Reviewable vector source for the context-state comparison; project-authored shapes and text only |

Both PNGs are generated rather than captured, and contain only image data
chunks: no profile, comment, timestamp, path, hostname, account, or device
metadata.

The 1.x desktop, start-page, session-menu, lock-screen, and motion captures
showed the retired Evangelion interface and were removed in 2.0. Replacement
captures of the SUBCULT desktop have not been taken yet.

Before adding or replacing a release image, inspect the complete frame, strip
metadata, update `release-media.sha256`, and record here why the source is safe
to publish. Captures from a live desktop must not show browser activity, media
recommendations, machine details, account identity, local paths, window titles,
or conversation text.

To capture the start page without exposing live telemetry, visit:

```text
http://127.0.0.1:8765/?demo=1
```
