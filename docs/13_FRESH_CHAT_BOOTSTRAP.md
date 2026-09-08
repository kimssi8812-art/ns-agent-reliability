# Fresh-Chat Bootstrap

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


A new chat should recover project state from live server metadata and durable project artifacts rather than depending on conversational memory.

Recommended order:

1. read current control-plane status;
2. load the public operating contract and bootstrap index;
3. recover current Goal and Taskboard state;
4. load the relevant architecture plan;
5. load only evidence/context references required by the Goal;
6. recover an existing Goal Session when valid;
7. load only the reference modules needed for the checkpoint;
8. continue work.

If an expected layer cannot be verified, expose an explicit state such as `CONTEXT_NOT_VERIFIED`. Do not replace missing current evidence with an old remembered assertion.

Fresh-room continuity does not require replaying the complete project history. Durable state should store references, digests, bounded summaries, Goal state, worker/session state, and blockers. The new chat hydrates only the relevant slice.

Acceptance requires a fresh chat to recover current connectivity, Goal progress, blockers, worker/session state, evidence references, and the next eligible checkpoint without the human retelling the project history.
