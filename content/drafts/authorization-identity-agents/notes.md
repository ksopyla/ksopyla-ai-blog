

Draft of the post "Authorization and Identity for Agents"

## Original Seed Ideas

Auth0 for agents how this works, what are the benefits and how to implement it.

Microsoft Agentic Framework how solves the problem of authorization and identity for agents.

AWS agentic core how solves the problem of authorization and identity for agents.

What are the types of authorization and identity for agents?
- working on behalf of the user
- the patterns for asking for permission for users, 
- agentic payment protocols should have this figour out
- how the A2A implements this

---

## Research Notes (collected 2026-04-12)

### The Core Problem

Agents are not humans. They are non-deterministic, ephemeral, can spawn sub-agents, chain actions across trust boundaries, and accumulate permissions over time without review. Traditional IAM (SSO, MFA, RBAC) was designed for humans sitting at keyboards.

Key stats (2026):
- NHI-to-human identity ratio: 45:1 to 144:1 in enterprise environments
- 78% of organizations have no formal identity policies for non-human actors
- 80% of organizations using AI agents report agents have taken unintended actions
- 53% of open-source MCP server implementations still rely on static API keys
- Only 23% of organizations have a formal strategy for agent identity management

The Salesloft-Drift 2025 incident: valid authentication tokens (long-lived) enabled large-scale data theft. "Valid authentication ≠ secure authority."

### Existing Material in This Repo

- `content/drafts/agents-orchestration-thoughts/index.md` — already covers identity as "the hardest part," RBAC limits, delegation chains, signed delegation, control plane thesis. This is the parent long-form piece.
- `content/linkedin/2026-03-enterprise-agents-new-systems-mindset/carousel_hardest_problem_is_identity.md` — carousel copy: identity as enterprise blocker, RBAC vs agents, static roles vs per-request tokens.
- `content/linkedin/2026-03-enterprise-agents-new-systems-mindset/post.md` — identity + authorization as least-solved layer.

This post should be the **deep-dive companion** to the orchestration piece — focused entirely on the identity/auth layer with concrete vendor implementations and emerging standards.

---

## The Big Three: Vendor Approaches

### 1. Auth0 for AI Agents

- Status: Developer Preview since April 2025
- Docs: https://auth0.com/docs/get-started/auth0-for-ai-agents
- Blog: https://auth0.com/blog/introducing-auth0-for-ai-agents/

Key capabilities:
- **User Authentication**: OAuth 2.0 + OIDC, account linking, step-up auth
- **Token Vault**: Securely stores and auto-refreshes API tokens for external services (Google, GitHub, Slack, Microsoft)
- **Asynchronous Authorization (CIBA)**: Client-Initiated Backchannel Authentication + Rich Authorization Requests (RAR) — human-in-the-loop approval while agent works in background
- **FGA for RAG**: Fine-Grained Authorization at document/relationship level in RAG pipelines — agents only access data they're authorized for

Framework integrations: LangChain, LlamaIndex, Cloudflare Agents, Vercel AI SDK, Firebase Genkit, early MCP support

**Angle for post**: Auth0 treats agents as first-class OAuth clients with dedicated identities. The CIBA pattern is the most interesting — it decouples "agent wants to do X" from "user approves X" asynchronously.

??Explore the idea further, is this authorization of agents on behalf of the users? Is so this is only the part of the story, what if agent spawns other agents? However every agent is working for a particular user, so at the and each instanse of the agent should be associated by the user, but how to track updates in agents prompts and backstory, even small change in prompt could change the agent behaviour, how to autorize the tools, yolo mode is dangerous but on the other side keeping asking the user of each permision as MS Vista did in the past is not scallable

### 2. Microsoft Entra Agent ID

- Status: Part of Microsoft Agent 365 control plane
- Docs: https://learn.microsoft.com/en-us/entra/agent-id/
- Agent Framework 1.0 shipped April 2026 (unified Semantic Kernel + AutoGen)

Key architecture:
- **Agent identity model**: Single-tenant service principals with "agent" subtype, built on existing Entra ID infrastructure
- **Impersonation model**: Agent identity blueprint acquires tokens on behalf of each agent identity (different from standard service principals that operate independently)
- **OAuth 2.0 grant types**: 
  - `client_credentials` — autonomous operations
  - `jwt-bearer` — On-Behalf-Of (OBO) delegation scenarios
  - `refresh_token` — background operations
- **Federated Identity Credentials (FIC)**: Specialized token exchange patterns

