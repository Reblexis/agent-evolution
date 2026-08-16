# Evolution

How new agents are produced, which ones survive, and where proposals come
from.

## The rule under all of it

An operator does not vary an agent and see what happens. It reads
per-task results, names the most general reason behind a pattern of
successes or failures, and changes the agent because of that reason. The
diagnosis comes first and is written down; the change is derived from it.

"Most general" is the working part. A reason that covers one task is an
anecdote and produces an agent that has memorised a task. A reason that
covers a class is a mechanism and produces an agent that has learned
something. When the diagnosis will not generalise past a handful of cases,
that is itself the finding, and the operator stops.

The reason must be checkable mechanically. An instruction added to a prompt
telling a model to be careful about something is not a mechanism; a
condition in code that fires on the class is.

### Changing the output is not a mechanism either

The prompt-versus-code line above is the easy half, and it is not enough.
The first project to run this practice refuted **seven** mechanisms in one
night, and they had one thing in common that the prompt-versus-code
distinction does not capture. Three were prompt changes: rewording the
question, asking what would have to go wrong instead of how likely, and
asking for a date so the answer could be computed rather than stated. Four
were code: routing on a judged fact, gating a confident answer on a quoted
rule, shrinking answers toward a constant, and shrinking them more where
they were confident.

All seven transformed **what the model said**. None changed **what the
model knew**. Every one came back inside the noise band or worse.

Two of them settled it beyond argument. Asked for a date instead of a
probability, the model expressed the same certainty through the new
channel - "will this ever happen: no" - and the arithmetic turned that into
0.02 on a quarter of the board; saturation rose rather than fell. And a
mechanism and its **exact inverse** - shrink confident answers more, shrink
them less - differed by 0.82 on a noise band of 1.88, which is what two
treatments look like when the quantity they both key on carries nothing.

Meanwhile the one thing that moved a number was adding a search: worth 13
to 19 points on the slice where the model lacked information, and a cost
elsewhere.

So the working rule is sharper than "code, not prompts":

> A transformation of the agent's own output is not new information, and on
> a task where the agent's problem is what it does not know, it will do
> nothing. Ask what the child will **know** that its parent did not.

This does not mean output transformations are always inert - a genuinely
miscalibrated estimator can be fixed by shrinking it, and that project's
own older record is full of cases where it worked. It means they cannot
manufacture information, so they only help where the failure is expression
rather than knowledge. Establish which one it is before spending a round on
it.

An operator's input is the `analysis/STRENGTHS.md` of the agents it acts on,
and where that document does not exist yet, producing it is the first half
of the work.

## The operators

Each names its input, its procedure, and the control its child must pass on
top of the project's ordinary acceptance rules.

### autopsy

*Input*: this agent's failures.
*Procedure*: find the largest concentration of error, read those cases, name
the most general cause, fix that cause.
*Control*: the child must improve the cases that motivated it, and must not
lose the parent's successes.

### rational-ablation

*Input*: this agent's failures, attributed to its components.
*Procedure*: determine which component is causing the damage, not which is
unused, and remove it.
*Control*: the argument comes from the failing cases, not from trying every
removal and keeping the best. A removal that improves things without an
explanation is a finding to investigate, not a child to ship.

### rational-substitution

*Input*: the failure mass per component, and the candidates that could
replace one.
*Procedure*: pick the component carrying the most failure mass, and replace
it with the candidate most likely to address that specific cause.
*Control*: everything else stays byte-identical, so the contrast is the
substitution alone.

### rational-crossover

*Input*: the per-task tables and strength documents of two agents.
*Procedure*: find where each parent wins, diagnose *why* each wins, and
build a child that carries both mechanisms.
*Control*: the child must beat both parents, and it must beat the naive
combination that simply sends each task to whichever parent won it before.
Mechanisms transfer between populations; the locations where they helped do
not, and a child that has learned the locations will not survive contact
with a new board.

### booster

*Input*: the tasks where this agent beats the rest of the population.
*Procedure*: name the general reason it wins there, then amplify that
mechanism, apply it more deeply, or more widely, or with more of whatever
makes it work.
*Control*: it must not give back the wins it was built on. If the
amplification is targeted at a slice, it must also beat applying the same
amplification everywhere.

### cheaper-and-better

*Input*: this agent's per-task costs beside its per-task results.
*Procedure*: work out where the money and the minutes actually go, and
which of that spending is buying anything. Then build the version that
costs less and is at least as good - fewer calls, a smaller model where the
task does not need a larger one, work skipped on the tasks it never changed,
whatever the cost table says.
*Control*: the child must not be worse. "At least as good" is measured
against the parent's own noise band, not against zero, because a cheaper
agent that is genuinely equal will still score a little differently every
run. Report the new cost per task next to the old one; a saving that cannot
be stated as a number was not measured.

Cost is a real axis of the metric, not an afterthought. An agent that
matches the incumbent for a tenth of the spend can be run on ten times the
tasks, and that is usually worth more than a small accuracy gain.

### rational-graft

*Input*: a mechanism identified as another agent's strength, and this
agent's weakness profile.
*Procedure*: port that mechanism onto this base, because this base's
weakness is what that mechanism addresses.
*Control*: the child must beat its base, and the grafted mechanism must beat
its own null in the new setting. A mechanism can be worth nothing away from
the agent it grew in.

### rational-specialization

*Input*: this agent's strength profile.
*Procedure*: restrict the agent to the region where it is strong.
*Control*: the restriction must be a trigger that fires observably in
production and is recorded before any accuracy is claimed for it, and it
must beat the constant rule of applying the agent everywhere or nowhere. A
table of regions fitted offline is refused: fitted regions do not transfer,
and a fitted table that appears to work is usually reproducing the
population's marginal.

