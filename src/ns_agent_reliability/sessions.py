from __future__ import annotations

from dataclasses import replace

from .contracts import SessionRecord, SessionState


class SessionRegistry:
    """In-memory reference registry; production deployments require durable storage."""

    def __init__(self) -> None:
        self._by_goal: dict[str, SessionRecord] = {}

    def bind(self, session: SessionRecord) -> None:
        current = self._by_goal.get(session.goal_id)
        if current and current.state != SessionState.CLOSED and current.session_id != session.session_id:
            raise ValueError("ACTIVE_GOAL_SESSION_ALREADY_EXISTS")
        self._by_goal[session.goal_id] = session

    def get(self, goal_id: str) -> SessionRecord | None:
        return self._by_goal.get(goal_id)

    def checkpoint(self, goal_id: str, added_context_units: int = 0) -> SessionRecord:
        current = self._require(goal_id)
        used = current.context.used_units
        new_context = replace(
            current.context,
            used_units=None if used is None else used + max(0, added_context_units),
            delta_units=current.context.delta_units + max(0, added_context_units),
        )
        updated = replace(
            current,
            state=SessionState.RUNNING,
            checkpoint_count=current.checkpoint_count + 1,
            context=new_context,
        )
        self._by_goal[goal_id] = updated
        return updated

    def rollover(self, goal_id: str, new_session_id: str) -> SessionRecord:
        current = self._require(goal_id)
        replacement = replace(
            current,
            session_id=new_session_id,
            generation=current.generation + 1,
            state=SessionState.CREATED,
            baseline_hydrated_count=0,
            checkpoint_count=0,
        )
        self._by_goal[goal_id] = replacement
        return replacement

    def close(self, goal_id: str) -> SessionRecord:
        current = self._require(goal_id)
        updated = replace(current, state=SessionState.CLOSED)
        self._by_goal[goal_id] = updated
        return updated

    def _require(self, goal_id: str) -> SessionRecord:
        if goal_id not in self._by_goal:
            raise KeyError("GOAL_SESSION_NOT_FOUND")
        return self._by_goal[goal_id]