**Angle for post**: Microsoft bolts agent identity onto their existing Entra infrastructure. The impersonation model is smart — agents don't get their own standing credentials, they get temporary tokens scoped to specific delegation contexts. But it's deeply tied to the Microsoft ecosystem.

### 3. AWS Bedrock AgentCore Identity

- Status: Production service
- Docs: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html
- Blog: https://aws.amazon.com/blogs/security/securing-ai-agents-with-amazon-bedrock-agentcore-identity/

Key architecture — **Identity Chaining**:
1. User authenticates via IdP (Okta, Cognito, Entra) → receives JWT
2. App passes JWT to AgentCore Runtime for validation
3. AgentCore creates a **workload access token** representing both agent identity AND user context
4. Agent uses this token to interact with AgentCore Identity services + Token Vault (never calls external systems directly)
5. For external providers, AgentCore orchestrates OAuth flows and stores credentials in the vault

The key insight: agents act as "constrained delegates" — the identity chain preserves who asked, who's acting, and what boundaries apply.

**Angle for post**: AWS's identity chaining is architecturally clean — separates identity from delegation, then recombines them with constraints. The Token Vault pattern (shared with Auth0) shows convergence: nobody trusts agents with raw credentials anymore.

### Vendor Comparison Table (draft)

| Feature | Auth0 | Microsoft Entra Agent ID | AWS AgentCore Identity |
|---------|-------|--------------------------|------------------------|
| Identity model | Dedicated agent identities | Service principals (agent subtype) | Identity chaining (user + agent context) |
| Delegation | CIBA (async approval) | OBO (jwt-bearer) | Workload access tokens |
| Token management | Token Vault | Managed tokens via FIC | Token Vault + KMS |
| External service auth | Auto-refresh stored tokens | Federated credentials | OAuth orchestration via vault |
| RAG/data access control | FGA per-document | Entra permissions model | IAM policies |
| Lock-in level | Low (framework integrations) | High (Microsoft ecosystem) | Medium (AWS services) |
| MCP integration | Early access | Via Agent Framework 1.0 | Via AgentCore Runtime |

---

## Protocol Layer: How Standards Handle Auth

### A2A Protocol Authorization

