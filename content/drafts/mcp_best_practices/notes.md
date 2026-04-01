# MCP best practices - research notes

## Legend

- `**[MOST IMPORTANT]**` = candidate fragment for the final article thesis or takeaway
- `Source:` lines = supporting link for the claim directly above

## Working thesis

**[MOST IMPORTANT]**

MCP is most useful when it exposes a capability that helps an agent complete a real job, not when it mirrors REST or GraphQL endpoints 1:1.

**[MOST IMPORTANT]** Editorial focus for this article: `tool pollution` means loading too many MCP tools into the agent and degrading tool selection quality, latency, and reasoning reliability. The security angle is real, but should only be mentioned briefly here and expanded in a separate article.

The article should argue for an "agent-first interface" mindset:

- MCP is a protocol for capability discovery and invocation.
- A good MCP server is closer to a product interface for an agent than to a thin transport wrapper.
- In enterprise settings, the hard problems for this article are tool shape, context budget, capability packaging, and avoiding tool pollution; security should be acknowledged, but not centered.

## My starting intuition that looks correct

- MCP is not for wrapping every endpoint.
- The server should expose what the user actually wants to get done.
- It can wrap a workflow composed of multiple API calls.
- It can wrap an agentic workflow or graph with internal prompts, logic, retries, and data-source calls.

## Strong article angle

Possible core message:

**[MOST IMPORTANT]**

"MCP is not your public API with a new transport. It is your agent interface. Design it around outcomes, trust boundaries, and context budget."

Possible title directions:

- MCP best practices for enterprise teams: design capabilities, not wrappers
- MCP is not your REST facade: what production-grade servers actually need
- Too many MCP tools make agents worse: how to avoid tool pollution

## Claim set with evidence and pushback

### 1. MCP should expose capabilities, not raw endpoints

**[MOST IMPORTANT]** Default to capabilities over raw operations. Expose endpoints directly only when the agent genuinely benefits from flexible composition.

Support:

- Phil Schmid argues that most bad MCP servers fail because developers treat MCP like a REST wrapper instead of an interface for agents.  
  Source: [Phil Schmid - MCP is Not the Problem, It's your Server](https://www.philschmid.de/mcp-best-practices)
- Block Engineering says to design top-down from workflows, not bottom-up from endpoints.  
  Source: [Block's Playbook for Designing MCP Servers](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)
- Docker makes the same point using "tool budget": one tool per endpoint usually overloads the agent.  
  Source: [Docker - 5 Best Practices for Building, Testing, and Packaging MCP Servers](https://www.docker.com/blog/mcp-server-best-practices/)

Why this matters:

- Fewer tool calls
- Smaller context footprint
- Less orchestration burden on the model
- Better reliability because the deterministic code owns the workflow

Lead engineer pushback:

- Do not overstate this as "low-level tools are always wrong."
- Low-level tools still make sense for expert domains where the agent genuinely needs flexible composition:
  - SQL querying
  - GraphQL read access
  - file system operations
  - code search / code edit primitives
- The better framing is: default to outcomes, and only expose lower-level composable tools when the workflow space is genuinely broad and the agent benefits from that flexibility.

How to use this in the article:

- "Don't expose `coin_search`, `coin_current_price`, `coin_news`, `coin_github_stats` if the real user intent is `analyze_crypto_project`."
- "Let the MCP tool hide orchestration and return a useful decision-oriented artifact."

### 2. Design from the user workflow backward

Support:

- Block: start from the workflow to automate and work backward in as few steps as possible.  
  Source: [Block's Playbook for Designing MCP Servers](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)
- Phil Schmid: outcome-oriented tools beat operation-oriented tools.  
  Source: [Phil Schmid - MCP is Not the Problem, It's your Server](https://www.philschmid.de/mcp-best-practices)
- Docker: prompts and tool grouping can hide multi-step complexity from the user and agent.  
  Source: [Docker - 5 Best Practices for Building, Testing, and Packaging MCP Servers](https://www.docker.com/blog/mcp-server-best-practices/)

Rationale:

- The workflow defines what data is necessary.
- The workflow defines what can be hidden behind the tool.
- The workflow defines where guardrails and approvals belong.

Lead engineer pushback:

- "Workflow" can become a vague buzzword.
- The article should force every proposed tool through a test:
  - What is the user trying to accomplish?
  - What would success look like?
  - What minimum inputs are really needed?
  - What internal steps should remain invisible to the model?

### 3. Tool names, schemas, descriptions, and errors are part of the interface

Support:

- Phil Schmid: instructions are context; docstrings and errors actively shape the next model action.  
  Source: [Phil Schmid - MCP is Not the Problem, It's your Server](https://www.philschmid.de/mcp-best-practices)
- Block: names and parameters act like prompts, so experiment with them.  
  Source: [Block's Playbook for Designing MCP Servers](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)
- Docker: document for both humans and agents.  
  Source: [Docker - 5 Best Practices for Building, Testing, and Packaging MCP Servers](https://www.docker.com/blog/mcp-server-best-practices/)
- MCP docs and blog: tool annotations give clients a risk vocabulary, but they are only hints.  
  Sources: [MCP blog - Tool Annotations as Risk Vocabulary](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/), [MCP docs - Understanding Authorization in MCP](https://modelcontextprotocol.io/docs/tutorials/security)

Best-practice implications:

- Use explicit, action-oriented names.
- Use flat, typed inputs where possible.
- Prefer bounded enums and clear descriptions over nested "config" objects.
- Make error messages agent-recoverable, not just human-readable.

Example:

- Bad: `run_analysis(payload: dict)`
- Better: `analyze_crypto_project(project_name: str, thesis: str | None = None, horizon: Literal["short","mid","long"] = "long")`

Lead engineer pushback:

- Be careful not to turn descriptions into mini-prompts full of policy, examples, and hidden logic.
- Overly long tool descriptions increase token cost and create more prompt-injection surface.
- The right balance is short, concrete, and operational.

### 4. Tool pollution: too many tools degrade agent quality

Support:

- Phil Schmid recommends roughly 5-15 tools per server and aggressive curation.  
  Source: [Phil Schmid - MCP is Not the Problem, It's your Server](https://www.philschmid.de/mcp-best-practices)
- Block emphasizes token budget and explicit handling of large outputs.  
  Source: [Block's Playbook for Designing MCP Servers](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)
- Docker uses the phrase "tool budget" and warns against overloaded servers.  
  Source: [Docker - 5 Best Practices for Building, Testing, and Packaging MCP Servers](https://www.docker.com/blog/mcp-server-best-practices/)
- MetaTool Benchmark shows that LLMs still struggle with the basic meta-problem of deciding whether to use tools and which tool to select from a set of candidates.  
  Source: [MetaTool Benchmark for Large Language Models: Deciding Whether to Use Tools and Which to Use](https://arxiv.org/abs/2310.03128)
- ToolRet shows that once toolsets become large, retrieval itself becomes a first-class problem; poor retrieval quality directly lowers downstream task pass rates for tool-using LLMs.  
  Source: [Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models](https://arxiv.org/abs/2503.01763)
- Toolshed explicitly frames scaling tool capacity beyond agent reasoning or model limits as a challenge and proposes retrieval + ranking to manage the trade-off between retrieval accuracy, agent performance, and token cost.  
  Source: [Toolshed: Scale Tool-Equipped Agents with Advanced RAG-Tool Fusion and Tool Knowledge Bases](https://arxiv.org/abs/2410.14594)
- ScaleMCP argues that manual monolithic tool repositories do not scale cleanly and proposes dynamic MCP tool retrieval and synchronization instead.  
  Source: [ScaleMCP: Dynamic and Auto-Synchronizing Model Context Protocol Tools for LLM Agents](https://arxiv.org/abs/2505.06416)

Implications:

**[MOST IMPORTANT]** Too many tools do not just make the interface ugly. They actively make the agent worse at choosing, grounding, and parameterizing the right action.

- One server, one job or one trust boundary.
- Avoid kitchen-sink servers.
- Paginate, truncate, or summarize large outputs.
- Return the minimum data needed for the next reasoning step.

What "tool pollution" looks like in practice:

- the agent picks the wrong tool even though the right one is installed
- the agent confuses two similar tools with overlapping descriptions
- the agent uses a generic tool when a specific high-signal tool exists
- the agent hallucinates parameters because too many schemas look similar
- the prompt/context budget gets consumed by tool metadata instead of the task
- latency rises because retrieval, ranking, or repeated retries become necessary

Why the quality drops:

- more tool descriptions compete for limited context
- overlapping tools increase ambiguity
- weak descriptions make retrieval worse
- larger tool inventories create a retrieval problem before the reasoning problem
- the model now has to solve "which tools matter?" before it can solve the user task

Lead engineer framing:

**[MOST IMPORTANT]** Tool pollution is not mainly a UX complaint. It is a systems-quality problem: precision of tool selection falls as the searchable tool universe gets noisier.

Good article formulation:

- "Adding more MCP tools can reduce agent quality if discovery and retrieval quality do not improve at the same time."
- "A large tool universe needs ranking, filtering, or capability packaging. Dumping everything into the prompt is not a scalable strategy."
- "The practical goal is not maximum tool count. It is maximum task success under bounded context and bounded ambiguity."

Lead engineer pushback:

- "5-15 tools" is practical guidance, not a protocol law.
- Some domains need more tools, but only if discovery remains usable.
- The better principle is: every additional tool must earn its place by improving task success more than it harms discovery.

What to recommend instead of loading everything:

- package low-level operations behind higher-level capability tools
- split servers by domain, persona, or trust boundary
- use retrieval / top-k filtering for large internal tool catalogs
- expose a small default surface and progressively disclose more tools when needed
- reduce semantic overlap between tool names and descriptions
- remove stale, duplicate, or weakly differentiated tools

### 5. Return useful outputs, not giant blobs

Support:

- Phil Schmid warns against data-dump services.  
  Source: [Phil Schmid - MCP is Not the Problem, It's your Server](https://www.philschmid.de/mcp-best-practices)
- Block recommends pagination, truncation, and recoverable errors for large outputs.  
  Source: [Block's Playbook for Designing MCP Servers](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)
- OWASP warns that tool outputs are also an injection surface and must be treated as untrusted.  
  Source: [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)

Practical guidance:

- Prefer concise, decision-ready outputs.
- Include citations or provenance where trust matters.
- Paginate large result sets.
- For enterprise tools, consider structured summaries plus source references, not raw JSON dumps.

Lead engineer pushback:

- Over-summarization can hide useful evidence.
- If the article recommends concise outputs, it should also recommend a retrieval path for drill-down:
  - summary tool first
  - details tool or page token second

### 6. Security note, but not the main article

This material is important, but based on the current editorial direction it should not dominate this article.

Recommended treatment:

- mention in 1 short section or 1 short sidebar
- frame it as "important enough for a separate article"
- keep the main article focused on design quality, tool overload, and capability packaging

Support:

- Simon Willison highlights prompt injection, tool poisoning, rug pulls, and dangerous tool combinations.  
  Source: [Simon Willison - Model Context Protocol has prompt injection security problems](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)
- OWASP MCP Security Cheat Sheet covers least privilege, tool schema review, sandboxing, human approval, validation, transport security, multi-server isolation, and logging.  
  Source: [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)
- GitHub emphasizes OAuth 2.1, audience/resource validation, multi-tenant isolation, secrets management, and gateway patterns for remote MCP servers.  
  Source: [GitHub Blog - How to build secure and scalable remote MCP servers](https://github.blog/ai-and-ml/generative-ai/how-to-build-secure-and-scalable-remote-mcp-servers/)
- Block security notes that identity, user context, and agent context all matter.  
  Source: [Block Engineering - Securing the Model Context Protocol](https://engineering.block.xyz/blog/securing-the-model-context-protocol)

What not to overclaim:

- MCP is not uniquely insecure. Many of these risks exist for any LLM tool-use system.
- But MCP makes composition easy, which increases the chance of risky combinations if governance is weak.

Key enterprise practices to include:

- Least-privilege scopes and per-server credentials
- Human approval for destructive or sensitive actions
- Treat tool outputs and web content as untrusted
- Sandboxing and containerization for local servers
- Strong auth and authorization for remote servers
- Audit logs and correlation IDs
- Supply-chain review for third-party servers
- Separate read-only tools from write / destructive tools when possible

### 6a. Separate article idea: tool poisoning and MCP security

This is useful research material, but it should not be the core of this article because it addresses a different question than "does loading too many tools make the agent worse?"

Important distinction for the article:

- "Tool budget pollution" = too many tools, too much interface clutter, degraded discovery.
- "Tool poisoning" = malicious instructions embedded in tool metadata, tool outputs, or adjacent shared context that manipulate agent behavior.

The stronger research literature is around **tool poisoning** and **indirect prompt injection**, not around the phrase "tool pollution" itself.

#### Why this matters

- MCP clients expose tool names, descriptions, schemas, and outputs to the model as context.
- That means the tool interface itself becomes part of the attack surface.
- A malicious or compromised server does not necessarily need to execute its own tool to cause harm; it may only need to shape the model's behavior toward other, more privileged tools.

#### Strong supporting evidence from practice

- Invariant Labs documented Tool Poisoning Attacks where hidden instructions in tool descriptions can cause sensitive file reads, exfiltration, and cross-server behavior hijacking.  
  Source: [Invariant Labs - MCP Security Notification: Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- Simon Willison describes the same family of problems using the MCP lens: rug pulls, tool shadowing, and dangerous combinations of private data access, untrusted input, and exfiltration channels.  
  Source: [Simon Willison - Model Context Protocol has prompt injection security problems](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)
- OWASP MCP guidance now treats tool descriptions, schemas, and outputs as injection surfaces, not just the natural-language chat prompt.  
  Source: [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)

#### Strong supporting evidence from papers

- **MCP-ITP (2026)** studies implicit tool poisoning in MCP, where the poisoned tool does not need to be invoked; instead it nudges the agent into using a legitimate high-privilege tool. Reported results: up to **84.2% attack success rate** with malicious tool detection as low as **0.3%**.  
  Source: [MCP-ITP: An Automated Framework for Implicit Tool Poisoning in MCP](https://arxiv.org/abs/2601.07395)
- **Systematic Analysis of MCP Security (2025)** introduces an MCP attack library with **31 distinct attack methods** and highlights agents' blind reliance on tool descriptions, chain attacks via shared context, and difficulty distinguishing data from executable instructions.  
  Source: [Systematic Analysis of MCP Security](https://arxiv.org/abs/2508.12538)
- **MCP at First Glance (2025)** is especially valuable because it is not just a toy attack paper; it is a large empirical study of **1,899 open-source MCP servers**. It reports **7.2%** of servers with general vulnerabilities and **5.5%** with MCP-specific tool poisoning.  
  Source: [Model Context Protocol (MCP) at First Glance: Studying the Security and Maintainability of MCP Servers](https://arxiv.org/abs/2506.13538)
- **InjecAgent (2024)** predates the MCP-specific papers but is foundational because it benchmarks indirect prompt injection against tool-integrated agents using **1,054 test cases**, **17 user tools**, and **62 attacker tools**. It reports ReAct-prompted GPT-4 vulnerable **24%** of the time, rising to **47%** with reinforced attacker prompts.  
  Source: [InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents](https://arxiv.org/abs/2403.02691)
- **Adaptive Attacks Break Defenses (2025)** is useful because it weakens any naive "we'll just add a classifier" defense story. The paper evaluates **8 defenses** and reports bypassing all of them with adaptive attacks, with **over 50%** attack success rate.  
  Source: [Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents](https://arxiv.org/abs/2503.00061)
- **Silent Egress (2026)** matters because it shows exfiltration can be caused by seemingly low-level web metadata such as titles, snippets, and URL previews. In **480 runs**, the attack succeeded with **P(egress)=0.89**, and **95%** of successful attacks were not detected by output-based safety checks.  
  Source: [Silent Egress: When Implicit Prompt Injection Makes LLM Agents Leak Without a Trace](https://arxiv.org/abs/2602.22450)
- **Large-scale public competition results (2026)** are helpful because they show this is not a lab curiosity tied to one model. Across **272,000 attack attempts**, **13 frontier models**, and **41 scenarios**, all models remained vulnerable.  
  Source: [How Vulnerable Are AI Agents to Indirect Prompt Injections? Insights from a Large-Scale Public Competition](https://arxiv.org/abs/2603.15714)

#### Strong supporting evidence for defensive design

- **Prompt Flow Integrity (PFI)** is one of the better references for a systems-style response rather than prompt-only hardening. It argues for isolation, secure handling of untrusted data, and privilege-escalation guardrails. It reports Secure Utility Rate gains and reduces Attacked Task Rate to **zero** on the evaluated benchmarks.  
  Source: [Prompt Flow Integrity to Prevent Privilege Escalation in LLM Agents](https://arxiv.org/abs/2503.15547)

#### What a skeptical lead engineer should conclude

Tool poisoning is not a niche edge case and not just "MCP drama on X". There is now converging evidence from:

- real attack writeups
- MCP-specific attack papers
- broad prompt-injection benchmarks
- large-scale empirical studies of open-source MCP servers
- papers showing many existing defenses fail under adaptive pressure

#### How to phrase this in the article without overselling

- Good: "Tool poisoning turns MCP interface metadata into part of the attack surface."
- Good: "MCP did not invent indirect prompt injection, but it makes the tool layer standardized, portable, and therefore easier to study, attack, and defend."
- Good: "Enterprise adoption needs controls at the architecture and policy layer, not only better prompting."
- Avoid: "MCP is broken by design."
- Avoid: "All third-party MCP servers are unsafe."

#### Concrete recommendations if this becomes a separate article

- Treat tool descriptions, schemas, and outputs as untrusted inputs unless the server is explicitly trusted.
- Separate open-world retrieval tools from sensitive action tools where possible.
- Avoid mixing private-data access, untrusted content ingestion, and outbound communication in the same unconstrained execution path.
- Use least-privilege tokens and per-tool/per-server scopes.
- Require human approval for destructive, data-sharing, or high-impact operations.
- Prefer deterministic policy and isolation controls over prompt-only defenses.
- Review third-party MCP servers as supply-chain dependencies, not just convenience plugins.

### 7. Tool annotations help, but they are not guarantees

**[MOST IMPORTANT]** Tool annotations are useful hints for UX and policy, not a security guarantee.

Support:

- The MCP blog explicitly says annotations are hints, not enforceable truth.  
  Source: [MCP blog - Tool Annotations as Risk Vocabulary](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)
- The defaults are deliberately pessimistic: missing annotations should not be interpreted as safe.  
  Source: [MCP blog - Tool Annotations as Risk Vocabulary](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)

Why this matters:

- `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` are useful for approvals and UX.
- They should inform policy, not replace deterministic controls.

Lead engineer pushback:

- Do not write "annotations solve security."
- The real guarantees come from authorization, sandboxing, network controls, and approval flows.

### 8. Transport and deployment model matter

What looks safe to say:

- Local stdio servers and remote HTTP servers have different security and auth needs.  
  Source: [MCP docs - Understanding Authorization in MCP](https://modelcontextprotocol.io/docs/tutorials/security)
- MCP docs recommend OAuth-based authorization for remote protected servers.  
  Source: [MCP docs - Understanding Authorization in MCP](https://modelcontextprotocol.io/docs/tutorials/security)
- Docker strongly favors containerized packaging for portability and isolation.  
  Source: [Docker - 5 Best Practices for Building, Testing, and Packaging MCP Servers](https://www.docker.com/blog/mcp-server-best-practices/)
- GitHub argues for gateway-style remote deployments once scale, auth, and policy matter.  
  Source: [GitHub Blog - How to build secure and scalable remote MCP servers](https://github.blog/ai-and-ml/generative-ai/how-to-build-secure-and-scalable-remote-mcp-servers/)

What to verify before publish:

- Transport guidance is evolving quickly.
- Re-check the latest MCP spec / SDK docs before making a strong claim about SSE vs Streamable HTTP.
- Current draft wording should avoid "always use X transport" unless revalidated.

## How this maps to my `agent-patterns-lab` example 02

Project reference:

[Example 02 repository folder](https://github.com/ksopyla/agent-patterns-lab/tree/main/examples/02-mcp-tool-integration)

### What the example gets right

**[MOST IMPORTANT]** Example 02 is good evidence for the "capability over endpoint" argument because it exposes one high-level tool and hides the orchestration graph behind it.

- It exposes a high-level capability: `research_crypto_project`.
- It hides internal orchestration behind the MCP interface.
- The same LangGraph pipeline powers both REST and MCP entry points.
- The planner turns raw user intent into structured downstream research tasks.
- CoinGecko and DuckDuckGo remain internal dependencies rather than being exposed as separate MCP tools.
- The tests cover node behavior and graph execution, including graceful degradation.

Sources:

- [Example 02 README](https://raw.githubusercontent.com/ksopyla/agent-patterns-lab/main/examples/02-mcp-tool-integration/README.md)
- [MCP server implementation](https://raw.githubusercontent.com/ksopyla/agent-patterns-lab/main/examples/02-mcp-tool-integration/src/mcp_servers/crypto_intelligence.py)
- [Graph wiring](https://raw.githubusercontent.com/ksopyla/agent-patterns-lab/main/examples/02-mcp-tool-integration/src/agents/graph.py)
- [E2E graph test](https://raw.githubusercontent.com/ksopyla/agent-patterns-lab/main/examples/02-mcp-tool-integration/tests/e2e/test_pipeline_graph.py)

This is the strongest evidence for the article's main point:

- the external interface is the capability
- the internal data-fetching and orchestration are implementation details

### What I would challenge before calling it "enterprise-ready"

**[MOST IMPORTANT]** The demo has the right external shape, but still lacks several production concerns: tighter contracts, auth/authz, approval flows, provenance, and explicit treatment of untrusted web data.

#### 1. The MCP tool contract is still too loose

- The MCP tool accepts `query: str` with no min/max constraints.
- The REST API validates input length, but the MCP entry point does not mirror that discipline.
- For production, the MCP schema should be as intentional as the REST schema or better.

Sources:

- [REST request model with min/max validation](https://raw.githubusercontent.com/ksopyla/agent-patterns-lab/main/examples/02-mcp-tool-integration/src/app.py)
- [MCP tool signature using free-form query](https://raw.githubusercontent.com/ksopyla/agent-patterns-lab/main/examples/02-mcp-tool-integration/src/mcp_servers/crypto_intelligence.py)

#### 2. Auth, identity, and approval are not addressed

- Fine for a demo.
- Not enough for enterprise remote use.
- Missing pieces:
  - user identity
  - per-user authorization
  - approval for risky actions
  - audit trail
  - rate limiting / quotas

#### 3. Open-world data sources create prompt-injection risk

- News and community nodes pull untrusted web content.
- The system currently relies on prompting and synthesis discipline, but not on strong taint boundaries.
- Simon Willison and OWASP would both push hard on this.

Sources:

- [News scanner uses DuckDuckGo web search](https://raw.githubusercontent.com/ksopyla/agent-patterns-lab/main/examples/02-mcp-tool-integration/src/agents/news_scanner.py)
- [Community analyst uses DuckDuckGo social search](https://raw.githubusercontent.com/ksopyla/agent-patterns-lab/main/examples/02-mcp-tool-integration/src/agents/community_analyst.py)
- [Simon Willison on MCP prompt injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)
- [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)

#### 4. The tool returns only a final free-form report

- Good for simplicity.
- But enterprise users may also want:
  - citations
  - freshness timestamps
  - source provenance
  - structured machine-readable fields

Potential improvement:

- return a concise report plus a compact source list
- or provide a second drill-down tool for evidence retrieval

#### 5. Tool risk metadata is missing

- The tool is effectively read-only from the user's system perspective.
- But it is also `open world` because it consumes external web data.
- Adding annotations and clear server instructions would improve approval UX in clients that honor them.

Sources:

- [MCP blog - Tool Annotations as Risk Vocabulary](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)
- [MCP server implementation](https://raw.githubusercontent.com/ksopyla/agent-patterns-lab/main/examples/02-mcp-tool-integration/src/mcp_servers/crypto_intelligence.py)

#### 6. Deployment defaults are demo-friendly, not enterprise-friendly

- `0.0.0.0` binding is normal in Docker demos, but dangerous if copied blindly.
- There is no remote auth flow, TLS story, or secret-management story here.
- Good article opportunity: "patterns that are valid in a learning repo, but incomplete in production."

#### 7. There is a small but important naming mismatch

- The README emphasizes `research_crypto_project(project_name)`.
- The actual tool currently accepts `query: str`.
- Not a major bug, but it weakens the "tight tool contract" story.

Sources:

- [README wording](https://raw.githubusercontent.com/ksopyla/agent-patterns-lab/main/examples/02-mcp-tool-integration/README.md)
- [Actual tool signature](https://raw.githubusercontent.com/ksopyla/agent-patterns-lab/main/examples/02-mcp-tool-integration/src/mcp_servers/crypto_intelligence.py)

### Best way to use example 02 in the article

**[MOST IMPORTANT]** Present example 02 as a good capability-first MCP design and, at the same time, as a useful illustration of what still has to be added before an enterprise team should trust it in production.

Position it as:

- a good example of capability-first MCP design
- a good example of hiding orchestration behind one tool
- a deliberately incomplete enterprise implementation that still needs auth, security, and governance layers

That nuance is important. It keeps the article honest.

## Crypto example framing for the article

Bad MCP design:

- `coin_search`
- `coin_current_price`
- `coin_recent_news`
- `coin_github_activity`
- `coin_categories`

Why it is weak:

- pushes orchestration onto the model
- increases tool count
- increases context cost
- exposes internal plumbing rather than user intent

Better MCP design:

**[MOST IMPORTANT]** The crypto case makes the design principle concrete: do not expose coin-data plumbing when the real user intent is investment-grade project analysis.

- `analyze_crypto_project`
- maybe `compare_crypto_projects`
- maybe `evaluate_entry_timing`

What the tool should return:

- executive summary
- market / project snapshot
- recent developments
- community and developer health
- risks and unknowns
- recommendation framing with confidence and evidence

## Best practices list to collect into the draft

### Design

**[MOST IMPORTANT]**

- Design from the job-to-be-done, not the endpoint list.
- Prefer capabilities over operations by default.
- Keep each server focused on one domain and one trust boundary.
- Hide internal orchestration in deterministic code where possible.

### Interface quality

- Use short, explicit, action-oriented tool names.
- Flatten arguments and bound them with types, enums, and limits.
- Keep descriptions concrete and operational.
- Return outputs that help the next reasoning step.
- Add pagination or truncation for large results.
- Make errors recoverable and instructional.

### Security and governance

**[MOST IMPORTANT]**

- Treat all model-generated inputs as untrusted.
- Treat tool outputs as untrusted, especially from web or external systems.
- Use least-privilege credentials and per-server scopes.
- Require user approval for destructive or sensitive actions.
- Sandbox local servers and isolate remote servers.
- Review tool schemas and dependencies as part of supply-chain security.
- Log tool calls with user context, parameters, timestamps, and correlation IDs.

### Enterprise operations

- Add OAuth-based auth for remote protected servers.
- Validate token audience / resource and issuer.
- Separate user identity from agent identity and server identity where possible.
- Add rate limits, quotas, retries, and circuit breakers.
- Use secret managers instead of plaintext env/config for production deployments.
- Add observability for latency, failure modes, and unusual tool-call patterns.

### Testing

- Test connection and discovery, not just tool logic.
- Test approval flows and error paths.
- Test tool descriptions and schemas with a real MCP client.
- Test prompt-injection scenarios when tools touch open-world data.

## Important caveats to keep the article credible

- Do not claim that "MCP replaces APIs." MCP usually wraps or composes APIs, services, CLIs, or workflows.
- Do not claim that "one tool is always better." Sometimes expert, composable primitives are the correct shape.
- Do not claim that annotations are trustworthy by themselves.
- Do not imply that auth is required for every local MCP server. The stronger claim is: remote protected enterprise servers need proper auth and authz.
- Do not treat directory or marketplace requirements as protocol laws.

## Named sources and supporting voices

### Product / interface design

- Phil Schmid - "MCP is Not the Problem, It's your Server"
  https://www.philschmid.de/mcp-best-practices

- Block Engineering - "Block's Playbook for Designing MCP Servers"
  https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers

- Docker - "5 Best Practices for Building, Testing, and Packaging MCP Servers"
  https://www.docker.com/blog/mcp-server-best-practices/

### Security / governance

- Simon Willison - "Model Context Protocol has prompt injection security problems"
  https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/

- OWASP MCP Security Cheat Sheet
  https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html

- GitHub Blog - "How to build secure and scalable remote MCP servers"
  https://github.blog/ai-and-ml/generative-ai/how-to-build-secure-and-scalable-remote-mcp-servers/

- Block Engineering - "Securing the Model Context Protocol"
  https://engineering.block.xyz/blog/securing-the-model-context-protocol

### Spec / official docs

- MCP docs - authorization tutorial and pitfalls
  https://modelcontextprotocol.io/docs/tutorials/security

- MCP blog - tool annotations as risk vocabulary
  https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/

- Anthropic support - best practices for building MCP servers
  https://support.anthropic.com/en/articles/11596040-best-practices-for-building-mcp-servers

## Questions to answer with Krzysztof before turning this into full draft prose

- Is the article mainly about MCP server design, or do you want equal weight on enterprise security and governance?
- Should `agent-patterns-lab` example 02 be the main running case study throughout the piece?
- Do you want a more opinionated stance against thin wrapper servers, or a more balanced "sometimes valid, often wrong" framing?
- Do you want to include a concrete enterprise checklist table at the end?

## Best next move

Turn these notes into:

1. a lean `index.md` blog draft with 5-7 sections
2. one repeated case study: `research_crypto_project`
3. a final section called something like "What changes between demo MCP and enterprise MCP"