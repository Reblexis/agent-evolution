# Metric

What a project must supply so that a population can be evolved against
something, and the properties that make that something worth evolving
against.

## The contract

A project supplies four things.

**A board.** A frozen set of tasks, with an identifier, a freeze timestamp,
and enough content for an agent to attempt each task. Frozen means the file
does not change; a new selection is a new board, and old boards are kept.

**A deciding score.** A function from an agent's outputs on a board to one
number, with an interval. Lower or higher must be stated once and never
flipped.

**Controls.** At minimum the two mandatory ones below, implemented so any
mission can run them without inventing them.

**A runner.** Something that takes an agent and a board, produces the
per-task table, and writes the score. Agents are never scored by hand.

## The deciding score is measured against ground truth

The score that decides promotions is measured against what actually
happened, not against another estimate of what will happen.

A score measured against an estimate, another system's answer, a market
price, a stronger model's opinion, measures agreement with that estimator.
A population evolved against it converges on imitating the estimator,
including where the estimator is wrong, and the better the population gets
at the metric the less the metric distinguishes it from the thing it is
imitating. This is not hypothetical: the first project to run this practice
spent two campaigns discovering that its score's target was better than its
agents at the thing both were supposed to be doing, and that two of its
correct improvements scored as regressions.

A project may keep a cheap proxy score as a screen, and many should: proxies
run in minutes where ground truth takes weeks. When it does, the proxy is
labelled as a screen everywhere it appears, and it never decides a
promotion.

## The board must not contain its own answers

If a task's answer already exists in the world when an agent attempts it, an
agent that searches will find it, and the score measures retrieval of
answers rather than production of them. A board of historical tasks is
therefore only valid for agents that cannot search, and the runner must know
which agents those are.

The general form: freeze tasks whose answers do not yet exist, and score
them when they resolve. This costs calendar time and is the price of a score
that means anything. A project that cannot wait uses the proxy screen for
iteration and the true score for promotion.

Related and easy to miss: a task whose answer became known between the
freeze and the run is contaminated even if the board looks fine. Boards
record when each task's underlying event occurs, and the runner excludes
tasks whose event predates the run.

## A board is a round, not a standing exam

The world moves while a board sits. An agent that answers a week after the
board was frozen is not smarter than one that answered the same hour: it
simply knows more, and it is being scored against a target that has since
stopped describing anything. Both effects flatter the latecomer, and
neither is skill.

So a board carries a deadline as well as a freeze time, and agents compared
against each other answer inside it. After the deadline the board is
closed: a new agent means a new board, and the agents worth comparing it
against are re-run on that board. Scoring an agent on a closed board is
allowed but marked, and a marked score never decides a promotion.

How long a window can be depends on the venue and is measurable rather than
a matter of opinion: sample the board and see how far its prices have moved
since the freeze. On the first board here, an hour after freezing, the
median market had not moved at all and the largest move was half a point.
Every run records that measurement, so a score taken against a drifted
board says so on its face.

The score measured against ground truth does not decay this way - what
happened is what happened - but the fairness problem remains, because a
later agent forecasts with more of the future already visible. The deadline
is what makes the comparison mean something, on both scores.

## The two mandatory controls

**The population's own noise.** Before a threshold is declared, run the
incumbent against itself on that board, two independent runs of identical
code, and measure the spread of the difference. A threshold inside that
spread cannot be met by a real effect, so declaring one guarantees either a
null or a false positive. The band is measured on the board in question:
bands do not transfer between boards, and importing one is a common way to
buy a result that was never buyable.

**The constant.** Whatever the simplest rule is that ignores the input, the
same answer every time, the most common outcome, doing nothing, a claim
must beat it. Most apparent skill on a skewed population is that population's
marginal wearing a mechanism's name. The constant is computed on the same
tasks with the same scoring, and reported next to the claim.

Projects add their own controls. Two that generalise: a scale-matched
version of the candidate that carries no information, which separates
information from movement; and a version of the candidate given deliberately
wrong inputs, which separates using the input from reacting to its presence.

## Reading a result

