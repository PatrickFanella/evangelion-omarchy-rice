# Release media

Presentation assets for the project README and releases. Their SHA-256 digests
are recorded in `release-media.sha256`, and validation rejects any unreviewed
replacement.

| File | Source |
|---|---|
| `wallpaper-gallery.png` | Contact sheet of the seven wallpapers in `theme/backgrounds/`, built with `magick montage ... -strip` |
| `context-states.png` | Deterministic `rsvg-convert` export of `context-states.svg`; four fictional context states and no live telemetry |
| `context-states.svg` | Reviewable vector source for the context-state comparison; project-authored shapes and text only |
| `readme-hero.{svg,png}` | SUBCULT title and feature-count banner; editable vector source and metadata-stripped raster |
| `readme-features.{svg,png}` | Four feature groups with repository-defined shortcuts; illustrative diagrams, not captured UI |
| `readme-workspaces.{svg,png}` | Shipped ten-workspace directory and wraparound controls; numbers illustrate the directory while the bar defaults to icons |

All PNGs are generated rather than captured, and contain only image data
chunks: no profile, comment, timestamp, path, hostname, account, or device
metadata.

## Rebuild the README illustrations

```bash
python3 scripts/build-readme-media
```

The renderer writes all three editable SVGs and their PNG exports. It uses
the bundled Oswald, Space Grotesk, and JetBrains Mono fonts through a private
fontconfig file, then strips PNG metadata with ImageMagick. It installs no
fonts and reads no live desktop state. Edit the script to preserve changes
across rebuilds, or edit an SVG directly for a one-off layout revision.

The diagrams use public repository defaults, not a particular laptop's scale,
temperature thresholds, accounts, or third-party bar setup. Thermal dwell
times are described without substituting machine-specific threshold values.
The start page is explicitly identified as optional. No generated-image
service was used for these assets. Brand/font terms remain documented in
[`../ASSETS_LICENSE.md`](../ASSETS_LICENSE.md).

After rebuilding, inspect every frame and update the SVG and PNG checksums
in `release-media.sha256` together.

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
