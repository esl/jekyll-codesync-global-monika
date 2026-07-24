#!/usr/bin/env python3
"""Minimal static server for the Lambda Days archive (preview verification).
Avoids stdlib `-m http.server`, which evaluates os.getcwd() at import and fails
under the preview sandbox's inaccessible starting cwd."""
import os
import functools
from http.server import HTTPServer, SimpleHTTPRequestHandler

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
os.chdir(SITE)  # absolute; recovers even if the inherited cwd is gone
handler = functools.partial(SimpleHTTPRequestHandler, directory=SITE)
print("serving %s at http://127.0.0.1:8907" % SITE, flush=True)
HTTPServer(("127.0.0.1", 8907), handler).serve_forever()
