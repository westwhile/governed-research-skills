---
name: research-workflow-router
description: Route natural-language research, quant, and statistics requests to one explicit specialist or the smallest safe chain; act as the sole implicit control Router and delegate domain workflows.
---

# Research Workflow Router

Route research work and cross-domain handoffs without loading any Skill group.
Act only as the sole implicit control layer; do not execute child work or
expand permissions.

## Run the decision kernel first

Initialize the routing fields before reasoning:

```text
route_type:
delegated_router:
recommended_skills_ordered: []
authorization_gates: []
capability_gaps: []
```

Separate route topology from execution readiness before choosing any token:

- Use `route_type`, `delegated_router`, and `recommended_skills_ordered` only to
  describe ownership topology.
- Use `required_input_artifacts`, `authorization_gates`, and `evidence_limit`
  to describe whether execution may start. When a host response contract also
  has `execution_verdict` or `evidence_grade`, put HOLD and evidence
  limitations there. For a `domain_delegate` to an explicit-only Router,
  `execution_verdict` must remain `HOLD` until that exact Router invocation is
  present; `planning_only` never clears the invocation gate.
- Freeze a valid ownership topology before evaluating ordinary missing inputs
  or an explicit-only child's invocation gate. Those readiness gaps may block
  execution, but they must not rewrite the frozen topology.
- Do not use `authorization_hold` as a synonym for a HOLD verdict. Reserve that
  route for a request whose operation is itself authorization-controlled, such
  as an uninvoked recurring pipeline or gated acquisition requested now.

Keep fail-closed control separate from the execution-verdict token:

| Condition | Route effect | Execution verdict |
|---|---|---|
| Missing required owner | `capability_gap` | `HOLD` |
| Missing ordinary input or authorization | preserve the frozen topology | `HOLD` |
| Evidence or contract integrity violation | preserve the actual topology | `FAIL` |
| All required gates satisfied | preserve the actual topology | `READY` |

Treat `capability_gap` as a fail-closed routing action, not as the `FAIL`
verdict. Never change its verdict from `HOLD` merely because the rationale uses
the words “fail closed.”

Apply this precedence to normalized facts:

```text
missing required owner        -> capability_gap
different installed Router    -> domain_delegate
authorization-control request -> authorization_hold
one installed specialist      -> host bypass_single_stage
multiple installed stages     -> direct_chain
```

After freezing that row, evaluate missing inputs, lawful access, explicit
invocation, and evidence depth independently. A non-recurring one-specialist
request remains `bypass_single_stage` with that specialist selected even when
the user will supply the input later, the input is currently absent, the owner
is explicit-only, and the execution verdict is HOLD.

### Enforce host-owned single-stage bypass

When a host response contract exposes `decision_layer` and `decision_skill`,
apply this hard serialization invariant after freezing the route topology:

| Final `route_type` | `decision_layer` | `decision_skill` | `delegated_router` | `recommended_skills_ordered` |
|---|---|---|---|---|
| `bypass_single_stage` | `host_discovery` | `""` | `""` | exactly one installed specialist |

Implicit discovery or loading does not transfer semantic ownership to this
Router. Never serialize `research-workflow-router` in `decision_skill` for a
host bypass. Record actual Router activation only in rationale or receiver
observation metadata; keep activation evidence out of ownership fields. After
drafting all prose, reject the draft unless all five cells match this row.

Apply this algorithm in order:

1. Bypass this Router at the host only when the user explicitly invoked a
   specialist or domain Router. When this implicit Router receives a natural-
   language market or quantitative request, delegate to
   `quant-workflow-router`. Delegate non-market statistical work to
   `stats-experiment-router`.
2. Choose exactly one route type: `direct_chain`, `domain_delegate`,
   `authorization_hold`, or `capability_gap`. Use a host's `none` or
   `bypass_single_stage` probe value only when the Router does not own the task;
   those values do not activate a child.
3. For `direct_chain`, leave `delegated_router` empty and list only exact,
   installed specialist folder names in dependency order.
4. For `domain_delegate`, name one different installed explicit-only domain
   Router, leave `recommended_skills_ordered` empty, copy its exact registry gate
   into `authorization_gates`, and set `next_handoff` to its exact `$router`
   token. This recommendation does not activate the delegated Router.
   Serialize the two adopted domain rows mechanically:

   | Domain | `delegated_router` | `recommended_skills_ordered` | `authorization_gates` | `execution_verdict` |
   |---|---|---|---|---|
   | Market or quantitative | `quant-workflow-router` | `[]` | `["explicit $quant-workflow-router"]` | `HOLD` |
   | Non-market statistics or experiments | `stats-experiment-router` | `[]` | `["explicit $stats-experiment-router"]` | `HOLD` |

   Never place the delegated Router in `recommended_skills_ordered`. That
   array is for specialist handoffs on bypass or direct-chain routes, not for
   a Router already represented by `delegated_router`. If normalized facts
   show that the user already invoked the domain Router explicitly, bypass
   this Router instead of returning a `domain_delegate` with `READY`.
