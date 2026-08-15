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


def impl_path(node_dir, cfg=None):
    names = ([cfg["implName"]] if cfg and cfg.get("implName") else []) \
        + list(IMPL_NAMES)
    for n in names:
        p = os.path.join(node_dir, n)
        if os.path.exists(p):
            return p
    return None


#: Things inside an agent folder that are written after it ran, and so are
#: not part of what produced its number. Everything else is.
NOT_THE_AGENT = ("RECORD.md", "node.json")


def impl_hash(node_dir, cfg=None):
    """Hash the whole agent folder.

    An agent is its folder, not its entry point: a data file, a prompt, a
    second module beside the entry point are all part of what produced the
    number. Excluded are the things written afterwards - the record, the
    status, the analysis - and any nested folder that is an agent in its own
    right, because a child is not part of its parent.

    A project's runner must hash agents this way too, or a freeze check
    compares two different questions and the answer means nothing. That is
    not hypothetical: the first project to run this practice had a runner
    hashing the folder and a checker hashing one file, and the disagreement
    surfaced as a false "edited after it was scored" on agents nobody had
    touched.
    """
    if not impl_path(node_dir, cfg):
        return None
    h = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(node_dir):
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in ("__pycache__", "analysis")
            and not os.path.exists(os.path.join(dirpath, d, "node.json")))
        for fn in sorted(filenames):
            rel = os.path.relpath(os.path.join(dirpath, fn), node_dir)
            if rel in NOT_THE_AGENT or rel.endswith(".pyc"):
                continue
            h.update(rel.encode())
            h.update(open(os.path.join(dirpath, fn), "rb").read())
    return h.hexdigest()


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
        # one score per board: show the newest, keep the rest
        score, history = None, []
        key = rel.replace(os.sep, "__")
        if os.path.isdir(scores_dir):
            for fn in sorted(os.listdir(scores_dir)):
                if not fn.startswith(key + "@") or fn.endswith(".preds.json"):
                    continue
                try:
                    history.append(json.load(open(os.path.join(scores_dir,
                                                               fn))))
                except ValueError:
                    continue
            if history:
                score = sorted(history, key=lambda r: r.get("at") or "")[-1]
        nodes[rel] = {"path": rel, "dir": dirpath, "name": name,
                      "difference": diff, "parents": parents,
                      "operator": meta.get("operator"),
                      "status": meta.get("status", "draft"),
                      "frozen": meta.get("frozen"), "score": score,
                      "history": history, "meta": meta}
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
        key = None
        for line in open(os.path.join(d, fn)):
            head = line.split(":", 1)
            k = head[0].strip().lower()
            if len(head) == 2 and k in FIELDS and not line[:1].isspace():
                key, rec[k] = k, head[1].strip()
            elif key and line.strip():
                # A wrapped line continues the field above it. Without this
                # every request was cut off at its first line, which on a
                # page whose whole job is to say what a researcher needs is
                # the difference between a request and a fragment.
                rec[key] = (rec[key] + " " + line.strip()).strip()
            elif not line.strip():
                key = None
        out.append(rec)
    return out


FIELDS = ("what", "why", "unblocks", "cost", "status")
