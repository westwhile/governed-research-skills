# Architecture

## Control plane

`research-workflow-router` is the sole implicit control router. It classifies a
request, selects one explicit specialist or the smallest safe chain, and does
not execute child work itself.

Domain routers are explicit delegation layers:

- `nature-research-router` for multi-stage academic publishing workflows;
- `quant-workflow-router` for quantitative research workflows;
- `stats-experiment-router` for experiment design and statistical workflows.

## Specialist layer

The bundled specialist layer contains literature synthesis, academic search,
paper reading, a literature-monitoring contract, and proposal-first research
writing. A router may name optional specialists that are not included in this
baseline. Availability must be resolved by the host; absence fails closed.

## Evaluation envelope

`payload/runtime-receiver/AGENTS.md` is a frozen evaluation envelope. It disables
external actions so that routing and output contracts can be evaluated against
the receiver without unrelated capabilities. It is not a global installation
profile.

## Trust boundary

The release payload contains declarative Skill instructions and selected local
helpers. It does not itself grant network, shell, filesystem, account, Manager,
or trading permissions. Those remain host-controlled capabilities requiring
separate authorization.