5. For `authorization_hold` or `capability_gap`, keep both route fields empty.
6. If any required child is missing, replace the planned route with
   `capability_gap`, keep both route fields empty, and emit
   `MISSING_REQUIRED_CHILD_<UPPER_SNAKE_SKILL_NAME>`. Use
   the exact code `MISSING_REQUIRED_CHILD_LITERATURE_SYNTHESIS` for the
   synthesis child; a prose paraphrase does not satisfy this contract.
7. Normalize the final object after all reasoning. Apply these postconditions
   literally:

   | Final route type | `delegated_router` | `recommended_skills_ordered` |
   |---|---|---|
   | `direct_chain` | `""` | exact installed children only |
   | `domain_delegate` | one different Router | `[]` |
   | `authorization_hold` | `""` | `[]` |
   | `capability_gap` | `""` | `[]` |
   | host probe `none` | `""` | `[]` |
   | host probe `bypass_single_stage` | `""` | exactly one recommended child |

   Empty means the empty string `""`, never the word `"none"`. Re-run this
   table after drafting the rationale; prose must not reintroduce a cleared
   delegation or selected child.

Resolve the two easily confused route families before applying the generic
postconditions. Treat `recurring=true` as taking precedence over
`single_stage`:

| Normalized facts | Required route state |
|---|---|
| Recurring workflow, explicit-only owner, and no explicit invocation | `authorization_hold`; clear both route fields |
| Gated acquisition requested now without adopted lawful access | `authorization_hold`; clear both route fields |
| Non-recurring `single_stage=true` and exactly one installed owner | host `bypass_single_stage`; recommend that one owner |

For the non-recurring single-stage row, keep the bypass recommendation when an
ordinary required input such as a lawful PDF has not yet been supplied or the
explicit-only owner has not yet been invoked. Record the input and invocation
as readiness gates; do not convert the route to `authorization_hold`. A
recommendation never activates the explicit-only owner.

Before drafting prose, build a stage checklist from the user's requested
outcomes. Map every distinct stage with an installed owner to exactly one
child. Do not let rationale text claim a stage that is absent from
`recommended_skills_ordered`. Reading papers and synthesizing across papers are
different stages: requests to compare sources, reconcile conflicts, synthesize
a review, or identify source-grounded gaps require the distinct
`literature-synthesis` child when it is installed. `nature-reader` cannot absorb
that stage.

Never place `research-workflow-router` in either route field. Never combine a
domain Router with its children.

For a planning-only request that explicitly forbids execution, return the full
future `direct_chain`, or the one-owner `bypass_single_stage` state defined
above, and list permissions that later execution would require. Do not turn
such a plan into `authorization_hold`, and do not truncate a future chain at
its first permission gate. Use `authorization_hold` only when the requested
operation is itself an authorization-controlled recurring, scheduling,
delivery, or gated-acquisition action. Do not use it merely because an
otherwise known specialist is waiting for an input or explicit invocation.

## Determine the smallest route

Identify the requested stages, domain, available evidence, source locations,
writes, and expected deliverable. Use this Router as the implicit front door
when no specialist was explicitly invoked, including for a natural-language
single-stage request that needs one explicit specialist. Also use it when two
or more general research stages need ordering, a domain handoff is needed,
ownership is unclear, or a recurring literature workflow needs a permission
decision.

Keep the receiver topology asymmetric:

| Natural-language domain | Route type | Exact delegate | Required handoff gate |
|---|---|---|---|
| General research | direct specialist or smallest research chain | none | each selected explicit specialist |
| Market or quantitative research | `domain_delegate` | `quant-workflow-router` | `explicit $quant-workflow-router` |
| Non-market statistics or experiment work | `domain_delegate` | `stats-experiment-router` | `explicit $stats-experiment-router` |

Apply the domain delegation row even when the natural-language request names a
single quant or statistics stage. Let the delegated Router decide whether to
bypass to one of its specialists. Do not duplicate its child table here. When
the user already invokes `$quant-workflow-router`, `$stats-experiment-router`,
or another explicit child, do not insert this Router.

Map needs to installed Skills:

| Need | Route |
|---|---|
| Evidence-bounded proposal, research question, or argument map | `researchwrite` |
| Scholarly search, citation discovery, or related literature | `nature-academic-search` |
| Read or translate a supplied lawful full text | `nature-reader` |
| Compare anchored sources, reconcile conflicts, or register research gaps | `literature-synthesis` |
| Draft manuscript sections from supplied evidence | `nature-writing` |
| Polish already supported academic prose | `nature-polishing` |
| Verify references or citation fields | `nature-ref-verifier` or `nature-academic-search` |
| Review, rebut, or data-availability work | `nature-reviewer`, `nature-response`, or `nature-data` |
| Unclear multi-stage Nature publication work | delegate to `nature-research-router` |
| Multi-stage non-market experiment work | delegate to `stats-experiment-router` |
| Multi-stage market, factor, ML, backtest, or attribution work | delegate to `quant-workflow-router` |
| Resolve the knowledge root or stable resources | `manage-personal-knowledge` |
| Read or write authorized Obsidian notes | `obsidian-vault-notes` |

When the user explicitly invokes one specialist, let the request bypass this
Router. Otherwise classify a single-stage request as host
`bypass_single_stage`, recommend exactly one installed specialist, and require
its exact explicit invocation gate. In particular, send one supplied paper to
`nature-reader`, search-only work to
`nature-academic-search`, cross-paper synthesis to `literature-synthesis`, and
writing-only work to `researchwrite` or `nature-writing` according to the
requested artifact. A recommended explicit-only specialist is not thereby
activated. If this Router was implicitly discovered first, record that fact
only as activation evidence, never as semantic ownership. Name the one
specialist as the next handoff, and require explicit `$specialist-name`
invocation unless the receiver independently activated that specialist. Put
the exact invocation gate
`explicit $<specialist-folder-name>` in `authorization_gates`; naming the child
alone does not satisfy the handoff. Copy the complete `explicit_gate` value
from the receiver capability registry; never reconstruct, shorten, translate,
or drop its `explicit ` prefix. Reject a draft containing a bare `$skill-name`
authorization item.

For a domain delegation, apply the same activation discipline to the explicit-
only Router. Emit exactly one registry-backed gate, keep the specialist list
empty, and wait for the explicit Router invocation before any second-layer
routing or execution.

## Build dependency-ordered chains

Use the fewest stages that produce a valid handoff. Common chains are:

- Direction planning:
  `nature-academic-search → literature-synthesis → researchwrite`
- Search to deep reading:
  `nature-academic-search → nature-reader`
- Search to synthesis:
  `nature-academic-search → nature-reader → literature-synthesis`
- Full evidence-to-proposal:
  `nature-academic-search → nature-reader → literature-synthesis → researchwrite`
- Full evidence-to-writing:
  `nature-academic-search → nature-reader → literature-synthesis → researchwrite → nature-writing`
- Supplied-paper drafting:
  `nature-reader → nature-writing → nature-polishing`
- Knowledge capture:
  `manage-personal-knowledge → obsidian-vault-notes`

Insert `nature-reader` before synthesis when selected full texts still need
structured reading. Do not omit `literature-synthesis` when the request needs
cross-paper comparison, conflict reconciliation, review synthesis, or a
source-grounded research-gap decision. In execution mode, stop at the first
unmet retrieval, full-text, evidence, dependency, or permission gate. In
planning-only mode, keep the complete future chain and record that gate without
claiming it was cleared.

## Fail closed on gaps and gates

Return `capability_gap` rather than improvising for:

- general innovation execution without an installed domain executor;
- automatic Case-to-Pattern-to-Skill promotion;
- institutional or credential-gated acquisition without an adopted downloader;
- a development repository without an installable `SKILL.md` payload.

For an implicit weekly digest, recurring monitor, or scheduled literature
delivery request, return `authorization_hold`, set `delegated_router` to `""`,
set `recommended_skills_ordered` to `[]`, and include the exact gate
`explicit $nature-literature-pipeline`. When the receiver defines gates in a
capability registry, treat `authorization_gates` as a closed ordered projection
of its exact `explicit_gate` values: do not append reconstructed or generic
retrieval, scheduling, or delivery approval labels. Record those still-
forbidden operations in `evidence_limit`, or in host-provided
`forbidden_claims` or rationale fields. Do not substitute a self-delegation or
selected children. Do not schedule anything.

For paywalled or institutional full text requested now, return
`authorization_hold` unless an adopted downloader, lawful access, and the
narrow required authorization exist. A DOI, metadata record, abstract, or
inaccessible page is not full text.

