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
- to ask the human something, file it with the `ask-operator` operator and
  carry on: it never blocks, and the answer becomes an agent whenever it
  arrives

## What will go wrong first

From the first project's first full night. Every one of these produced a
confident number that meant nothing, and each is cheap to prevent.

- **You will compare scores across boards.** Agents that cannot vary - a
  constant, a coin flip - scored 1.4 to 4.3 points apart on three boards of
  the same kind. A score moving by that much says nothing. Compare paired
  within one board, or on a score measured against ground truth, which is
  not board-relative.
- **You will trust a bootstrap interval as a noise band.** It resamples
  tasks within one pair of runs and cannot see run-to-run variation. Two
  runs of an identical agent differed by 2.77 with an interval excluding
  zero. Measure the real band by running the same agent twice, several
  times, and expect it to take three or four goes before it settles.
- **Your mechanism will fire on nothing, and you will not notice.** Three
  did here: an arithmetic layer on 0 of 284 tasks, a page fetcher on 0 of
  284, a rule-quote gate on 4%. Two of them looked like results. Make every
  conditional mechanism log each decision to a file beside the agent, and
  check the fire rate before reading the score.
- **The best score on the board will be noise.** It was, twice, and both
  times the fire log was the only thing that said so.
- **A tool that regenerates will overwrite something that cost money.** A
  dry run ate a paid trigger log; a sync ate annotations on result records;
  a redirect truncated a live log. Anything derived should be rebuildable
  and anything paid for should be write-once.

The general shape: the cheap silent thing quietly destroys or misrepresents
the expensive one. Assume it is happening and go and look.

## Installing this skill for an agent

Copy or symlink this `skill/` folder into the agent's skills directory as
`agent-evolution/`:

    git clone https://github.com/Reblexis/agent-evolution
    ln -s "$PWD/agent-evolution/skill" ~/.claude/skills/agent-evolution