Four ways a number here can be true and mean nothing. Each was bought with
a mistake on the first project to run this practice, and each is stated
with the measurement that bought it, because the general form of the rule
is easy to nod at and hard to apply against a result you like.

They come in the order they bite: what the score is really ranking, whether
the difference is bigger than the noise, whether the test could have seen
the effect at all, whether it survives a second board, and what to do when
it does not.

### Report the paired difference, not only the score

A whole-board score mixes two things a project usually wants to keep
apart: how well an agent does the task, and how often it manages to do it
at all. Where an unattempted task is scored at a penalty - and it should be,
or skipping the hard ones pays - the second can dominate the first.

Measured on the first project to run this practice: three agents in one
lineage scored 18.49, 19.69 and 20.50, which reads as a ranking. Paired
task by task on the rows each pair both attempted, the differences were
+0.50 [-2.45, +3.57] and -0.20 [-3.65, +2.80]. They were the same agent for
forecasting purposes; every point between them was coverage. On that board
a blank cost about 30 points where a bad answer cost about 17.

So a claim carries two numbers. The whole-board score, which ranks by
reliability and is a real thing to be good at. And the paired difference on
shared tasks, which is the only one that speaks to quality. Reporting the
first alone is how a retry loop gets promoted for wisdom - which is exactly
what nearly happened.

The runner should compute the paired comparison against an agent's parents
automatically. Leaving it to whoever remembers to check means it gets
checked when the result is surprising and skipped when it is welcome.

### A difference smaller than two runs of the same agent is not a difference

The mandatory noise control above says to measure the population's own
spread before declaring a threshold. This is what it looks like when a
project does not.

On the first project, two agents were compared across two boards and gave
+2.77 [+0.71, +4.98] and -1.66 [-3.58, +0.17]. They then turned out to be
the same agent: the only difference between them fired on zero tasks. So
those two numbers are the run-to-run spread, and one of them had an
interval excluding zero.

A later direct twin - the same agent, the same board, run twice - gave
0.465, and per-task disagreement with a median of 4 points and a 90th
percentile of 27. With three more pairs the six observations were +2.77,
-1.66, -0.47, +0.70, +2.42, +0.58: mean +0.72, standard deviation **1.68**,
and the estimate moved only 1.88 to 1.68 on the sixth, which is where a
project can start trusting it.

Three figures were published before that one, each stated as if it were the
answer: about three points from three observations, then 0.465 from a
single twin, then 1.88 from five. The first was too confident, the second
too generous, the third close. **Expect three or four goes**, and say which
one you are quoting.

Two things follow. **A bootstrap interval is not a noise band**: it
resamples tasks within one pair of runs and cannot see how much the answer
depends on the run, because it only has one. And **one twin is one draw**:
a band needs several, and at the price of a run they are the cheapest
measurement a project can buy.

Until a project has them, the honest form of every small result is "smaller
than we can measure".

### Say what your test could have seen, before you run it

A null result means one of two things and they are not close: *no effect
exists*, or *this test could not have found one*. Only the first is a
finding, and telling them apart takes one line of arithmetic done in
advance.

Worked example. An agent was built to fetch a fact for tasks of a
particular shape, which are about 15% of a board. Its record said, before
it ran, that only 18 tasks would qualify on one board, that per-task noise
is about 21.8 points, and therefore that **an effect smaller than 10 points
would be invisible**. Pooled over two boards it predicted an interval near
3.3 and it came out at 4.7.

The result was -0.65 with an interval spanning ten points. Its record also
carried a kill condition: if this shows nothing, the whole line of work is
finished. **The condition did not fire, and refusing to fire it was the
right call**, because an interval ten points wide cannot rule out the two
to five point effects the project cares about. Declaring the line dead
would have been a real conclusion drawn from no evidence.

Writing the detectable effect down in advance is what makes that call
available. Afterwards, every null is tempting to read as a refutation,
especially a null on something expensive.

The arithmetic is: per-task noise divided by the square root of the number
of tasks the mechanism will actually touch. Not the board size - the
**touched** size, which for anything conditional is much smaller and is the
number that decides whether the experiment is worth running at all.

### Give every open question a closing date

The arithmetic that says what a test could see also says *when* it will be
able to see it, and that turns a backlog of unresolved questions into a
schedule.

