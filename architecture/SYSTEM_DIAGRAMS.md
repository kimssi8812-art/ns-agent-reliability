# System Diagrams

## 1. V3 end-to-end control path

```mermaid
flowchart TD
    S[Human Owner] --> N[GPT/N Architecture + Judgment]
    N --> H[NS Control Hub]
    H --> G[Goal Registry / DAG / Critical Path]
    H --> E[Evidence / Progress / Taskboard]
    H --> R[Resource + Model + Session Registry]
    H --> DX[Bounded Deterministic Executor]
    H --> W1[Claude Worker Manager]
    H --> W2[Codex Worker Manager]
    H --> W3[Gemini Worker Manager]
    DX --> EV[Atomic Machine Event Ledger]
    W1 --> C1[Reusable Goal Session]
    W2 --> C2[Reusable Goal Session]
    W3 --> C3[Reusable Goal Session]
    C1 --> EV
    C2 --> EV
    C3 --> EV
    EV --> E
    EV --> MF[Machine Flowboard]
    EV --> HC[Human Cockpit Projection]
    E --> H
    H --> N
    HC --> S
    H --> GA[Gate Adapter]
    GA --> OP[Operational Runtime / SSOT]
```

## 2. Direct Channel boundary

```mermaid
flowchart LR
    CHAT[ChatGPT / Work] --> T[Secure MCP Tunnel]
    T --> MCP[Direct Channel MCP Server]
    MCP --> READ[Safe Read Capabilities]
    MCP --> SW[Sandbox Write Capabilities]
    MCP --> EXEC[Bounded Deterministic Executor]
    MCP --> DISPATCH[Bounded Worker Dispatch]
    MCP --> GP[Gate Request Preparation]
    READ --> NS[(Private Server State)]
    SW --> SB[(GPT Sandbox)]
    EXEC --> SB
    DISPATCH --> Q[Task Queue / Consumer]
    Q --> RUNNER[Pinned Provider Runner]
    RUNNER --> WORKER[Provider CLI]
    GP --> GATE[External Gate]
```

Rule: executor access is bounded capability, not unrestricted root shell.

## 3. Routing decision

```mermaid
flowchart TD
    CK[Goal Checkpoint] --> AUTH[Authority / Security Boundary]
    AUTH --> KIND{Deterministic?}
    KIND -->|yes| EX[Bounded Executor]
    KIND -->|no| ELIG[Eligible READY Providers]
    ELIG --> WARM[Warm Goal Session Affinity]
    WARM --> CAP[Capability / Resource / Reliability]
    CAP --> PROF[Runtime / Model / Profile]
    PROF --> PIN[Pin to Goal Session Generation]
    EX --> RESULT[Result + Evidence + FlowEvent]
    PIN --> RESULT
```

## 4. Goal Session context lifecycle

```mermaid
stateDiagram-v2
    [*] --> GoalAssigned
    GoalAssigned --> SessionCreate
    SessionCreate --> BaselineHydrated
    BaselineHydrated --> Running
    Running --> CheckpointPersisted
    CheckpointPersisted --> Running: delta only
    CheckpointPersisted --> RolloverRequired: projected capacity/recovery
    RolloverRequired --> SessionCreate: generation + 1 / compact baseline
    Running --> GoalResult
    GoalResult --> StatePersisted
    StatePersisted --> SessionClosed
    SessionClosed --> [*]
```

## 5. Zero-unnecessary-AI DNA path

```mermaid
flowchart LR
    SHARE[Share Reference] --> INTAKE[Deterministic Intake]
    INTAKE --> EXPORT[Transcript Extraction]
    EXPORT --> COMP[Completeness Verification]
    COMP --> PKG[Deterministic Package / DNA]
    PKG --> REG[DNA Registry / Index]
    REG --> PACK[Bounded Inheritance Packet]
    PACK --> BASE[Goal / Fresh-Room Baseline]
    BASE --> DELTA[Checkpoint Deltas]
    REG -. on-demand referenced fragment .-> DELTA
```

Default infrastructure path creates no provider session. Optional semantic enrichment is separate.

## 6. Health normalization

```mermaid
flowchart TD
    PERSIST[Persisted health/latches] --> NORM[Health Normalizer]
    LIVE[Fresh liveness probe] --> NORM
    READY[Readiness probe] --> NORM
    AUTH[Auth state] --> NORM
    QUOTA[Quota/resource state] --> NORM
    SCOPE[Session scope + generation] --> NORM
    NORM --> L[Liveness]
    NORM --> RD[Readiness]
    NORM --> DA[Dispatch Allowed]
    NORM --> FC[Failure Classes]
```

Rule: `Liveness != Readiness != Dispatch Allowed`, and health identity includes scope/source/freshness.

## 7. Execution-profile governance

```mermaid
flowchart LR
    CK[Semantic Goal Checkpoint] --> P[Provider selection]
    P --> V[Runtime/CLI + adapter version]
    V --> M[Model]
    M --> RP[Reasoning/tool profile]
    RP --> PIN[Pin to Goal Session generation]
    NEW[New version/model discovered] --> CANARY[Compatibility + shadow/canary]
    CANARY --> PROMOTE[Promote at safe boundary]
    CANARY --> QUAR[Quarantine / rollback]
```

## 8. Atomic event truth and dual projection

```mermaid
flowchart TD
    SRC[Hub / Executor / WorkerManagers / Taskboard / Evidence / Gate] --> F[Normalized FlowEvent]
    F --> LEDGER[Bounded Durable Event Ledger]
    LEDGER --> RED[Reducers / Materialized State]
    RED --> M[Machine Flowboard Snapshot]
    RED --> H[Human Cockpit Snapshot]
```

Rule: Human Cockpit is a projection, never a second truth collector.

## 9. Evidence-driven progress

```mermaid
flowchart LR
    A[Checkpoint result] --> V[Evidence verification]
    V -->|verified| C[Consume Taskboard/DAG state]
    V -->|not verified| B[Blocked/Failed]
    C --> P[Recalculate verified weighted progress]
    P --> EVT[Emit state/progress FlowEvents]
    EVT --> NEXT[Select next ready critical-path node]
```

## 10. Progressive GPT/N role reduction

```mermaid
flowchart LR
    BUILD[Build phase: N architect + integrator + bounded executor user] --> STABLE[Stabilized: N architect + orchestrator + reviewer]
    STABLE --> MATURE[Mature: N Goal/judgment layer]
    BUILD --> AUTO[Repeated deterministic loops]
    AUTO --> HUBJOB[Promote into Hub jobs/adapters]
    HUBJOB --> STABLE
```
