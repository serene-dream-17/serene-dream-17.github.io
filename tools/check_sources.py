# -*- coding: utf-8 -*-
"""可选：检查外部来源链接的可达性（需要网络）。

用法：
    python tools/check_sources.py
    python tools/check_sources.py --json source_check.json

说明：部分站点会拦截 HEAD（403/429）或超时；这里只用于发现明确的 404/410，
不把 403/超时当作失效。默认使用系统证书校验；只有显式传入 --insecure 时才跳过校验。
"""

import argparse
import concurrent.futures
import json
import ssl
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from data import sources  # noqa: E402

def check(item, insecure=False):
    kind, key, url = item
    context = ssl._create_unverified_context() if insecure else None
    try:
        req = urllib.request.Request(
            url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 (compatible; archive-audit)"}
        )
        with urllib.request.urlopen(req, timeout=8, context=context) as r:
            return {"kind": kind, "key": key, "url": url, "status": r.status, "result": "ok"}
    except urllib.error.HTTPError as e:
        return {"kind": kind, "key": key, "url": url, "status": e.code, "result": "http"}
    except Exception as e:
        return {"kind": kind, "key": key, "url": url, "status": None, "result": type(e).__name__}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_path")
    parser.add_argument("--insecure", action="store_true", help="跳过 TLS 证书校验（不推荐）")
    args = parser.parse_args()

    items = [("lang", k, v[1]) for k, v in sources.LANG.items()]
    items += [("fw", f"{s}/{n}", v[1]) for (s, n), v in sources.FW.items()]

    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        results = list(ex.map(lambda item: check(item, args.insecure), items))

    print("total:", len(results))
    print("results:", dict(Counter(r["result"] for r in results)))
    print("status:", dict(Counter(r["status"] for r in results if r["status"])))
    missing = [r for r in results if r["status"] in (404, 410)]
    print("404/410:", len(missing))
    for r in missing:
        print(" -", r["kind"], r["key"], r["url"])
    print("blocked/timeout are reported but not treated as broken.")

    if args.json_path:
        Path(args.json_path).write_text(
            json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print("wrote", args.json_path)


if __name__ == "__main__":
    main()
