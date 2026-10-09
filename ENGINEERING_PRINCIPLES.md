# UnvibeCode Engineering Approach

## Five Dimensions of a Workflow

UnvibeCode describes a workflow across five complementary dimensions, separating **business intent** from **technical execution**.

| Dimension | Question | Example |
| --- | --- | --- |
| ⚙️ **Runtime** | How does it execute? | REST request, queue event, cron job |
| 💼 **Domain** | What business operation occurs? | Calculate tax, issue refund |
| 🗄️ **State** | What data or lifecycle state changes? | Order `Pending → Shipped`, ledger update |
| 🛣️ **Path** | How does execution move between components? | Middleware, services, retries, external calls |
| 👤 **Actor** | Who initiates it, and under what authority? | Customer, admin, service account |

The dimensions are **complementary rather than strictly orthogonal**: one workflow may span multiple actors or execution paths.

## Engineering Principles

### 1. Separation of Concerns

Classify *how* a workflow runs separately from *what* it does. For example, moving a refund workflow from a serverless function to a container should not inherently change its refund rules or state invariants. The classification helps expose unwanted coupling; it does not guarantee zero migration changes.

### 2. Managing Complexity in AI-Generated Code

Fast code generation can mix transport logic, business decisions and state mutations. The five dimensions provide an explicit review framework to identify such mixing, locate dependencies and guide focused changes rather than treating generated code as an undifferentiated whole.

### 3. Domain-Driven Design (DDD) and Clean Architecture

Keep domain behavior understandable independently of infrastructure. For instance, `IssueRefund()` expresses business intent, while the runtime, persistence and routing layers determine how that intent executes. The taxonomy helps *describe and assess* these boundaries; it does not by itself enforce pure functions or clean architecture.

**Principle:** Describe the workflow across independent concerns first; then trace the supporting code and verify the behavior against requirements and evidence.