Read [routing-boundaries.md](references/routing-boundaries.md) for domain,
retrieval, knowledge, innovation, missing-child, and experience-governance
boundaries.

## Preserve handoff evidence

Carry only the smallest artifact needed by the next stage. Follow
[artifact-handoff-contract.md](references/artifact-handoff-contract.md) and
preserve:

- the frozen question and scope;
- source locators and evidence depth;
- allowed and forbidden conclusions;
- unresolved gaps and authorization gates;
- the next Skill or delegated Router;
- an output path only when the user authorized a write.

Routing alone never authorizes network access, gated acquisition, external
services, scheduling, training, persistent writes, installation, deployment,
publication, version-control actions, or Manager changes.

## Return the routing contract

Return exactly these fields:

```text
route_type:
delegated_router:
recommended_skills_ordered:
excluded_skills:
required_input_artifacts:
expected_output_artifacts:
authorization_gates:
capability_gaps:
evidence_limit:
next_handoff:
```

Validate before returning:

- a Router-owned route uses one of the four exact tokens; a host-level probe
  may instead use exact `none` or `bypass_single_stage`;
- only `domain_delegate` has a different Router in `delegated_router`;
- every `domain_delegate` to an explicit-only Router has exactly its registry
  gate and exact `$router` value in `next_handoff`;
- `direct_chain` has its exact installed children and
  `bypass_single_stage` has exactly one recommended installed child in
  `recommended_skills_ordered`;
- hold and gap routes keep both route fields empty;
- missing dependencies use a stable code and stop the dependent chain;
- an empty delegated Router is serialized as `""`, not `"none"`;
- a recommended explicit-only child is not reported as the activated Skill;
- the Router never selects or delegates to itself.

Run these semantic postconditions last, after writing the rationale:

1. Compare the stage checklist with `recommended_skills_ordered`. Add any missing
   installed owner or remove the unsupported stage claim. Never collapse
   cross-source synthesis into reading.
2. If an implicit Router recommends an explicit-only child, require the exact
   `explicit $<specialist-folder-name>` token in `authorization_gates`, even
   when the current request is planning-only.
3. If a required child is missing, include its stable
   `MISSING_REQUIRED_CHILD_<UPPER_SNAKE_SKILL_NAME>` code verbatim in
   `capability_gaps` before any explanation. For missing
   `literature-synthesis`, reject the draft unless it contains the exact code
   `MISSING_REQUIRED_CHILD_LITERATURE_SYNTHESIS`.
4. For a recurring literature digest governed by the receiver registry,
   reject the draft unless `authorization_gates` is exactly
   `["explicit $nature-literature-pipeline"]`. Do not add prose approval labels
   that the registry does not define.
5. If an ordinary input or explicit-only invocation is missing after a valid
   bypass or direct chain was frozen, preserve that topology and express the
   block only in readiness fields. Reject a draft that changes the route to
   `authorization_hold` solely because its verdict is HOLD.
6. When a host response contract exposes ownership fields and `route_type` is
   `bypass_single_stage`, reject the draft unless `decision_layer` is exactly
   `host_discovery` and `decision_skill` is exactly `""`. Router activation
   evidence never relaxes this postcondition.

Do not replace a required literal with a synonym, translated phrase, or prose
description. The literal is machine-readable evidence; prose may follow it.

## Constrain implicit discovery

Follow [implicit-router-policy.md](references/implicit-router-policy.md).
Implicit discovery permits classification only. If the receiver has not adopted
the bounded exception, require explicit `$research-workflow-router` invocation.

## Hard boundaries

- Do not load all research Skills as a group.
- Do not permit a second project-level implicit Router in the same receiver
  without a new zero-warning runtime budget receipt.
- Do not insert this Router after a specialist was explicitly invoked. When
  acting as the implicit front door for a clear single-stage request, classify
  only and hand off; do not execute the specialist work.
- Do not claim search metadata or an abstract proves full-text review.
- Do not turn proposals, synthesis, model output, or heuristics into established
  evidence without supporting sources and evaluation contracts.
- Do not interpret model agreement, feature importance, or literature frequency
  as causality or truth.
- Do not treat development repositories as installed Skills.
- Do not promote experience to a Pattern or Skill automatically.
- Do not infer Kimi, Manager, deployment, or external-service authority.
- Do not write a report or knowledge note without an authorized output path.

## References

- [artifact-handoff-contract.md](references/artifact-handoff-contract.md)
- [routing-boundaries.md](references/routing-boundaries.md)
- [implicit-router-policy.md](references/implicit-router-policy.md)
