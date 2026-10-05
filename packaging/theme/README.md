# SUBCULT for Omarchy

The SUBCULT poster-press theme for Omarchy. Ink canvases carry paper text,
with violet and acid green kept for marks, borders, and focus. It includes
seven wallpapers rendered from the SUBCULT marks.

## Install

Install from the published dedicated theme repository:

```bash
omarchy theme install https://github.com/PatrickFanella/omarchy-subcult-theme.git
```

The repository name resolves to the theme slug `subcult`. Installation
applies the theme; switch back later with `omarchy theme set <another-theme>`.

Cycle its wallpapers with:

```bash
omarchy theme bg next
```

This package contains only declarative theme files and images. It does not
include the SUBCULT widgets, commands, Hyprland configuration, start page, or user
services from the complete SUBCULT Rice suite.

## Want the complete SUBCULT desktop?

This theme is the lightweight, native Omarchy option. The coordinated
wallpaper affinity, themed shell widgets, workspace identities, media and Cava
integration, start page, screensaver, terminal profiles, motion system, and
installer live in the complete **SUBCULT Omarchy Rice** project:

**[Explore the complete SUBCULT Rice suite →](https://github.com/PatrickFanella/subcult-omarchy-rice)**

The suite includes this theme, so install one path or the other according to
the experience you want. Installing the theme does not silently install or
enable any suite component.

## Requirements

- A current Omarchy installation
- Git, as used by `omarchy theme install`
- An Omarchy shell version that supports split `shell.*.toml` theme fragments

## Updates and removal

Omarchy can update a Git-installed theme through its normal theme update flow.
To remove it, first select another theme, then remove only the cloned
`~/.config/omarchy/themes/subcult` directory. No unrelated configuration is
owned by this package.

## Licensing

Software/configuration is MIT-licensed. The SUBCULT name, marks, and the
wallpapers rendered from them belong to SUBCULT (subcult.tv) and are not covered
by the MIT license. Their terms are in `ASSETS_LICENSE.md`, and wallpaper
provenance is in `ARTWORK.md`.
