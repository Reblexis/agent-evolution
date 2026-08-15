# Agent evolution

A way to make an AI agent measurably better at something: keep a population
of complete, standalone agents, breed new ones with operators that start
from a diagnosis rather than a guess, freeze every agent the moment it has a
score, and judge them all against ground truth with the controls that stop
you fooling yourself.

- [`docs/practice.md`](docs/practice.md), the governing doc.
- [`implementation/`](implementation/), the implementation of that
  description: [`population.md`](implementation/population.md) (what an
  agent is on disk), [`evolution.md`](implementation/evolution.md) (the
  operators, selection, where proposals come from),
  [`metric.md`](implementation/metric.md) (what a project must supply and
  what makes a score worth optimising),
  [`researching.md`](implementation/researching.md) (the rules a research
  agent works under), [`operating.md`](implementation/operating.md)
  (dispatch, the record, asks, the rendering).
- [`skill/`](skill/SKILL.md), an installable skill for AI agents: copy or
  symlink it into an agent's skills directory.
- [`tools/`](tools/), project-agnostic: `check-tree` validates a population,
  `new-node` scaffolds an agent, `render-tree` draws the page.
- [`index.html`](index.html), the human-readable representation of `./docs`.

## Using it in a project

Drop a `.agent-evolution.json` at the project root naming where its
population, scores and asks live, then run the tools against it:

```json
{
  "name": "trader-agent",
  "population": "traders",
  "scores": "state/bench",
  "asks": "asks",
  "metric": {"name": "points from the outcome", "lowerIsBetter": true}
}
```

## License

[MIT](LICENSE)

---

This repo uses [ddd-practice](https://github.com/Reblexis/ddd-practice):
docs are the source of truth, everything else is derived. `./docs` holds one
governing document, [`practice.md`](docs/practice.md), elaborated by
`./implementation`. The human-readable representation is
[`index.html`](index.html) at the repo root.
