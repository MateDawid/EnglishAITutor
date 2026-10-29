---
name: write-architecture
description: "Use when asked to create or update an architecture document or ADR using this repository’s architecture workflow."
argument-hint: "Describe the application or feature to document"
---

# Architecture and ADR authoring

Create or update concise, implementation-oriented architecture documentation through an interactive, approval-based workflow. Ask questions and get agreement at each design stage; do not silently make product or architecture decisions for the user.

## Workflow

1. **Inspect the repository and documentation**
   - Identify whether the user wants a new architecture, an update to an existing one, or an architecture for a particular feature.
   - Read the existing architecture document, ADRs, repository guidance, and relevant implementation when the requested documentation must match an existing system.
   - Preserve existing conventions and ADR numbering. Distinguish current implementation from target design; never present a proposal as already implemented.
   - If the requested output pattern is unclear, show the recognized structure and ask the user to confirm or correct it before drafting.

2. **Ask about the application or feature first**
   - Start by asking what application or feature this architecture should describe, its users, and the problem it solves.
   - For an existing architecture, ask which part should change and whether the document should describe current behavior, a target design, or both.
   - Do not start drafting models or endpoints until the scope is understood.

3. **Gather design requirements**
   - Ask for functional requirements: user-visible capabilities and important business rules.
   - Ask for non-functional requirements: relevant security, privacy, reliability, performance, accessibility, operations, scale, and delivery-quality goals.
   - Ask about external integrations, supported clients/protocols, and deployment assumptions when they materially affect the design.
   - Do not invent numeric service levels, technologies, or infrastructure. Capture goals now and defer detailed choices unless the user already knows them.
   - Summarize the requirements for user confirmation before proceeding.

4. **Propose the data model**
   - Propose domain entities and their relationships based on the confirmed requirements.
   - Use a table for each entity with columns for field, database type, and constraints; include meaningful enums and relationship semantics where relevant.
   - Include a Mermaid `erDiagram` showing entity relationships.
   - Keep field-level detail in this section when it helps an implementation agent understand persistence; do not add implementation-specific ORM or migration instructions.
   - Ask the user to confirm or correct the proposal before defining the API.

5. **Propose the API design**
   - Group endpoints by service or domain responsibility.
   - For every endpoint, state method/path, goal, an example request, and an example response. Include HTTP status only where useful and known.
   - Cover every required user-facing operation, including non-HTTP protocols such as WebSocket when applicable.
   - Keep examples representative and short; do not turn the architecture into a full OpenAPI specification. Defer validation edge cases, exhaustive errors, and transport-level mechanics unless the user asks for them.
   - Mark endpoint behavior as current or target when there is a difference. Ask for approval before moving on.

6. **Create diagrams**
   - Draw a high-level Mermaid system diagram showing the client, ingress or API boundary, application services, primary data stores, and confirmed external integrations. Connect ingress to the application boundary rather than drawing a cluttered edge to every service.
   - Do not add components such as Redis, S3, queues, or a specific cloud platform unless they are confirmed requirements. Deployment-specific boundaries may be shown generically and labeled as such.
   - Add a Mermaid sequence diagram for each protocol used by the application, such as HTTPS and WSS. Show the normal request path, authentication/authorization boundary, service work, data access, external calls, and response/streaming path.
   - Keep diagrams consistent with the accepted endpoint/API descriptions and data model. Ask the user to review them before finalizing.

7. **Record architecture decisions**
   - Use ADRs for significant decisions the user has accepted, not for undecided options or routine implementation details.
   - For each needed decision, explain the context and meaningful trade-offs, ask the user to choose, then record the accepted choice and consequences.
   - Follow the repository's ADR naming and format. Determine the next number by inspecting existing files; do not overwrite or renumber existing ADRs.
   - Link accepted ADRs from the relevant architecture section. If a decision remains open, state that it is deferred rather than writing an accepted ADR.

8. **Write, review, and validate**
   - Only edit documentation after the relevant content has been confirmed. For updates, preserve unrelated content and integrate existing changes.
   - Use the architecture section pattern below unless the repository already has an established alternative:
     1. Design requirements (functional and non-functional)
     2. Data model (detailed entity tables and relationship diagram)
     3. API design (services, endpoint goals, and examples)
     4. High-level system architecture (component diagram and protocol flows)
   - Keep the document a starting point for implementation: explicit about capabilities and relationships, concise about mechanisms that can be decided during development.
   - Check that all required endpoints and entities are represented, that target/current state is clear, and that Mermaid and Markdown are well formed. Run documentation checks only if the repository provides them.
   - Summarize changed files and any decisions intentionally left open.
