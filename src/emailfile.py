"""Turn an uploaded .txt or .eml file into plain text for the detector.

The file is only read as text. Links inside it are never opened.
"""
import re
from email import policy
from email.parser import BytesParser
from html import unescape

MAX_BYTES = 1_000_000   # ignore anything past 1 MB
MAX_CHARS = 20000       # same limit as the API


def _strip_html(markup):
    markup = re.sub(r"(?is)<(script|style).*?</\1>", " ", markup)
    return unescape(re.sub(r"(?s)<[^>]+>", " ", markup))


def read_email_file(raw, name=""):
    raw = raw[:MAX_BYTES]
    if name.lower().endswith(".eml"):
        try:
            msg = BytesParser(policy=policy.default).parsebytes(raw)
            part = msg.get_body(preferencelist=("plain", "html"))
            body = part.get_content() if part is not None else ""
            if part is not None and part.get_content_type() == "text/html":
                body = _strip_html(body)
            text = f"{msg.get('subject') or ''} {body}"
        except Exception:
            text = raw.decode("utf-8", errors="replace")
    else:
        text = raw.decode("utf-8", errors="replace")
    return text.strip()[:MAX_CHARS]