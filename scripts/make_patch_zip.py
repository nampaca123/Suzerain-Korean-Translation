# dist/의 수정 번들 2개와 원 패치의 나머지 파일을 원래 폴더 구조 그대로 zip으로 묶는다.
import datetime, sys, zipfile
from pathlib import Path
from scripts import paths

PATCH_ROOT = paths.PATCH_BUNDLE_DIR.parents[3]  # .../Downloads/Suzerain_Data 의 부모(Downloads)


def make_zip(patch_root: Path, dist_dir: Path, out_zip: Path) -> list[str]:
    base = patch_root / "Suzerain_Data"; names = []
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(base.rglob("*")):
            if not p.is_file() or any(part.startswith(".") for part in p.relative_to(base).parts):
                continue  # .idea 같은 숨김 폴더 제외
            rel = "Suzerain_Data/" + p.relative_to(base).as_posix()
            src = p
            if p.suffix == ".bundle" and (dist_dir / p.name).exists():
                src = dist_dir / p.name; print(f"replaced from dist: {p.name}", file=sys.stderr)
            z.write(src, rel); names.append(rel)
    return names


if __name__ == "__main__":
    out = paths.DIST / f"Suzerain_Korean_Patch_RiziaFixed_{datetime.date.today():%Y%m%d}.zip"
    names = make_zip(PATCH_ROOT, paths.DIST, out)
    replaced = sum(1 for n in names if n.endswith(".bundle") and (paths.DIST / Path(n).name).exists())
    if replaced < 2:
        print(f"WARNING: only {replaced} bundles replaced from dist, expected 2", file=sys.stderr)
    print(f"zip={out} files={len(names)}", file=sys.stderr)
