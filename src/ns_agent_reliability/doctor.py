"""Small outsider-usable diagnostics over a normalized agent reliability JSON snapshot."""
from __future__ import annotations
import argparse, json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    evidence: str
    remediation: str

def _f(rule_id: str, severity: str, evidence: str, remediation: str) -> Finding:
    return Finding(rule_id, severity, evidence, remediation)

def inspect_snapshot(s: Mapping[str, Any]) -> list[Finding]:
    """Missing fields are UNKNOWN; a rule fires only on supplied failure evidence."""
    out: list[Finding] = []
    o=s.get("ownership") or {}
    if o.get("released_or_expired") is True and o.get("session_alive") is True and o.get("reacquire_blocked") is True:
        out.append(_f("STALE_OWNERSHIP","HIGH","released/expired ownership + live session blocks reacquire","Separate session liveness from lease ownership; fence new ownership with a monotonic epoch/token."))

    by_target: dict[str,list[str]]={}
    for a in s.get("authorities") or []:
        if isinstance(a,Mapping) and a.get("writes") is True and a.get("target"):
            by_target.setdefault(str(a["target"]),[]).append(str(a.get("name") or "unnamed"))
    for target,names in by_target.items():
        if len(names)>1:
            out.append(_f("DUPLICATE_AUTHORITY","CRITICAL",f"target={target}; writers={','.join(names)}","Collapse mutation to one canonical authority; keep other projections read-only/advisory."))

    r=s.get("retry") or {}
    if r.get("enabled") is True and r.get("max_attempts") in (None,0):
        out.append(_f("UNBOUNDED_RETRY","HIGH",f"max_attempts={r.get('max_attempts')!r}","Set a finite retry budget and terminal failure state."))
    if r.get("lineage_nested") is True:
        out.append(_f("RETRY_LINEAGE_CORRUPTION","HIGH","lineage_nested=true","Preserve one root task/run identity and advance only bounded retry generation."))

    resume=s.get("resume") or {}
    if resume.get("long_running") is True and (resume.get("durable_resume") is False or resume.get("requires_raw_chat_history") is True):
        out.append(_f("CONTEXT_RESUME_DEFECT","HIGH",f"durable_resume={resume.get('durable_resume')!r}; raw_chat_required={resume.get('requires_raw_chat_history')!r}","Persist a bounded checkpoint/handoff artifact and resume from current canonical state."))

    public=s.get("public_tools")
    threshold=int(s.get("public_tool_warning_threshold") or 20)
    if isinstance(public,list) and len(public)>threshold:
        out.append(_f("EXCESSIVE_PUBLIC_TOOL_SURFACE","MEDIUM",f"public_tools={len(public)} > {threshold}","Group capabilities behind stable authority-class primitives and bounded action/payload contracts where semantics permit."))

    schema=s.get("schema") or {}
    if schema.get("client_version") and schema.get("server_version") and schema.get("client_version")!=schema.get("server_version") and schema.get("stale_client_overrides_server") is True:
        out.append(_f("STALE_CLIENT_SERVER_SCHEMA","HIGH",f"client={schema.get('client_version')}; server={schema.get('server_version')}","Treat live server contract as current truth; refresh stale clients without resurrecting deprecated server surfaces."))

    for t in s.get("tools") or []:
        if isinstance(t,Mapping) and str(t.get("class") or "").upper()=="READ" and t.get("can_mutate") is True:
            out.append(_f("AUTHORITY_LEAKAGE","CRITICAL",f"read tool can mutate: {t.get('name') or 'unnamed'}","Separate read and mutation authority classes."))

    m=s.get("mutation") or {}; v=s.get("verification") or {}
    if m.get("enabled") is True and v.get("result_evidence_required") is False:
        out.append(_f("EVIDENCE_GAP","HIGH","mutation enabled while result evidence is optional","Require risk-appropriate observed result evidence; worker self-report is not completion evidence."))

    d=s.get("redispatch") or {}; completed={str(x) for x in d.get("completed_task_ids") or []}; dispatched={str(x) for x in d.get("dispatched_task_ids") or []}
    dup=sorted(completed & dispatched)
    if dup:
        out.append(_f("DUPLICATE_REDISPATCH","HIGH",f"redispatched completed ids={','.join(dup)}","Converge terminal evidence onto canonical task identity and deny completed-task redispatch."))

    for p in s.get("dependency_pins") or []:
        if isinstance(p,Mapping) and p.get("expected") and p.get("observed") and p.get("expected")!=p.get("observed"):
            out.append(_f("STALE_DEPENDENCY_PIN","HIGH",f"{p.get('name') or 'dependency'} expected={p.get('expected')} observed={p.get('observed')}","Bind current entrypoint to current canonical dependency or remove obsolete ancestry pins."))

    dep=s.get("deployment") or {}
    if dep.get("self_pin_blocks_current") is True:
        out.append(_f("SELF_LOCKING_DEPLOY_BOUNDARY","CRITICAL","self_pin_blocks_current=true","Collapse stale self-pins and reuse one current privileged change boundary."))

    rb=s.get("rollback") or {}; restored=rb.get("deprecated_surfaces_restored") or []
    if restored:
        out.append(_f("ROLLBACK_RESURRECTS_DEPRECATED_SURFACE","CRITICAL",f"restored={','.join(map(str,restored))}","Rollback to the last verified current-generation state, not an obsolete compatibility surface."))

    obs=s.get("observability") or {}
    if obs.get("required_for_execution") is True:
        out.append(_f("OBSERVABILITY_COUPLED_TO_EXECUTION","MEDIUM","observability.required_for_execution=true","Make telemetry/feedback fail-soft unless it is a required safety input."))

    hist=s.get("history") or {}
    if hist.get("rebound_as_current_authority") is True:
        out.append(_f("HISTORICAL_STATE_CURRENT_AUTHORITY","HIGH","historical state rebound as current authority","Keep history searchable but require fresh explicit/current-state binding before authority is restored."))
    return out

def report_dict(s: Mapping[str,Any]) -> dict[str,Any]:
    findings=inspect_snapshot(s)
    return {"schema":"agent_reliability_doctor_report_v1","finding_count":len(findings),"findings":[asdict(x) for x in findings]}

def main(argv: list[str] | None=None) -> int:
    p=argparse.ArgumentParser(description="Diagnose normalized agent-reliability evidence JSON")
    p.add_argument("snapshot",type=Path); p.add_argument("--json",action="store_true")
    a=p.parse_args(argv); report=report_dict(json.loads(a.snapshot.read_text(encoding="utf-8")))
    if a.json: print(json.dumps(report,indent=2,sort_keys=True))
    else:
        print(f"Agent Reliability Doctor: {report['finding_count']} finding(s)")
        for x in report["findings"]:
            print(f"[{x['severity']}] {x['rule_id']}\n  evidence: {x['evidence']}\n  remediation: {x['remediation']}")
    return 0

if __name__=="__main__": raise SystemExit(main())