The detectable effect on a slice is roughly twice the per-task noise over
the square root of the slice's size. Slices grow by pooling boards, not by
enlarging one - a bigger board runs out of supply, and a project running
rounds gets another board for free every cycle. So for each open question:
take the effect being looked for, the slice it lives in, how fast that
slice grows per round, and solve for the round at which the two cross.

Worked, on the first project. A mechanism worth about 3.3 points on the
"likely" slice had 90 such tasks and needed 4.60 to see it. The next board
took it to 151 and 3.55 - still short. One more day of two boards took it
to 261 and 2.70, which settles it. **That was computed before the board ran
and it changed how the result was read**: a number arriving on a board
known in advance to be underpowered cannot be promoted, however it looks.

Three things follow.

**A question with a date is not a question that needs work.** The first
project ended a night with 88 agents and four open questions, every one of
which closes within four days on boards that were going to be frozen
anyway. Building an 89th agent would have added a question, not answered
one.

**A date exposes a question that will never close.** If the slice does not
grow - a mechanism firing on 4% of a board, a venue that supplies twelve
qualifying tasks - the arithmetic says so, and the honest response is to
change the mechanism or drop it rather than run it monthly forever.

**And it removes the temptation to read an underpowered result.** Knowing
on Tuesday that Thursday settles it is what makes Tuesday's number easy to
leave alone.

### One board is not enough, whatever the interval says

A bootstrap interval measures spread *within* a board. It says nothing
about spread *between* boards, and those are not the same size.

Measured, on the first project to run this practice. An agent was compared
against its parent on one board and came out worse by 2.77 points with an
interval of [+0.71, +4.98] - excluding zero, which is what a project
normally treats as a result. The comparison was repeated on a second board
frozen a day later, drawn from the same venues by the same rules, and came
out better by 1.66 [-3.58, +0.17]. On the first board the mechanism moved
the answer the wrong way on 36 of the 58 tasks it touched; on the second it
moved it the right way on 42 of 72.

The mechanism did not change. The board did.

So: **an effect measured on one board is a hypothesis, and the interval
around it is not protection.** A claim that decides anything is measured on
two boards, and the two agree in direction. A project running rounds
already has a second board for free - the next one - so this costs
patience rather than money.

The corollary is worth stating plainly, because it is the expensive half. A
finding that has not been repeated should be written down as unrepeated,
even when it is well argued and its interval looks clean, and especially
when a mechanism has been reasoned out to explain it. A convincing
explanation of a one-board effect is the most persuasive thing a project
produces and the least reliable.

### When an aggregate reverses, look at the slices before believing anything

Two comparisons in the first project reversed between boards. They look
identical in the summary table and they are not the same thing at all.

**One was composition.** An agent that pulls its answers toward a constant
scored better than its base on the first board and worse on the second.
Sliced by how likely the task was, the pattern is the same on both boards
to within a point: the pull helps in the middle and hurts at both extremes.
What changed was the board - one had 14 extreme-low tasks and the other had
35 - so the same stable mechanism averaged out to opposite signs. The
mechanism was understood; the aggregate was just a weighted average over a
mix that varies.

**One was the mechanism.** An agent that adds a computed arithmetic line
was worse than its parent in *every* slice on the first board and better in
*every* slice on the second. Nothing about composition explains that. The
thing itself behaved differently, and there is no finding to keep.

So the rule is not "aggregates reverse, distrust them". It is:

- aggregate flips, slices agree -> a real mechanism and a mix effect. Keep
  the mechanism, describe it by slice, and stop quoting the aggregate.
- aggregate flips, slices flip too -> nothing is established. Withdraw it.

The second case usually means something outside the agent moved between
runs. Which is only diagnosable if the agent recorded what it did: the
arithmetic agent fetches live data and writes down nothing about whether
the fetch worked, so whether its line was present on both runs at all
cannot now be established. **Any mechanism that fires conditionally must
log its firing, or a reversal like this is permanently uninterpretable.**

## Reporting

Every claim carries the board it was measured on, the number, its interval,
the noise band, the constant, and the number of independent clusters, not
the number of tasks, where tasks are correlated within a cluster. Numbers
enter a record as pasted output from the run that produced them.

