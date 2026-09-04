# Scheduling and Delivery Boundaries

Replaces platform-specific cron/delivery notes with generic, tool-agnostic rules.

## Scheduling (cron / scheduled jobs)

- Create, modify, or delete scheduled jobs only after explicit user approval in
  the current task.
- Immediately after creating a job, verify with the scheduler's own list/show
  command that the job is actually registered and visible; a "create succeeded"
  response alone is not evidence.
- Local schedulers fire only while the machine and the agent runtime are
  running. Tell the user this when scheduling morning or one-shot jobs.
- For a recurring daily pipeline, validate the full chain once manually before
  relying on the schedule: search → score → format → (authorized) delivery →
  (approved) archival.
- If a scheduled run did not fire, prefer a manual catch-up run over long
  diagnosis sessions; report the miss plainly.

## Delivery (messaging platforms)

- Delivery happens only on explicit per-run user authorization, to a target the
  user has already configured (e.g., a Feishu group the bot belongs to, a
  Telegram channel, an email address).
- Never ask for, accept, or transmit credentials, bot tokens, webhooks with
  embedded secrets, or session material in chat. Refer to configuration by
  name (e.g., "the Feishu target you configured"), not by secret value.
- Without explicit authorization, present the digest directly in chat and note
  that delivery was skipped.
- Keep an audit line per run: date, candidate count, delivered count, target
  label (non-secret), and any failures.

## Archival

- Write notes only to a user-approved raw-notes directory, never to curated
  wiki/knowledge-base pages.
- Use `references/note-template.md` for note structure and naming.
- Deduplicate against the existing archive (DOI / arXiv ID / OpenAlex ID /
  normalized title) before writing.
