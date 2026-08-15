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

## Report the paired difference, not only the score

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

## Reporting

Every claim carries the board it was measured on, the number, its interval,
the noise band, the constant, and the number of independent clusters, not
the number of tasks, where tasks are correlated within a cluster. Numbers
enter a record as pasted output from the run that produced them.

Absolute scores from different boards are never compared. Only paired
contrasts on the same board are.
