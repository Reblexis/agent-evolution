# Agent evolution

This repo describes a way to make an AI agent better at a measurable thing,
by evolving a population of agents against a metric and keeping the whole
attempt legible to a human.

Everything else in the repo is the implementation of that description. Where
the implementation contradicts this document, the implementation is wrong.
A project that adopts this practice supplies what only it can supply: the
task population, the metric, and the agents. Nothing here knows what the
agents do.

## The population

A project holds a population of agents. Each agent is one folder. The folder
holds a complete, standalone implementation, a short statement of how the
agent differs from the agents it descends from, its own analysis of where it
succeeds and fails, and its record of what has been measured about it.

Agents are not built from shared parts. An agent may reuse only the
project's interface to the outside world; everything that makes it the agent
it is lives in its own folder and is readable there in full. Two agents that
differ by one idea duplicate everything else, and that duplication is the
price of being able to read any single agent and know what it does.

Descent is recorded, and an agent may descend from several. The population
is therefore a directed graph, not a tree, and a mechanism taken from one
agent and applied to another is an edge from both.

An agent is frozen the moment it has been evaluated. Its implementation, its
statement and its analysis are never edited again; a correction is an
erratum in its record, and a change of behaviour is a new agent. What
enforces this is a hash of the implementation stored when the agent was
frozen, checked mechanically. Without this rule a published number stops
referring to anything.

## Difference, stated

An agent's statement says only how it differs from its parents, in plain
language, in as few sentences as the difference takes. It does not restate
what the parents already do, and it does not describe the implementation. A
reader walking a path from the root to any agent reads the whole design of
that agent as a sequence of differences.

The root of a population is the simplest thing that performs the task at
all.

## Evolution

A new agent exists because an operator was applied to existing agents. The
operator is recorded, so a project can measure which of its operators
produce winners and spend accordingly.

Operators are rational: an operator reads per-agent, per-task results, names
the most general reason behind a pattern of successes or failures, and acts
on that reason. Blind variation is not an operator here. The reason an
operator acts on must be stated as a condition that can be checked
mechanically, because a reason that exists only as an instruction to a model
is not a reason the population can inherit.

One operator is deliberately outside this rule: the population must be able
to try something that resembles nothing already in it. Its only constraint
is that constraint.

## The metric

A project supplies a metric contract: a frozen population of tasks, a score
that decides, and the controls a claim must pass.

The score that decides is measured against ground truth. A score measured
against something that is itself an estimate of the truth measures agreement
with that estimator, and a population evolved against it converges on the
estimator rather than on the truth. A project may keep such a score as a
cheap screen, and if it does, it says so wherever the number appears.

The task population is frozen before it is used, and it is frozen in a state
that cannot leak the answer: if the answer to a task already exists in the
world, an agent that searches will find it, and the score becomes a measure
of searching for answers rather than of producing them.

Two controls are mandatory in every claim. The first is the population's own
noise: run the incumbent against itself and measure the spread, because a
threshold inside that spread cannot be met by any real effect. The second is
the constant: whatever the simplest rule is that ignores the input entirely,
a claim must beat it, because most apparent skill is a marginal in disguise.

## Selection

An agent replaces the incumbent only on the deciding score, having passed
the controls, without losing the incumbent's successes beyond a bound
declared in advance.

Agents that lose stay in the population, marked, carrying their number and
the reason they failed. The record of what does not work is the more
valuable half of the population, because it is what stops the next attempt
from buying the same null again.

A lineage is worked while it has a stated live reason to be worked. When
that reason is gone, the lineage is closed and its budget returns. Several
lineages are kept alive on purpose: a population that has collapsed to a
single agent has stopped evolving.

## Researchers

Agents in this population are built by AI research agents working in
parallel, each on one assignment, each running to completion and stopping.
The rules they work under, and the mechanics of dispatching them, are the
implementation of this document.

A researcher that needs something only the human can provide, access, a
credential, money beyond its budget, a decision, writes the request into
the project where the human will see it, and stops. It does not wait, and it
does not proceed without it.

## What the human sees

The state of the population is on disk in the project, and a human-readable
rendering is generated from it deterministically, with no model in the
generation path. The rendering shows the graph, what each agent is, how well
it does, and what the researchers are waiting for. It is generated, never
maintained: anything a human would have to keep in sync by hand will fall
out of sync.
