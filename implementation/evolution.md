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

## When selection is worth less than averaging

Selection is the default move of this practice: run the population, promote
the winner, build children of it. That move has a precondition nobody
states, and it is worth checking before every promotion.

**Selection needs the quality difference between agents to be large
relative to the per-task noise.** When it is not, ranking is fitting noise
and the promotion apparatus is expensive theatre.

Measured on one project, 2026-08-16, across every ordered pair of four
boards:

| | score, lower better |
|---|---|
| the average agent | 20.4 |
| the winner picked on another board | 19.5 |
| **every agent averaged** | **17.2** |

Rank transferred moderately - mean Spearman +0.550 - so selection was not
worthless: it bought 0.89 points. Averaging bought 2.29, in twelve board
pairs out of twelve, and beat an *oracle* allowed to pick the best single
agent on the test board itself in eleven out of twelve.

The reason was measurable and is the thing to check: per-task noise was
about 22 points and true differences between agents were one to two. A
signal of one under noise of twenty-two cannot be selected on, and is
exactly what averaging exists for.

**The check, before promoting anything:**

1. Measure the per-task noise, by running one agent twice.
2. Measure the spread of agent means.
3. If the spread is small next to the noise divided by the square root of
   the task count, the ranking is mostly noise. Compare the population's
   average output against its best member before promoting the best member.

**When it fails, the output of a round is an ensemble, not a champion**,
and selection's job changes from picking a winner to deciding what is worth
keeping in the pool. Children are still built from diagnoses of individual
agents - that part is unaffected, because an autopsy reads a mechanism's
failures and does not need the mechanism to be the best one.

Two warnings. An ensemble sits nearer the consensus of its members, so if
the metric rewards agreeing with some other consensus, part of the gain may
be that and not accuracy - check against a metric that cannot be gamed that
way before believing it. And averaging costs one run per member per task,
so an ensemble that needs eleven members to beat one agent has multiplied
the cost of every future round by eleven; the curve of members against gain
has to be measured, not assumed.

### Selecting parents when performance is noisy

Selection has two jobs that get conflated, and only one of them survives
contact with a noisy metric.

**Picking a champion is often dominated by averaging** - see the section
above. **Picking who breeds is not**, and it should be weighted by
performance rather than by whichever agent somebody happened to autopsy
first. On one project, six of seven children in a round came off the fifth
agent rather than the first, because the fifth was the one with twin runs
and therefore the most diagnostic data. The agent whose failures you read
and the agent you build the child on are two different choices.

The scheme that survives a noisy metric, in order:

1. **Score relative to the field on each task-set, not absolutely.** The
   same agent scored 18.15 and 20.98 on two boards; that is the boards, not
   the agent. Pool the relative numbers, weighted by tasks.
2. **Shrink by uncertainty.** `shrunk = raw x tau2 / (tau2 + se2)`, where
   `se` is the per-task noise over the square root of the tasks the agent
   ran, and `tau2` is the variance of the raw fitnesses minus the mean
   sampling variance. An agent measured once on a small set barely leaves
   the population mean; one measured four times keeps its number. On the
   project above this moved the leader from -1.92 to -1.39, so 28% of its
   apparent lead was noise it would have bred on.
3. **Carry elites over untouched.** A good lineage should not be lost to
   one bad draw.
4. **Draw the rest by linear rank weight, not fitness proportion.** These
   scores are distances with an arbitrary zero, so a proportional weight on
   them means nothing. Best gets weight `pressure`, worst gets 1, linear
   between.
5. **Closed lineages keep their number and stop breeding.** That is what
   closing one meant.

The check that says whether any of this is worth running: compare the
population's average output against its best member. If averaging wins,
selection is for breeding only and the round's output is an ensemble.

## Averaging raises the floor and lowers the ceiling

A population that can average its members will keep proposing to average
more of them, because each addition looks like it helps. Measure it as a
curve over subset size and the shape gives the mechanism away:

    k members averaged   best subset   mean subset
        1                   16.95         21.04
        3                   17.26         19.49
        6                   19.00         19.00

The two columns converge from opposite directions. Averaging is pulling
every subset toward the same middle: it lifts a randomly chosen member and
it caps the best one. That is variance reduction, and it is worth having
when you cannot tell your members apart. It is **not** accuracy, and a
lineage that keeps buying members while calling it accuracy is paying more
each generation to move toward its own average.