Absolute scores from different boards are never compared. Only paired
contrasts on the same board are.

### A band is defined by one variable, so it lies about the other

Score tables in this practice are usually cut into bands of the thing being
compared against - price bands, difficulty bands, size bands. Every one of
those tables is a regression-to-the-mean trap, and the trap is not subtle:
it produces large, orderly, entirely fake gradients.

Binning 205 markets by venue price and reading off what the agents said:

| price band | mean price | what the agents said |
|---|---|---|
| 0-5 | 2.3 | 14.9 |
| 5-20 | 11.9 | 24.8 |
| 50-80 | 63.7 | 43.1 |
| 80-101 | 91.9 | 69.7 |

That reads as a population badly compressed toward the middle, and it is
the kind of table that gets a recalibration layer built for it. Bin the
same data the other way round, by what the agents said, and the venue looks
compressed instead: they say 2.8 where the price is 5.1, and 87.0 where it
is 84.8. Both slopes are below one - 0.55 and 0.83 - because two noisy
quantities that disagree always look mutually compressed, whichever you
condition on.

**The check is one line: bin by the other variable.** If the picture
mirrors, the gradient is regression to the mean and there is nothing to
fix. Here the direct test agreed - stretching every answer away from the
middle, sweeping the coefficient from 1.0 to 4.0, improved not one agent
out of eleven.

Two related failures from the same night, both of which produced a real
number that meant nothing:

- **A slice that differs in composition.** Markets whose question names a
  deadline sat 6.48 points higher above the venue than markets that did
  not, which looks like agents ignoring the window. They also had a mean
  price of 29.3 against 46.4. Matched band by band the difference is -0.50
  [-4.74, +3.74]. The whole effect was the price mix.
- **An output transform imitating a mechanism.** An agent that answered 6.5
  points lower than its parent everywhere appeared to be better on cheap
  markets and worse on expensive ones. Subtracting 6.5 from the parent's
  own answers reproduced the expensive-market half exactly and the cheap
  half not at all, which is how the one real effect was separated from the
  arithmetic.

The general form: **before believing a slice, construct the dumbest thing
that would produce the same table, and run it.** A shift, a stretch, a
reweighting of the mix. It costs nothing because no agent runs.

### Pool by the unit of independence, not by the observation

Boards frozen at different times from the same venues overlap. Five boards
in this project held 705 agent-market observations and 427 distinct
markets. Pooling them raw treats one market that appeared on three boards
as three independent facts, and shrinks the interval by a third around
nothing.

A market that ran more than once is repeated measurement of one quantity.
Average the runs into one observation: the noise reduction is kept and the
market is counted once. An accumulation strategy is the case where this
matters most, because the double counting grows with the pile.

### A slice chosen because the failure is visible in it has a free direction

The natural way to study a failure cheaply is to take the markets where it
happens. That slice is then, by construction, one where one direction of
error costs almost nothing - and every estimator that leans that way will
look good on it.

Seventy tasks were picked because a research failure showed there. They
were all priced under 0.15. On them:

| | score |
|---|---|
| answering zero every time | **6.07** |
| the best combiner tried | 8.30 |
| a single draw | 13.81 |

The combiner beat a flat-shift null - 8.30 against a best-shift 9.20 - and
was still meaningless, because the null was not extreme enough. The
constant was.

**So the null for a biased-looking estimator is not a shift. It is the
constant that the slice rewards.** Answer zero, answer one, answer the
slice's own mean - whichever direction is free there. If the estimator
cannot beat that, the slice cannot judge it.

Dispersion survives this and central tendency does not. Two runs of the
same thing differ by the same spread whatever shift they share, so noise
decompositions measured on a biased slice are still valid. "Which of these
two is better" measured on one is not, unless the two have the same mean
output - and that has to be checked and reported, not assumed.

### A board of already-solved tasks is a floor test, not a ranking

Waiting for tasks to resolve is often the rate limit on a research loop, so
the obvious shortcut is to score agents on tasks that have already
finished, choosing tasks whose answers postdate the model's training data
so it cannot know them. That works, and it works for less than it looks.

