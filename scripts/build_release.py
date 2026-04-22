from __future__ import annotations

import json
import os
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
DIST = ROOT / "dist"
MANIFEST_PATH = SOURCE / "manifest.json"
UPDATE_XML_PATH = ROOT / "update.xml"


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def get_version() -> str:
    version = os.environ.get("RELEASE_VERSION", "").strip()
    if not version:
        fail("RELEASE_VERSION ist nicht gesetzt.")
    return version.removeprefix("v")


def main() -> None:
    user = os.environ.get("GITHUB_USER", "Boltotelli").strip()
    repo = os.environ.get("GITHUB_REPO", "Autodarts-StatistikPlus").strip()
    extension_id = os.environ.get("EXTENSION_ID", "gikocipgcbbaddbbocecdphicbnmlkcj").strip()
    version = get_version()
    tag = f"v{version}"
    crx_name = f"statistik-plus-v{version}.crx"
    zip_name = f"statistik-plus-source-v{version}.zip"

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["version"] = version
    manifest["update_url"] = f"https://raw.githubusercontent.com/{user}/{repo}/main/update.xml"
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    update_xml = f"""<?xml version='1.0' encoding='UTF-8'?>
<gupdate xmlns='http://www.google.com/update2/response' protocol='2.0'>
  <app appid='{extension_id}'>
    <updatecheck codebase='https://github.com/{user}/{repo}/releases/download/{tag}/{crx_name}' version='{version}' />
  </app>
</gupdate>
"""
    UPDATE_XML_PATH.write_text(update_xml, encoding="utf-8")

    DIST.mkdir(parents=True, exist_ok=True)
    source_zip_path = DIST / zip_name
    if source_zip_path.exists():
        source_zip_path.unlink()

    with zipfile.ZipFile(source_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(SOURCE.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(SOURCE.parent))

    latest_dir = DIST / "latest"
    if latest_dir.exists():
        shutil.rmtree(latest_dir)
    latest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(UPDATE_XML_PATH, latest_dir / "update.xml")
    shutil.copy2(source_zip_path, latest_dir / zip_name)

    print("Prepared release files:")
    print(f"- version:     {version}")
    print(f"- update.xml:  {UPDATE_XML_PATH}")
    print(f"- source zip:  {source_zip_path}")
    print(f"- CRX name:    {crx_name}")


if __name__ == "__main__":
    main()