The distinguishing question is whether the members differ in quality. Here
they ran from 16.95 to 27.00 - a factor the averaging simply absorbed, so
averaging a good member with a bad one produced something worse than the
good member alone. **When members vary in quality more than they vary in
error, selecting beats averaging.** When they are near-equals that fail
independently, averaging wins. Measure which regime you are in before
spending a generation on either, and the subset curve measures it in one
run for free if every member's output is logged.

### The trap in the same table

Best-of-k is selected after the fact. The 16.95 is the *maximum* of six
draws, so it carries the optimism of that maximum, and a lineage that
promotes it on the strength of this table has fitted the board. Mean-of-k
is the honest column: it says averaging genuinely helps against a member
chosen blind, which is the only kind you can commit to in advance.

So the finding licenses exactly one move - go and test the apparent best
member on a board frozen *after* the choice was made - and it does not
license promoting it. The free direction and the real effect are both in
that table, and only a held-out board separates them.

### The median discards the member that is rarely right and decisive

The rule above - robust aggregation when members are unequal - held on three
boards and then flipped on the fourth, and the flip is more useful than the
rule.

On three boards with a fixed set of six members, the median beat the mean
every time. On the fourth, one member was swapped and the mean beat the
median, 18.40 to 19.28. Nothing about the aggregation changed. What changed
was the *shape* of the replaced member's errors.

The member it replaced was diffusely wrong: asked for a reference class
that did not exist, it produced a plausible middling number most of the
time. A median ignores that for free, which is why the median kept winning.

The new member was a check on whether the event had already happened. That
one is usually silent and occasionally decisive - when it fires it is near
certain and near right. **With six members the median is the average of the
third and fourth, so a member that sits at an extreme is excluded by
construction, whether it is extreme because it is wrong or extreme because
it is certain.** The mean keeps a sixth of it. On a board where it fired,
that sixth was worth more than the noise it let in.

So the choice of aggregator is not a property of the population's average
quality, which is how it is usually framed. It is a property of *how the
bad members fail*:

- members that are **diffusely wrong** - noisy around the truth, or
  confabulating a middling answer - argue for the median
- members that are **rarely right and decisive** - silent, then certain -
  argue for the mean, or for routing round the aggregator entirely and
  letting that member override when it fires

A population containing both wants neither aggregate. It wants the
decisive member consulted first and the rest averaged robustly behind it,
which is a different architecture and not a parameter choice.

The general warning: **an aggregation rule validated on one member set is
not validated for the population, only for that set.** Swapping a member is
enough to invert it, so a lineage that changes members and keeps the
aggregator has silently stopped testing what it thinks it tested.

### Two aggregators with different asymptotics look like one noisy result

Earlier sections here recorded that the median beat the mean, then that it
sometimes did not, and treated the inconsistency as a property of the
members. Part of it was. Most of it was not.

Scored over every subset of nine members on one board:

| k members | median of subsets | mean of subsets |
|---|---|---|
| 1 | 19.49 | 19.49 |
| 4 | 16.75 | 17.81 |
| 6 | 15.81 | 17.58 |
| 9 | **13.55** | 17.42 |

**The mean saturates and the median does not.** Past four members the mean
gains 0.4 in total; the median gains 3.2 and is still falling.

So the two rules are not near-equivalents that swap places under noise.
They have different limits, and the gap between them is a function of the
member count: 1.38 apart at six members, 3.87 at nine. **Every single-board
comparison of two aggregators is silently a measurement of the population
size it happened to run at**, and comparing two such measurements taken at
different sizes produces a contradiction that looks like noise and is not.

The practical rules:

- **Compare aggregators as curves over k, never as two numbers.** One run
  gives the whole curve if every member's output is logged, so there is no
  excuse for the two-number version.
- **A conclusion that returns to members are diminishing is conditional on
  the aggregator that measured it.** This population concluded exactly that
  and went hunting elsewhere for four generations. It was true under the
  mean and false under the median, and the cheapest available gain was in
  the member count the whole time.
- **When an aggregator changes, every prior finding about member count is
  void**, and vice versa. They are not independent knobs, and a lineage
  that turns one while holding conclusions from the other is reading a
  stale map.

