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