On one project it produced nineteen agents scored in an afternoon against
300 resolved tasks, at $2.54, replacing a three-week wait. Then the check
for having read rather than predicted the answer - comparing each agent
against the reference price on the tasks the reference itself was unsure
about - flagged three agents. Sorted by that check, **the flagged three
were the three most capable agents on the board, the next three were
borderline, and the clean agents were the weakest.**

Two of the three had been the day's headline results in the hour before
they were checked.

**Capability and contamination are the same axis.** A stronger model
recalls more. A model given room to reason recalls more - one agent's
parent, with identical search, was clean, and the child differed only in
being allowed to think out loud. A more capable search finds more. Every
axis along which an agent gets better is an axis along which it gets better
at finding an answer that already exists.

So the instrument can say **whether an agent beats a constant** and cannot
say **which of two good agents is better**, because the better one is the
more likely to be cheating. Use it for the floor, for negative results, and
for anything measured below the contamination line. Rank the top of the
table on tasks that resolve after the agent runs, and accept that this is
the slow measurement the shortcut was meant to replace.

**The check itself is worth building whatever else you do.** It is: on the
tasks the reference was uncertain about, does the agent beat the reference?
Nothing honest does. It caught two results that would otherwise have been
published, and its false-negative direction is safe - a contaminated agent
that fails to exploit its knowledge is merely uninformative.

## A board nobody current ran on cannot colour the picture

The page picks one reference board, because scores do not transfer between
boards and colouring each agent by whichever board it last ran on puts two
different exams on one scale. Given a choice it prefers a board scored
against outcomes over one scored against a screen, and that preference is
right: the two rank differently, and the screen has inverted a ranking.

The preference was written with no coverage condition, and a two-agent
historical board then beat the live nine-agent one. Every current agent
rendered as **not scored yet** while the page cited a board that had been
retired for being a floor test. The numbers were all sitting in the loader;
only the choice of exam was wrong, so nothing looked broken - the page just
quietly said the population had never been measured.

So the rule now needs both: an outcome board wins **only if it covers at
least as many agents as the best screen board does.** Quality of the
instrument does not override whether it was pointed at anybody.

The general form, which is why this sits with the other metric laws: **a
selection rule that ranks instruments by quality alone will eventually pick
an excellent measurement of the wrong population.** Coverage is not a
tiebreak under quality, it is a precondition for quality mattering at all.

## A starved run scores like a bad idea

The worst failure in a scored population is not a crash. A crash is
labelled. It is the run that completes, reports a number, and had no way of
succeeding.

An overnight chain died on its fifth run because the agent's prepaid token
credit ran out. The gate answered 402 to every call. Each way of looking
caught the error - correctly, since a single failed search should not lose
a whole market - returned nothing, and the agent scored **1 market out of
50 in six seconds for a tenth of a cent**. Two agents were within one
sentence of being written off as bad ideas. The idea was untested.

Robust error handling is what made it silent. Every layer did the right
local thing and the aggregate lied.

**Three defences, in order of how much they are worth.**

1. **The runner owns the preconditions, not the agent.** Funding, keys,
   quota - anything a run needs and an agent should never think about -
   is checked and repaired by the thing that brackets the run. An agent
   that has to remember to top up its own account is one that will
   eventually forget, and every new agent forgets by default.
2. **Report the denominator, always.** "answered 1/50" was in the output
   and it is the only reason this was caught. A score without a count of
   what it was computed over cannot be sanity-checked by a reader who is
   moving fast, and the reader is always moving fast at 1am.
3. **Refuse to score below a floor of coverage.** A run that answered a
   twentieth of its board should not produce a number at all. A number,
   once printed, gets compared to other numbers.

The generalisation: **check that a result was *possible* before asking
whether it is *good*.** Cost per market, wall clock and answered count all
collapse together when a run is starved, and any one of them read before
the score would have caught it in a second.

## Tasks resolve in order of how easy they were

A deciding score that arrives over time - outcomes, ground truth, whatever
settles later - is usually treated as a matter of patience. Wait longer,
get more labels, rank sooner.

