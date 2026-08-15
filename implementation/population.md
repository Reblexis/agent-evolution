# Population

The on-disk shape of a population, and the rules that keep it honest.

## Layout

A project holds its population under one directory. Each agent is a folder
inside it; a child's folder is inside its first parent's folder, so the
directory tree is the primary descent and additional parents are recorded in
metadata.

```
<population>/
  _api/                    the project's interface to the outside world
  <root-agent>/
    SPEC.md
    agent.py               (or whatever the project's runtime is)
    node.json
    analysis/
      tasks.jsonl
      STRENGTHS.md
    RECORD.md
    <child-agent>/
      ...
```

`_api` is the only thing an agent may import from the project. It exposes
the task type, the readers that fetch tasks, and — for a project that acts
in the world — the execution path. It does not expose model access, prompt
helpers, or anything else an agent could differ in: those belong inside
agents, where the differences are visible.

## SPEC.md

The first line is the agent's name in plain words. The rest is one to three
sentences saying only how this agent differs from its parents.

It does not restate the parents. It does not describe the code. It does not
use the project's internal vocabulary if a plain word exists. A reader who
walks from the root to this agent, reading each SPEC in turn, has read the
whole design.

## node.json

```json
{
  "parents": ["<path>", "<path>"],
  "operator": "autopsy",
  "status": "candidate",
  "frozen": {"hash": "<sha256 of the implementation>", "at": "<iso8601>"}
}
```

`parents` is a list; the first is the directory parent. `operator` is the
move that produced this agent, from the set in `evolution.md`. `status` is
one of `draft`, `candidate`, `champion`, `closed`. `frozen` appears once the
agent has a score and never changes after.

## Freezing

An agent is frozen the moment a score is written for it. From then on:

- its implementation, `SPEC.md` and `analysis/` are immutable
- the recorded hash is checked mechanically; a mismatch is an error, not a
  warning
- a correction is an erratum appended to `RECORD.md`
- any change of behaviour is a new agent, even a one-line change

The rule exists because a number that does not refer to an exact
implementation refers to nothing, and because populations that allow
in-place edits accumulate agents whose published results were produced by
code that no longer exists.

## analysis/

`tasks.jsonl` — one row per task in the board, written by the runner: the
task id, what the agent produced, what the score was, what it cost, and any
trace the agent chose to record. This file is data; it is not interpreted.

`STRENGTHS.md` — where this agent does well, where it does badly, and the
most general reason for each, written by a researcher who read the cases.
Each claim names the tasks that support it. This document is the input to
every rational operator: an operator that has not read it is guessing.

A generated first pass (groupings, the largest error masses, the tasks where
this agent most beats and most trails the field) is produced by the runner
as a starting point. The reasons are written by a person or an agent that
read the cases, never generated from the groupings alone.

## RECORD.md

What has been measured about this agent: the scores with their intervals and
the board they were measured on, the controls that were run, any errata, and
links to the missions and findings that produced them. Records accumulate;
nothing is rewritten.

## Checks

`tools/check-tree` enforces, and fails the build on any violation:

- every agent has `SPEC.md`, an implementation, and `node.json`
- every declared parent resolves to an existing agent
- no agent imports another agent
- every scored agent's implementation hashes to its frozen hash
- no cycles in the parent graph