### A member that can be outvoted is safe; the same member with authority is not

An operator will eventually notice that one member of an aggregate is being
suppressed and propose promoting it - letting it decide directly when it is
confident, instead of being averaged away. The argument is always the same
and always sounds right: *this member is looking something up while the
others are guessing, and being outvoted about a fact by six guesses is a
bug.*

Measured, that argument was wrong, and the way it was wrong is worth
keeping.

The member was a check on whether an event had already happened. Given
authority, it fired on **20% of tasks** and its mean error where it fired
was **41.4 points against 16.7 for the aggregate it replaced.** It asserted
that events had already occurred on tasks the venue priced at one cent. The
output format was three fixed words, the prompt said do not forecast, and
the prompt said uncertainty means abstain. None of it helped, and the rigid
format made things worse: a fabricated certificate is indistinguishable
from a real one at the point of use, which is exactly what a format is for.

**The suppression was the safety mechanism.** A median over six members
excludes extremes by construction, so a member that is confidently wrong a
fifth of the time costs almost nothing inside the aggregate and is ruinous
outside it. The operator saw the exclusion and read it as lost information.
It was purchased protection.

So the rule: **before promoting a suppressed member, measure its error
conditional on firing, not its error overall.** Those are different numbers
and only the first one matters, because firing is the only time promotion
changes anything. A member whose overall error looks tolerable can be
carrying all of it in the cases where it would act.

And the corollary that costs the most to learn late: **a strict output
format does not make a model more truthful, it makes its errors better
disguised.** Free text hedges visibly. A schema does not have a field for
doubt.

### Every aggregator saturates; the useful number is where

The previous section recorded that the mean saturates and the median does
not. Half right, and the correction matters more than the original.

Measured over subsets on two boards, the mean is flat from four members
onward - the same point on both, so it belongs to the aggregator rather
than to a set of members. The median keeps paying much longer and then
stops too, at **ten to twelve**. The earlier reading came from a curve that
ran out at nine, one member short of its own knee, and a curve that has not
turned yet looks exactly like a curve that never will.

So the general shape: **an aggregator has a saturation point, it is a
property of the rule, and the only interesting question about two
aggregators is where each one turns.** "Does averaging help" is not a
question with an answer. "Averaging helps to four, medians to twelve" is.

Two practical consequences.

**Size the run past where you expect the knee.** A curve measured up to
exactly the point you can afford will always look like it is still rising,
and you will conclude that more is better every time. This population did,
for one generation, and spent a run finding out.

**A flat tail is not a failed experiment.** Locating a knee is the result.
It closed a lever permanently - one run instead of three generations of
buying members one at a time - and it did it for the price of one board,
because the whole curve came free from logged component outputs.

That last part is now the strongest argument for logging every member's
output on every run: it has twice produced the finding that outranked the
run's own headline number.

### Check where the correlation is before paying to decorrelate

An aggregate that has stopped improving is limited by how alike its members
are, so the natural move is to make them less alike. The expensive way to
do that is to diversify the model. It is also usually the wrong one.

Measured: nine members read by three model families - three different labs,
three different training sets - disagreed with each other **0.106**, while
the same model reading three different inputs disagreed with itself 0.089
to 0.117. The between-family number sat inside the within-family range.
Three labs bought no diversity whatsoever.

The reason generalises past this population. Each member was conditioned on
its own retrieved evidence and largely transcribed it. **When members are
conditioned on different inputs, the inputs supply nearly all the variance
and the model supplies almost none.** Swapping models decorrelates members
that differ only in sampling; it does nothing for members that already
differ in what they were shown.

So before spending on diversity:

- **Measure between-source spread against within-source spread.** It is one
  number from data you already have if member outputs are logged, and it
  says whether the axis you are about to buy has any room in it.
- **Diversify the axis that carries the variance.** Here that was
  retrieval, not inference, and the population had spent twelve generations
  varying the wrong one without noticing, because the model was a constant
  nobody had written down as a choice.
- **An unnamed constant is not a validated one.** Worth auditing what a
  population has never varied. Sometimes, as here, the answer is that it
  never mattered - which is itself worth knowing cheaply rather than
  assuming expensively in either direction.