The labels do not arrive in a random order. **Easy tasks settle first**,
because being obvious and being quick are the same property in most
domains. Of the first eleven tasks to resolve on one population's boards,
ten had been priced by the venue below 0.10 and none fell in the middle
band at all.

So the early deciding score is computed almost entirely on tasks nobody
disagreed about, and it ranks agents by whether they produce confident
answers on obvious questions - which every competent agent does. It looks
like the real metric arriving early. It is a different metric that will be
replaced by the real one later, quietly, without changing its name.

Two rules follow.

**Gate the ranking on the informative subset, not the total.** Counting
resolutions is the wrong denominator; count resolutions *in the band where
agents disagree*. One population requires fifteen such tasks before it will
rank at all, and reports how many it has, which is what stops a reader
mistaking eleven easy labels for progress.

**Date it.** Counting how many uncertain tasks close in each of the next
few weeks turns "it matures over time" into a specific week, and a specific
week is actionable: it says stop checking until then. "Over time" invites a
daily look at a number that cannot yet mean anything, and a number looked
at daily eventually gets believed.

## Regression toward the middle is not a bias you can correct

A tempting table. Bucket predictions by the *true* value and compare:

| true value | mean estimate | estimate minus truth |
|---|---|---|
| 0.00-0.05 | 0.234 | **+0.213** |
| 0.05-0.20 | 0.302 | +0.185 |
| 0.20-0.50 | 0.409 | +0.067 |
| 0.50-0.80 | 0.475 | -0.175 |
| 0.80-1.01 | 0.684 | **-0.236** |

It reads as a large, systematic, obviously fixable defect: the estimator is
under-confident everywhere, so stretch it away from the middle and collect
several points for free. Overall bias was +0.020, so it is not optimism or
pessimism, just compression.

**Measured, the correction is worth nothing and usually costs.** The best
stretch factor per board came out 0.9, 1.0, 1.0, 1.1, 1.2, 1.6, 1.7 - no
transfer at all - and on the two largest boards it was exactly 1.0. A fixed
stretch chosen from the table made every large board worse, 15.32 to 16.92
on one.

**The table is an artifact of how it was built.** Conditioning on the truth
and averaging the estimates will show regression toward the middle for any
estimator that is not perfect, and the amount of regression is a measure of
how uncertain it is, not of how biased it is. Compressing toward the middle
is *correct* behaviour under uncertainty. Undoing it requires knowing which
bucket a case is in, which is the thing being estimated.

The general rule: **a bias measured by conditioning on the answer cannot be
corrected without the answer.** Before acting on any per-bucket table, ask
whether the bucketing variable is available at prediction time. If it is
not, the pattern is real, describes the estimator honestly, and is not a
lever.

