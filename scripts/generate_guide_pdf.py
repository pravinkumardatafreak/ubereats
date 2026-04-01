"""
Build docs/PROJECT_FULL_GUIDE.pdf from docs/PROJECT_FULL_GUIDE.md
Run from project root: python scripts/generate_guide_pdf.py
Requires: pip install markdown xhtml2pdf
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD_PATH = ROOT / "docs" / "PROJECT_FULL_GUIDE.md"
PDF_PATH = ROOT / "docs" / "PROJECT_FULL_GUIDE.pdf"


def main() -> int:
    try:
        import markdown
        from xhtml2pdf import pisa
    except ImportError:
        print("Install: pip install markdown xhtml2pdf", file=sys.stderr)
        return 1

    if not MD_PATH.is_file():
        print(f"Missing: {MD_PATH}", file=sys.stderr)
        return 1

    text = MD_PATH.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "nl2br"])
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; margin: 24px; line-height: 1.35; }}
  h1 {{ font-size: 18pt; }}
  h2 {{ font-size: 14pt; margin-top: 14pt; }}
  h3 {{ font-size: 12pt; }}
  table {{ border-collapse: collapse; width: 100%; margin: 8px 0; }}
  th, td {{ border: 1px solid #444; padding: 4px 6px; text-align: left; }}
  th {{ background: #eee; }}
  code {{ font-size: 10pt; }}
  hr {{ margin: 12px 0; }}
</style></head><body>{body}</body></html>"""

    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PDF_PATH, "wb") as f:
        status = pisa.CreatePDF(html, dest=f, encoding="utf-8")
    if status.err:
        print("PDF generation reported errors.", file=sys.stderr)
        return 1
    print(f"Wrote: {PDF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
