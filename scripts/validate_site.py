#!/usr/bin/env python3
"""Checks basic integrity for the static site before a Netlify deploy."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
EXTERNAL_SCHEMES = {"data", "http", "https", "mailto", "tel", "javascript"}


class ReferenceCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.titles = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "title":
            self.titles += 1
        for attribute in ("href", "src"):
            value = attributes.get(attribute)
            if value:
                self.references.append(value)


def is_local_reference(reference):
    parts = urlsplit(reference)
    return not parts.scheme and not reference.startswith("//") and not reference.startswith("#")


def target_exists(page, reference):
    path = unquote(urlsplit(reference).path)
    if not path:
        return True
    target = (ROOT / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    return target.exists()


def main():
    errors = []
    pages = sorted(SITE.glob("*.html"))
    if not pages:
        errors.append("Aucune page HTML trouvée dans site/.")

    for page in pages:
        content = page.read_text(encoding="utf-8")
        if not content.lower().startswith("<!doctype html>"):
            errors.append(f"{page.relative_to(ROOT)} : doctype HTML manquant.")
        parser = ReferenceCollector()
        parser.feed(content)
        if parser.titles != 1:
            errors.append(f"{page.relative_to(ROOT)} : exactement un titre HTML est requis.")
        for reference in parser.references:
            if is_local_reference(reference) and not target_exists(page, reference):
                errors.append(f"{page.relative_to(ROOT)} : ressource introuvable : {reference}")

    if errors:
        print("Validation du site échouée :", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Validation réussie : {len(pages)} pages et leurs ressources locales sont cohérentes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