The safe version of the same question - bucket by something the agent
*can* see (its own confidence, its members' spread, the question type) and
look for bias there. That table is actionable because the agent can
condition on it too.

## A baseline you can reconstruct is a baseline you should not run

Comparing a child to its parent on the same board is the obvious control,
and for a large class of changes it is strictly worse than the free
alternative - as well as costing real money. On one project it was 29% of a
night's spend.

**If the child logs the outputs of its parts, the parent's answer is often
arithmetic over rows the run already produced.** A child that adds a
component, removes one, or combines them differently contains its parent:
same tasks, same retrieved evidence, same component outputs, differing only
in the thing under test. Re-running the parent reproduces that comparison
with fresh randomness added - the same measurement plus a sample of the
noise band.

Both were run side by side on one question. Within-run, the change was
worth +0.64; cross-run, it was worth -0.25. The straddle is what settled
the question, and the cross-run half contributed only the reversal.

**The test**: is the baseline's behaviour a function of data the treatment
logs? Combining rules, component counts and component identity all are.
Prompts, retrieval, architecture and model usually are not, because they
change what the components see.

Two consequences worth keeping:

- **Log component outputs even when nothing needs them yet.** It converts
  a whole class of future baselines from purchases into arithmetic, and it
  is the same habit that produces subset curves and leave-one-out tables
  for free.
- **A reconstructed baseline is the better measurement, not a cheaper
  approximation of it.** It holds constant everything the re-run
  re-randomises. Treating it as second-best gets the preference exactly
  backwards.

## Find the slices where a constant beats your agent

One pooled score is the average of every regime the agent operates in, and
an agent can be excellent on most of them while being **worse than a
constant** on others. The average hides it perfectly, because the good
slices pay for the bad ones and the total still improves generation over
generation.

Measured on one population that had run fourteen generations and thought
it knew where its error was:

| slice | agent | best constant | edge |
|---|---|---|---|
| venue A | 10.01 | 1.98 | **-8.02** |
| venue B | 18.11 | 30.01 | +11.91 |

Every point of measured skill was on one venue. On the other the agent was
eight points worse than saying the same number every time, and had been
since the population was created.

**The diagnostic is one pass and it should be standard.** Partition the
scored tasks by anything observable *at prediction time* - source, task
type, a regex over the text, the agent's own internal disagreement - and
for each slice compute the agent's score **and the best constant on that
slice**. Any slice where the constant wins is a slice the agent should not
be answering with its own judgement.

Two kinds of fix, and both are calibration rather than skill:

- **The agent is systematically mis-scaled on the slice.** It hedges toward
  the middle while that slice is nearly all extremes. Scale it, conditional
  on the observable.
- **The agent has no information on the slice at all** - tasks about
  private lives, fiction, in-jokes, anything with no record to retrieve.
  Answer the slice's base rate and skip the retrieval entirely, which saves
  the money as well.

Three cautions, learned the same night:

- **The partition must be observable at prediction time.** Slicing by the
  true answer produces a large, convincing, uncorrectable pattern - see the
  regression section above.
- **Validate leave-one-slice-out**, or the correction is fitted to the
  boards that revealed it.
- **State plainly that it is not edge.** Beating your own previous score by
  being less wrong where you know nothing is worth having and is not the
  same as discriminating better between tasks. Only the second one pays,
  and a score that improves for the first reason will be misread as the
  second by whoever reads it next - including you.

## A fresh board drawn the same way is not a fresh board

Held-out evaluation assumes the held-out set is a different sample. That
assumption is about the *sampler*, not about the timestamp on the file, and
it fails quietly in a very ordinary setup:

- a fixed random seed, which is normally good practice and is why nobody
  looks at it
- a pool of eligible tasks that changes slowly, which is normally fine
- a sampler that therefore returns nearly the same tasks each time

One project froze eight boards over a night and they overlapped each other
**52% to 100%** - two pairs identical, 25 tasks present on all eight, 16
tasks unique to any board. Every held-out result from that night was
measured on tasks it had been fitted on.

**It cannot be seen from one board.** Each was fifty tasks with a sensible
spread and a plausible score. Boards are inputs, and an input that has
never been wrong is not audited.

Three defences:

- **Seed from the sample's own identity** - its name, its timestamp - not
  from a constant. That keeps a named sample exactly reproducible, which is
  what the fixed seed was for, while making two samples genuinely
  different.
- **Print the overlap with the previous sample at build time.** One line.
  A sample is only suspicious next to another sample, so the comparison has
  to be automatic or it never happens.
- **Treat "held out" as a claim requiring evidence**, like any other. The
  evidence is the overlap number, and before that number exists the phrase
  is an assumption wearing the clothes of a control.

## When two instruments disagree, one of them is broken

This is the lesson that would have saved the night above, and it was
available for hours before anyone acted on it.

Two ways of measuring the same effect were in use: a within-run comparison
holding tasks and intermediate outputs fixed, and a cross-board comparison
re-running a baseline separately. They disagreed repeatedly - one said a
change was worth +0.64, the other said -0.25; one said a member helped, the
other said it hurt - and each disagreement was written off as noise,
because a noisy benchmark is the expected explanation and there was a
measured noise band to point at.

**The disagreement was not noise. One instrument was broken**, and the
pattern of which one won was the evidence: the within-run measurements were
right every time. A genuinely noisy pair disagrees *in both directions* and
neither wins consistently.

So: **when two measurements of the same thing disagree more than once,
count who wins.** If it is not close to even, stop treating it as variance
and go and find out why. Noise is symmetric; a broken instrument has a
direction, and the direction is the tell.
