"""Shared reading of a project's population. No third-party imports.

A project declares itself with .agent-evolution.json at its root:

    {
      "name":       "trader-agent",
      "population": "traders",
      "scores":     "state/bench",
      "asks":       "asks",
      "metric":     {"name": "points from the outcome",
                     "lowerIsBetter": true,
                     "screen": "points from the market price"}
    }

Everything else is discovered from the tree: an agent is any directory
containing node.json.
"""
import hashlib
import json
import os

CONFIG_NAME = ".agent-evolution.json"
IMPL_NAMES = ("agent.py", "trader.py", "main.py", "agent.sh")


def find_project(start="."):
    """Walk up from start until .agent-evolution.json is found."""
    d = os.path.abspath(start)
    while True:
        p = os.path.join(d, CONFIG_NAME)
        if os.path.exists(p):
            return d, json.load(open(p))
        parent = os.path.dirname(d)
        if parent == d:
            raise SystemExit("no %s found above %s" % (CONFIG_NAME, start))
        d = parent


def impl_path(node_dir):
    for n in IMPL_NAMES:
        p = os.path.join(node_dir, n)
        if os.path.exists(p):
            return p
    return None


def impl_hash(node_dir):
    p = impl_path(node_dir)
    if not p:
        return None
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def spec_of(node_dir):
    """(name, difference). First line is the name, rest is the difference."""
    p = os.path.join(node_dir, "SPEC.md")
    if not os.path.exists(p):
        return os.path.basename(node_dir), ""
    lines = [l.rstrip() for l in open(p).read().strip().splitlines()]
    name = lines[0].lstrip("# ").strip() if lines else ""
    body = " ".join(l.strip() for l in lines[1:] if l.strip())
    return name or os.path.basename(node_dir), body


def load_population(root, cfg):
    """Every agent in the project, keyed by path relative to the population
    root. Each value: name, difference, node.json fields, score if any."""
    pop_root = os.path.join(root, cfg["population"])
    scores_dir = os.path.join(root, cfg.get("scores", "state/bench"))
    nodes = {}
    for dirpath, dirnames, filenames in os.walk(pop_root):
        dirnames[:] = [d for d in dirnames
                       if not d.startswith((".", "_", "__"))]
        if "node.json" not in filenames:
            continue
        rel = os.path.relpath(dirpath, pop_root)
        try:
            meta = json.load(open(os.path.join(dirpath, "node.json")))
        except ValueError as e:
            raise SystemExit("bad node.json in %s: %s" % (rel, e))
        name, diff = spec_of(dirpath)
        parent_dir = os.path.dirname(rel)
        parents = list(meta.get("parents") or
                       ([parent_dir] if parent_dir and parent_dir != "." else []))
        score = None
        sp = os.path.join(scores_dir, rel.replace(os.sep, "__") + ".json")
        if os.path.exists(sp):
            try:
                score = json.load(open(sp))
            except ValueError:
                score = None
        nodes[rel] = {"path": rel, "dir": dirpath, "name": name,
                      "difference": diff, "parents": parents,
                      "operator": meta.get("operator"),
                      "status": meta.get("status", "draft"),
                      "frozen": meta.get("frozen"), "score": score,
                      "meta": meta}
    return nodes


def load_asks(root, cfg):
    """Operator requests: one file each, simple key: value header."""
    d = os.path.join(root, cfg.get("asks", "asks"))
    out = []
    if not os.path.isdir(d):
        return out
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"):
            continue
        rec = {"file": fn, "status": "open"}
        for line in open(os.path.join(d, fn)):
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip().lower()
                if k in ("what", "why", "unblocks", "cost", "status"):
                    rec[k] = v.strip()
            if line.strip() == "":
                continue
        out.append(rec)
    return out
