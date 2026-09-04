# Governed implicit control-router policy

This policy records the approved candidate exception for exactly one
project-level implicit control Router. It becomes active only after the frozen
candidate passes its acceptance gates and a separately authorized deployment
completes. The policy itself grants no execution or external-action permission.

## Eligibility

Allow implicit discovery only when every condition holds:

1. The Skill is a control Router and does not execute domain work.
2. It performs no network, browser, API, external-service, training, scheduling,
   trading, installation, deployment, Manager, Vault, project, or active-Skill
   mutation.
3. The Router classifies a clear single-specialist request, emits the host
   `bypass_single_stage` handoff, and does not execute the specialist work.
4. The Router returns the smallest ordered set or delegates to one domain Router.
5. It never selects itself and never preloads a delegated Router's children.
6. Missing required children, evidence, or authorization fail closed.
7. The route decision cannot expand permissions held by the original request.
8. Static tests and independent receiver discovery tests cover false-positive,
   self-routing, missing-child, and authorization cases.

## Receiver inventory policy

Keep the implicitly injected inventory deliberately small:

- keep exactly one project-level implicit control Router unless a controlled
  runtime A/B test proves that a larger implicit set produces no context-budget
  event;
- prefer non-mutating L0/L1 control Routers for ambiguous or multi-stage work;
- keep delegated domain Routers explicit-only and hand them off with their
  exact `$router-name` token;
- keep specialist Skills explicit-only by default;
- grant a specialist an implicit exception only after measured single-stage
  trigger and non-trigger cases show that the exception improves routing;
- remove unused or overlapping implicit descriptions from the receiver rather
  than compensating with a catch-all Router description;
- keep each implicit description short, distinctive, and explicit about its
  nearest exclusions.

This file defines the approved candidate policy but does not by itself change
the active receiver, Manager, preset, group, or installed-Skill state. Activate
it only through the separately authorized, receipt-backed deployment described
by the acceptance gate below.

If any condition fails, set `allow_implicit_invocation: false` and require
explicit invocation.

## Runtime behavior

- Treat an implicit match as permission to classify the request only.
- Ask for the narrow authorization required by a selected child operation.
- Bypass routing when the user explicitly names a specialist.
- Do not claim that an explicit-only specialist was activated merely because
  the Router recommends or selects it. When an implicitly discovered Router
  identifies one clear specialist, report the Router as the actual activation,
  provide the explicit `$specialist-name` handoff, and wait for that invocation
  unless the receiver independently activated the child.
- Prefer one domain Router over duplicating its internal chain.
- Require the exact registry-backed `explicit $router-name` gate before an
  explicit-only delegated Router may perform second-layer routing.
- Report a capability gap instead of substituting an uninstalled repository.

## Acceptance gate

Before deployment, require:

- the recorded governance decision that explicitly permits this one-Router
  exception while keeping domain Routers and specialists explicit-only;
- `quick_validate.py` success;
- static audit with no unresolved structural or permission risk;
- offline routing-contract success;
- independent receiver tests showing intended discovery and non-discovery cases;
- no unresolved Skill-context truncation warning in the tested receiver, or
  evidence from controlled A/B cases that the warning is harmless;
- a deployment plan that preserves rollback and does not mutate Manager unless
  separately authorized.

Until the predeployment receipts exist, keep the candidate staged and describe
readiness as HOLD. When they all exist, describe the candidate only as ready
for the separately authorized conditional deployment. After deployment,
require target hashes, validation, and fresh isolated receiver tests before
describing the deployed payload as accepted. Do not equate either state with a
Default-group change, Manager adoption, Kimi adaptation, or Codex final
acceptance.

Treat a receiver warning that Skill descriptions were shortened to fit a
context budget as a discovery blocker, not as a cosmetic warning. Do not claim
implicit-routing acceptance while the tested trigger surface differs from the
intended allowlist.
