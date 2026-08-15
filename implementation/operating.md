# Operating

The mechanics: how missions are dispatched, where their output goes, how the
human sees the state, and how requests reach the human.

## Dispatch

The orchestrator writes a mission as one file into the project's queue.
A slot process pops the oldest file, moves it to the done directory — the
move is the claim, and it is atomic — and runs it as a headless agent with
the file's contents as the whole prompt. Logs land under the project's log
directory, named by slot, mission and timestamp. Slots run in parallel and
poll when the queue is empty.

More than one model family should be dispatched against the same population.
A second family reviewing the same code and numbers sees what the first
cannot, and this is measurable rather than decorative.

## A mission

Every mission file, in this order:

1. who the agent is and which repo it works in
2. read the practice first, and the project's own rules
3. its branch and workspace
4. what to read before starting: the parents' findings and what each left
   open, the current open issues, the record of what is dead
5. the mission: its identifier, its operator, what it is testing, and the
   diagnosis it acts on
6. the design, mechanically: arms, population, repetitions, clustering, the
   thresholds printed first, the controls
7. what each outcome decides
8. what shipping would look like if it passes, without shipping it
9. the named next experiment it owes
10. its budget, the current balance, and what to do if it cannot afford the
    design
11. deliverables and the constraints that always bind

A mission whose two possible outcomes both leave the project in the same
place should not be dispatched.

## The record

Four files, all append-only, all read before any work starts:

- **claims** — who is running what, right now, with what resources
- **kills** — what died today, published the moment it is measured, so a
  parallel researcher does not buy it again this afternoon
- **graveyard** — what is dead for good, with the number and the cause, and
  the condition under which it could be revisited
- **issues** — the open failure modes of the system, each with its state,
  its evidence, and what has been attempted against it

Findings live one file per mission and are never rewritten.

## Asks

Requests to the human live in the project as one file each:

```
asks/0007-kalshi-trading-access.md

what:      an API key and a funded account on <venue>
why:       <one paragraph>
unblocks:  <what becomes possible>
cost:      <money, time, or risk>
status:    open
```

Any researcher may file one. The rendering shows every open ask beneath the
population, so the human sees them without reading the repo. Status changes
to `granted` or `declined` when answered, with a line saying what happened;
the file stays.

## The rendering

Generated from the project's state by a tool in this repo, deterministically,
with no model in the path. It shows:

- the population as a graph, laid out by descent, each agent coloured by
  status and labelled with its score
- on hover, the agent's difference from its parents and its numbers
- beneath it, the open asks

It is regenerated whenever the project's state changes and is never edited
by hand. Anything a human has to keep in sync will drift out of sync.

## Tools

`tools/new-node` scaffolds an agent folder with its spec, metadata and empty
analysis, given a name and its parents.

`tools/check-tree` validates a population: specs present, parents resolve,
no agent importing another, frozen hashes intact, no cycles. It fails; it
does not warn.

`tools/render-tree` produces the human-readable page from the population,
the scores and the asks.

A project supplies the adapter these tools call to find its population, its
scores and its asks, and nothing else.
