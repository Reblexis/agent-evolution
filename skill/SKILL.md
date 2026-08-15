---
name: agent-evolution
description: >
  Evolve a population of AI agents against a measurable metric: agents as
  standalone folders in a directed graph, rational operators driven by
  per-task diagnosis, frozen once evaluated, scored against ground truth
  with mandatory controls. Use when asked to "adopt agent-evolution", to
  set up or run an agent-evolution population, to propose or evaluate a new
  agent variant, to run an evolution operator (autopsy, crossover, booster,
  graft, specialization, restart, step-back, first-principles, or something
  genuinely new), or when working in a repo that names agent-evolution as
  its practice.
---

# agent-evolution

Governing doc: `docs/practice.md` in
https://github.com/Reblexis/agent-evolution. This skill is the
implementation of that document, alongside the repo's `implementation/`
files, which are the authoritative elaboration:

- `implementation/population.md`, the on-disk population: one folder per
  agent, a complete standalone implementation in each, a spec that states
  only the difference from its parents, `node.json` carrying parents,
  operator and frozen hash, an `analysis/` folder holding the per-task table
  and the written strengths and weaknesses, and a record. **Agents are
  frozen once scored**; a change of behaviour is a new agent.
- `implementation/evolution.md`, the operators. Every one of them is
  rational: read per-task results, name the most general reason behind a
  pattern, act on that reason, state it as a mechanical condition. autopsy,
  rational-ablation, rational-substitution, rational-crossover, booster,
  rational-graft, rational-specialization, rational-restart, step-back,
  first-principles, and crazy-new-thing (the one operator with no diagnosis
  requirement and no list to choose from, its only constraint is that it
  resembles nothing already in the population).
- `implementation/metric.md`, the metric contract. The deciding score is
  measured against ground truth, never against another estimator; the board
  must not contain its own answers; two controls are mandatory, the
  population's own noise band measured on that board and the constant rule.
- `implementation/researching.md`, how a research agent works: claim before
  you run, preregister the threshold and print it first, cluster correlated
  tasks, exact tests below ten clusters, paste numbers rather than
  remembering them, audit instruments before believing them, finish with a
  finding and a named priced next experiment, and file an ask and stop when
  something needs the human.
- `implementation/operating.md`, dispatch, the append-only record, the asks
  channel, and the generated rendering.

Follow those documents when executing. Where they and a project's own docs
differ, the project's docs win. Where anything here contradicts
`docs/practice.md`, this skill is wrong.

## Working in a project that practices this

Read the project's population record before proposing anything: what is
open, what is dead and why, what other researchers are running. Then:

- to propose an agent, name the operator, write the diagnosis it acts on,
  and scaffold with `tools/new-node`
- to evaluate one, use the project's runner; never score by hand
- to change an agent that already has a score, don't, create a child
- to validate the population, `tools/check-tree`, which fails rather than
  warns
- to publish, `tools/render-tree`, never hand-edit the page

## Installing this skill for an agent

Copy or symlink this `skill/` folder into the agent's skills directory as
`agent-evolution/`:

    git clone https://github.com/Reblexis/agent-evolution
    ln -s "$PWD/agent-evolution/skill" ~/.claude/skills/agent-evolution