Two things make this operator survivable, and both are cheap.

**Write the fire rate down before the run.** A range, in advance. A trigger
that fires on almost everything is not a trigger, and one that fires on
almost nothing cannot be responsible for any change in the score - so if
the score moves anyway, something else moved it.

**Have the agent log every decision as it goes**, to a file beside it. The
paired comparison that decides the operator is not the whole-board one; it
is the comparison restricted to the tasks where the trigger actually fired.
Without the log that comparison cannot be made at all.

Worked example from the first project: a specialization posted the best
whole-board score in the population. Its trigger fired on 49% of the board
against a fifth-to-a-third written down in advance, and against the same
mechanism applied everywhere it scored -0.95 [-3.89, +1.95] overall and
+0.84 [-3.66, +5.75] on the tasks where it fired. It was refused. Without
the fire log it would have entered the record as the best agent there.

### rational-restart

*Input*: the failure causes that recur across the whole population.
*Procedure*: design a new agent from an empty file whose architecture
attacks a cause that keeps reappearing no matter which lineage is worked.
*Control*: its stated reason to exist names that recurring cause, and its
first evaluation is against the incumbent, not against its own ambition.

### step-back

*Input*: the population, the metric, and the task board, together.
*Procedure*: ask what is being missed entirely. Is a whole dimension
unexplored. Is there an obvious improvement nobody tried because everyone
was busy refining. Is an instrument broken. Is the score measuring the thing
we want.
*Control*: none, because its output is often not an agent. It may produce an
agent, or an issue, or a repair to the benchmark, or a request to the human.
It is the operator most likely to produce the largest single improvement,
and the one most likely to be skipped, because everything else feels like
progress and this feels like doubt.

### first-principles

*Input*: this agent's strengths and weaknesses.
*Procedure*: work out from the ground up what the ideal procedure for this
task population would be, ignoring what the current lineage happens to do,
then build the nearest reachable thing to it.
*Control*: it states what it kept from the parent and what it discarded, so
the result is not an unexamined restart wearing a lineage's name.

### crazy-new-thing

*Input*: the population, read as the set of everything already tried.
*Procedure*: do something that is not in it. A tool nothing here uses, a
source nothing here reads, a way of arriving at the answer that no lineage
resembles.
*Control*: none beyond the ordinary scores, and no requirement to justify
itself from a diagnosis. There is deliberately no list to choose from: a
list of unexplored ideas is a list of ideas someone already had. The only
constraint is the negative one, and it is checked against the population
itself.
*Budget*: capped, and spent regardless of how the last one went. Without
this operator the population only ever explores its own neighbourhood, and
the cost of that is invisible until it is enormous.

### ask-operator

*Input*: the population as it stands, and one agent the researcher wants
advice on.
*Procedure*: write the human a description of where things actually are -
what each family does, what the numbers say, where this agent is strong and
where it is weak, what has been tried on it and failed - and ask what to
change. Then **leave**.
*Control*: the child that eventually comes back is judged like any other,
and its record quotes the reply that produced it, so a human suggestion
that does not work is recorded as such rather than quietly dropped.

**It must never block.** A human answers on their own schedule, and a
population that waits is a population doing nothing. So the operator has
two halves that run at different times:

- **filing.** The question goes into the asks channel with the state
  description attached. The operator then returns, and the round
  immediately selects a different agent and applies a different operator.
  Nothing waits.
- **collecting.** Every round begins by checking the asks channel for
  answered questions. An answer that has not yet produced an agent produces
  one now, as an ordinary child with `ask-operator` as its operator and the
  agent that was asked about as its parent.

An answer that arrives three days later is still worth acting on, and a
question that is never answered costs nothing beyond the writing.

This is the only operator whose input comes from outside the system. That
is exactly why it is worth having: everything else can only recombine what
the population already contains, and the human is the one participant who
can see the frame the whole population is working inside. It is also the
operator most likely to be quietly skipped, because filing a question feels
less like progress than building something.

Writing the description is most of the value even when no reply comes. A
researcher who cannot say plainly what its agents are good at does not know.

## What is not an operator

Changing a parameter. That is a substitution, and it needs the same stated
reason the old value was wrong. A sweep over parameter values is not
evolution; it is a way of finding the value that best fits the board.

## Selection

An agent becomes the incumbent only when it passes, on the deciding score:

- the score, by a margin declared before the run
- the population's own noise band, measured on that board, not imported
- the constant rule
- the incumbent's successes, kept within a bound declared before the run

Agents that fail stay in the population with their number and the reason.
A lineage with no stated live reason to be worked is closed. Two consecutive
rounds on a lineage with nothing clearing the bar closes it, and its budget
returns to the pool. More than one lineage stays open at all times.

## Where proposals come from

The sources, in the order a project should prefer them until it has measured
its own:

- **the previous mission's named next experiment.** Every mission ends by
  naming and pricing the single highest-value thing to do next; that is a
  deliverable, not a courtesy. Measured on the first project to run this:
  39% produced a durable result and none produced nothing, over 28 missions.
- **a scan or audit over data already collected.** Measured at 44-50%, and
  cheap, which is why no build is dispatched without a scan naming the slice
  it should attack.
- **the human's idea.** Measured at 21% directly, but it starts the chains
  that produce the 39%, and it is the only source that can see the frame
  everyone inside is working within.
- **a review by a different model family.** A second family reading the same
  code and the same numbers finds what the first cannot see, measured at 14
  findings in four missions on the first project, two of them things the
  home family had walked past for days.

Because the operator is recorded on every agent, a project measures these
priors on itself as its population grows, and re-weights.
