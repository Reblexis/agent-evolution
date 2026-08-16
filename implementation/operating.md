# Operating

The mechanics: how missions are dispatched, where their output goes, how the
human sees the state, and how requests reach the human.

## Dispatch

The orchestrator writes a mission as one file into the project's queue.
A slot process pops the oldest file, moves it to the done directory, the
move is the claim, and it is atomic, and runs it as a headless agent with
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

- **claims**, who is running what, right now, with what resources
- **kills**, what died today, published the moment it is measured, so a
  parallel researcher does not buy it again this afternoon
- **graveyard**, what is dead for good, with the number and the cause, and
  the condition under which it could be revisited
- **issues**, the open failure modes of the system, each with its state,
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

## Doing it by hand is how you lose the thing the tool was protecting

A deploy script refused to run. The reason was real: untracked files on the
machine collided with files the incoming commits added. What followed is
worth writing down in order, because each step was reasonable and the
sequence was not.

1. The files were removed by hand, after checking each was byte-identical
   to what was coming. Correct, and it exposed the next problem.
2. A rebase then conflicted on derived score records and **wrote conflict
   markers into result files** - the same corruption this project had
   already had once that week.
3. The rebase was aborted and the machine's results were pulled into git so
   nothing could be lost. Correct.
4. Its checkout was then reset with `git reset --hard`. That **cost 270
   rows of a live trading journal**, recovered afterwards from the reflog.

Step 4 is the one to learn from. The deploy script contains a check that
refuses when that journal shrinks. It exists because the journal had been
stranded three times before. Resetting by hand did the same job as the
deploy script with that check removed, and removed exactly the check that
mattered.

**The rule: when a tool refuses, fix the tool.** A tool that refuses is
usually refusing for a reason it knows and you have not reconstructed yet,
and the hand-run version of what it does is the same operation minus every
guard somebody added after being burned. If the fix is urgent, add the
missing case to the tool and run the tool - that is rarely slower, and it
leaves the next person protected.

**And the corollary for recovery: capture before you reset.** The reflog
saved this one, which was luck rather than design. Copy the mutable state
somewhere outside the repository first, verify what you captured parses,
and only then let anything destructive run.

**A related failure from the same hour, worth pairing with it.** A queue of
sixteen registered runs emptied in eight seconds because a tool crashed at
startup on every item: name resolution had been added to two tools, tested
through the one that imported its helper, and not the other. Nothing was
spent and nothing was measured, and the queue looked exactly like a queue
that had finished. A worker that pops work before the work succeeds cannot
tell those apart. **Count consecutive failures and stop**, and leave the
remainder where it was.

## Two traps that cost a whole day between them

**`pkill -f` matches the command that issued it.** Killing a background
worker by pattern from inside a shell whose own command line contains that
pattern kills the shell first, and the kill never happens. The bracket
trick - `[d]rain.sh` - only helps when the pattern appears nowhere else in
the command, and it will appear if the same line also copies or restarts
the thing. This happened three times in one session; the third time it
killed the session that was trying to restart a stalled worker, leaving it
stopped. Kill by PID, in a command that does nothing else.

**A worker that snapshots itself only picks up fixes on restart.** A
long-running script that copies itself to a temporary path before running -
a sensible guard, so a deploy cannot rewrite it mid-execution - also means
every fix to it lands one full run later. The same deadlock was fixed three
times and reappeared each time because the copy in memory was the old one.
If a worker snapshots itself, the fix is not deployed until the worker is
restarted, and nothing about the repository state will tell you that.