- Auth added in A2A v0.2 (2025-2026)
- Uses OpenAPI Security Schemes defined in **Agent Cards**
- Supports: OAuth 2.0, Bearer Token verification
- **Delegated User Authorization** (Issue #19): agents act on behalf of users via external IdP + OAuth 2.0, optional auth headers in agent-to-agent requests, middleware validation per request
- SDKs: Python, Go, JavaScript, Java, .NET
- Links: https://deepwiki.com/google/A2A/3.2-security-and-authentication, https://github.com/google/A2A/issues/19

### MCP Authorization

- Based on OAuth 2.1 (RFC8414, RFC7591, RFC9728)
- Protected MCP servers = OAuth 2.1 resource servers
- MCP clients = OAuth 2.1 clients acting on behalf of resource owners
- Flow: 401 Unauthorized → Protected Resource Metadata → standard OAuth flow → access token
- Authorization is optional but recommended for user-specific data, audit trails, enterprise
- Spec: https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization

**Key insight**: MCP and A2A handle auth at different levels. MCP secures tool/resource access (capability layer). A2A secures agent-to-agent delegation (coordination layer). Enterprise stacks need both.

---

## Emerging Standards (IETF + Open Protocols)

?? Emerging standards are so goood, keep this in orginal post

### IETF: OAuth 2.0 Extension for AI Agents (On-Behalf-Of User)

- Draft: `draft-oauth-ai-agents-on-behalf-of-user-02` (August 2025)
- Spec: https://datatracker.ietf.org/doc/html/draft-oauth-ai-agents-on-behalf-of-user-02

Key additions to OAuth 2.0:
- `requested_actor` parameter — identifies the specific agent needing delegation
- `actor_token` parameter — authenticates the agent during code exchange
- New grant type: `urn:ietf:params:oauth:grant-type:agent-authorization_code`
- Can be initiated by resource server challenge (dynamic user consent when access is attempted)
- Enhanced auditability via access token claims documenting full delegation chain (user → client app → agent)

### IETF AIMS (Agent Identity Management System)

- Draft: `draft-klrc-aiagent-auth-01` (March 30, 2026)
- Authors from Defakto Security, AWS, Zscaler, Ping Identity
- Spec: https://datatracker.ietf.org/doc/html/draft-klrc-aiagent-auth-00

Composes existing standards into 8-layer architecture:
1. **Agent Identifier**: WIMSE/SPIFFE URI (`spiffe://company.example/agents/data-analyst`)
2. **Agent Credentials**: X509-SVID, JWT-SVID, or Workload Identity tokens (all short-lived)
3. **Agent Attestation**: Hardware, software, platform, or supply-chain evidence
4. **Credential Provisioning**: Automated via SPIRE with rotation and revocation
5-8. Authorization, monitoring, observability layers

### IETF AIP (Agent Identity Protocol)

- Draft: `draft-paras-agent-identity-protocol-00` (April 2026)
- Spec: https://www.ietf.org/staging/draft-paras-agent-identity-protocol-00.html

More ambitious approach:
- W3C DID-conformant agent identifier (`did:aip`)
- Cryptographically verifiable principal delegation chain
- Fine-grained Capability Manifest
- Signed Credential Token with 12-step validation algorithm
- Chained workflow approval mechanism (AIP-GRANT)

### Grantex Protocol (v1.0 finalized February 2026)

- Site: https://grantex.dev/
- Spec: https://github.com/mishrasanjeev/grantex/blob/main/SPEC.md

Open protocol for delegated agent authorization:
- DIDs for cryptographic agent identity
- Human-consent-based grant flow with scoped, revocable permissions
- Signed JWT token format
- Real-time revocation + immutable audit trail

---

## SPIFFE / Workload Identity for Agents

- Blog: https://blog.ogwilliam.com/post/securing-ai-agents-with-spiffe-spire.html
- IETF analysis: https://iamdevbox.com/posts/ietf-aims-ai-agent-identity-management-system-spiffe-oauth/

Why SPIFFE matters for agents:
- Provides cryptographically-signed identities (SPIFFE IDs): `spiffe://corp.ai/agents/customer-support-v2`
- Short-lived credentials via SPIRE (SVIDs) — auto-rotation, reduces blast radius
- Context-aware policies: security rules based on software properties, can quarantine untrusted agents
- Cryptographic chain of custody for all agent actions

SPIFFE vs cloud-native identity:
- SPIFFE/SPIRE: cross-cloud, zero-trust, strong for multi-vendor agent federation
- Cloud-native (AWS IAM roles, GCP Workload Identity, Azure Managed Identity): simpler operations, vendor-locked
- Trend: 2026 orgs evaluating hybrid — cloud-native for internal, SPIFFE for cross-org federation

---

## Agentic Payment Protocols

Payments force the identity/authorization problem to its sharpest edge — agents spending real money need unambiguous delegation.

### Google AP2 (Agent Payments Protocol)

- Announced 2025, major push April 2026
- 60+ launch partners (Mastercard, PayPal, Adyen, Coinbase)
- Link: https://vellum.ai/blog/googles-ap2-a-new-protocol-for-ai-agent-payments

Key concept: **Verifiable Credential mandates**
- Cart Mandate — final purchase approval
- Intent Mandate — pre-authorized delegated tasks
- Payment Mandate — signals for fraud detection

### Stripe ACP (Agentic Commerce Protocol)

- Developed with OpenAI, live in ChatGPT Instant Checkout (early 2026)
- Handles merchant integration layer
- Agents share credentials and initiate checkouts without exposing raw payment data
- Link: https://orium.com/blog/agentic-payments-acp-ap2-x402

### Coinbase x402

- HTTP 402 "Payment Required" revived for machine-to-machine payments
- No accounts, no API keys — programmatic settlement
- Execution layer (complements AP2's auth layer and ACP's merchant layer)
- Link: https://aptosfoundation.org/currents/what-is-x402-the-payment-protocol-for-ai-agents-on-aptos

### Comparison: https://atxp.ai/blog/agent-payment-protocols-compared/

**Angle**: Payment protocols are ahead of general-purpose agent auth in one way — they already define clear delegation boundaries because the cost of getting it wrong is financial. The rest of agent auth should learn from this.

---

## Human-in-the-Loop Permission Patterns

Five production patterns (from https://cordum.io/blog/human-in-the-loop-ai-patterns):

1. **Pre-execution approval gate** — agent prepares action, human approves, then executes
2. **Exception-based escalation** — autonomous for routine, escalates ambiguous/high-stakes
3. **Graduated autonomy** — permissions expand based on demonstrated reliability
4. **Sampled audit at scale** — random sampling of executed actions for review
5. **Post-execution output review** — approval after execution (for low-risk, reversible actions)

Delegation chain security invariants (from https://agenticcontrolplane.com/agent-to-agent):
- **Origin tracking**: The human initiating the chain is never changed across hops
- **Permission narrowing**: Child agents receive only the intersection of parent permissions and their own profile — permissions only narrow, never widen

Anti-pattern: "Prompt-based permissions" — telling agents in prompts to "ask permission" is not real HITL. Agents can ignore prompts. Real HITL requires deterministic, version-controlled policy enforcement **outside the model** with immutable audit trails.

EU AI Act Article 14 (human oversight) takes full effect August 2, 2026 — regulatory pressure will force enterprise adoption of real HITL patterns.

---

## Taxonomy: Types of Agent Authorization

?? This is so goood, keep this in orginal post

Based on research, the authorization problem splits into these distinct scenarios:

### 1. Agent Acting on Behalf of User (Delegated Authority)
- User explicitly grants agent scoped permissions
- OAuth OBO flows, CIBA async approval, identity chaining
- Token carries both user identity and agent identity
- Examples: Auth0 CIBA, AWS identity chaining, Microsoft OBO
- Key constraint: agent can never exceed user's own permissions

### 2. Agent Acting Autonomously (Own Identity)
- Agent has its own service principal / workload identity
- Operates under pre-defined policies, not user delegation
- Examples: Microsoft `client_credentials`, SPIFFE-based identity
- Key risk: permission accumulation, orphaned credentials
- Requires: periodic review, ephemeral credentials, kill switches

### 3. Agent-to-Agent Delegation (Chained Authority)
- One agent delegates subset of its authority to another
- Permissions narrow at each hop (never widen)
- Requires: signed delegation chains, origin tracking, full audit trail
- Examples: A2A delegated authorization, AIP-GRANT chained workflow
- Hardest scenario — dynamic agent spawning makes static RBAC impossible

### 4. Agent Accessing External Services (Credential Brokering)
- Agent needs to call external APIs (GitHub, Slack, databases)
- Never holds raw credentials — Token Vault pattern
- Broker manages OAuth flows, stores tokens, auto-refreshes
- Examples: Auth0 Token Vault, AWS AgentCore Token Vault
- Pattern convergence: every vendor landed on this independently

### 5. Agent Spending Money (Financial Delegation)
- Highest-stakes delegation — requires verifiable mandates
- Cryptographically signed authorization with clear limits
- Examples: AP2 mandates, ACP checkout flow, x402 programmatic payments
- Unique constraint: financial regulations + fraud detection requirements

---

## Open Questions / Post Angles

1. **Why RBAC breaks for agents** — dynamic agent creation, prompt-based responsibility changes, permission accumulation. Already covered in orchestration draft, but worth a focused take.

2. **The Token Vault convergence** — Auth0, AWS, and Microsoft all independently arrived at "never let agents hold raw credentials." What does this tell us about the design space?

3. **Identity chaining vs impersonation vs CIBA** — three different architectural bets by AWS, Microsoft, and Auth0. Which pattern wins for which use case?

4. **Standards fragmentation** — IETF has at least 3 competing drafts (AIMS, AIP, OAuth extension). Plus vendor-specific approaches. How does an enterprise pick?

5. **Payment protocols as authorization frontier** — payment systems are ahead because the cost of failure is visible and immediate. Can general agent auth learn from AP2/ACP/x402?

6. **The 53% static API key problem** — most MCP servers still use static keys. What's the migration path to proper OAuth?

7. **EU AI Act Article 14** — human oversight regulation takes effect August 2026. Enterprise pressure will force real HITL, not prompt-based theater.

---

## Suggested Post Structure

**Title options**:
- "Authorization and Identity for Agents: What the Big Three Got Right (and What's Still Missing)"
- "The Hardest Problem in Enterprise Agents Isn't the Model — It's Identity"
- "Agent Identity in 2026: Vendor Approaches, Emerging Standards, and What Actually Works"

**Structure**:
1. Hook: Why traditional IAM fails for agents (NHI stats, the RBAC breaking point)
2. The taxonomy: 5 types of agent authorization (framework for thinking about the problem)
3. Vendor deep-dive: Auth0 vs Entra Agent ID vs AWS AgentCore (compare approaches, not just features)
4. Protocol layer: How MCP and A2A handle auth differently and why you need both
5. Emerging standards: IETF drafts (AIMS, AIP, OAuth extension), Grantex — the fragmentation risk
6. Payment protocols as the leading edge of agent authorization
7. HITL patterns that actually work (not prompt-based theater)
8. What's still missing: cross-vendor federation, permission lifecycle, agent deprecation

**Best first format**: Blog post (deep technical content) → LinkedIn carousel (vendor comparison visual) → LinkedIn text post (HITL anti-pattern hot take)
