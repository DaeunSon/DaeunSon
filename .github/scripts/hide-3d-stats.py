#!/usr/bin/env python3
"""Remove contribution count, star, and fork stats from 3D contrib SVGs."""

from pathlib import Path
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
STAR_PATH_PREFIX = "M8 .25a.75.75"


def _tag(el: ET.Element) -> str:
    return el.tag.split("}")[-1]


def hide_stats(path: Path) -> bool:
    tree = ET.parse(path)
    root = tree.getroot()
    changed = False

    for group in root:
        if _tag(group) != "g":
            continue

        has_contrib_label = any(
            _tag(child) == "text" and (child.text or "").strip() == "contributions"
            for child in group
        )
        has_star = any(
            _tag(child) == "g"
            and any(
                _tag(icon) == "path"
                and (icon.get("d") or "").startswith(STAR_PATH_PREFIX)
                for icon in child
            )
            for child in group
        )
        if not (has_contrib_label or has_star):
            continue

        for child in list(group):
            keep_date = (
                _tag(child) == "text"
                and child.get("dominant-baseline") == "hanging"
            )
            if keep_date:
                continue
            group.remove(child)
            changed = True

    if changed:
        tree.write(path, encoding="utf-8", xml_declaration=False)
    return changed


def main() -> None:
    folder = Path("profile-3d-contrib")
    for svg in sorted(folder.glob("*.svg")):
        hide_stats(svg)


if __name__ == "__main__":
    main()
