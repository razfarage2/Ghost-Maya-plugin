# Clean Architecture 
## Book Map

- **Part I - Introduction**: Why architecture matters and why structure is a business value.
- **Part II - Starting with the Bricks: Programming Paradigms**: How structured, object-oriented, and functional programming constrain programmers in useful ways.
- **Part III - Design Principles**: SOLID principles as class/module-level rules for change control and dependency management.
- **Part IV - Component Principles**: Cohesion and coupling principles for packaging, release, reuse, stability, and component dependency graphs.
- **Part V - Architecture**: Boundaries, policies, use cases, clean architecture, services, tests, embedded architecture, and the Dependency Rule.
- **Part VI - Details**: Why databases, web, frameworks, and code organization are implementation details rather than the center of the system.
- **Part VII - Appendix**: Historical case studies that show the principles recurring across decades and system types.

---

# Part I - Introduction

## Chapter 1 - What Is Design and Architecture? - Part I

### Central argument

This chapter removes the artificial split between "design" and "architecture." Martin treats them as one continuous discipline: every decision, from major component structure down to small code organization, shapes the system. The real measure of architecture is not how impressive the diagrams look, but how much human effort is required to build, change, and maintain the system over time.

### Principles covered

- **Architecture and design are one continuum.** High-level component boundaries and low-level code choices are part of the same design fabric. A bad low-level dependency can damage architecture just as much as a bad top-level service split.
- **Architecture quality is measured by lifetime effort.** Good architecture keeps the cost of change low. If each release requires more people, more coordination, and more risk for less output, the architecture is failing.
- **Sustainable speed requires technical discipline.** The chapter rejects the idea that messiness is a short-term accelerator. In real systems, mess creates drag almost immediately.
- **Cleanliness is an economic property.** Code structure is not only aesthetic. It affects payroll, release speed, defect rate, morale, and the ability to respond to business change.

### Visual models and diagrams

- **House architecture analogy.** The chapter uses the idea of a building plan to show that architecture includes both visible structure and hidden details. Software is the same: component topology, dependency direction, data flow, class structure, and small implementation choices all participate.
- **Engineering staff growth vs productivity.** The book shows charts where team size increases while output flattens. Conceptually, this illustrates that adding people does not solve structural drag.
- **Cost per line and productivity decline.** The visual trend is: more releases create more mess, and the cost of each new change rises. The important relationship is not the exact numbers, but the curve: unmanaged complexity compounds.
- **TDD comparison chart.** The chapter uses a small experiment to support the claim that disciplined development can be faster even in short timeframes, not only over the long term.

### Key architectural concepts and terms

- **Architecture/design:** The total structure of the system across levels, from policies and components to code-level dependencies.
- **Lifetime cost:** The total human effort needed to deliver, maintain, modify, test, and deploy the system.
- **Productivity collapse:** The state where most team effort goes into navigating or patching the mess rather than delivering meaningful behavior.
- **Technical mess:** Accumulated poor structure that makes each future change harder than the last.

### Anti-patterns warned against

- **"We will clean it later."** Later rarely comes because feature pressure continues. The debt becomes part of the release process.
- **Heroic feature delivery over structural care.** Overtime and brute force hide architectural decline until changes become economically impossible.
- **Restart fantasy.** Starting over without changing discipline usually recreates the same failure in a new codebase.
- **Measuring progress only by staff size or activity.** More developers and more effort can coincide with less actual throughput.

### Actionable architectural guidance

- Track feature lead time and change cost, not just delivery dates.
- Treat rising coordination cost as an architectural smell.
- Keep code clean as part of delivery, not as a future cleanup phase.
- Make architecture decisions that reduce future effort, not only current implementation time.
- Avoid rewrites unless the team has a concrete plan to change the design discipline that caused the current mess.

### Connections to other chapters and to Clean Code

This chapter sets up the book's economic thesis: architecture exists to keep software changeable. It connects directly to Chapter 2's distinction between behavior and structure, Chapter 15's life-cycle view of architecture, and Chapter 28's emphasis on testability. It also extends *Clean Code*: clean functions and classes are not only local virtues; they are the small-scale foundation of architecture.

---

## Chapter 2 - A Tale of Two Values - Part I

### Central argument

Software has two values: what it does now and how easy it is to change later. Stakeholders often emphasize behavior because it is urgent, visible, and directly tied to business requests. Architecture is less urgent, but it is the value that preserves the ability to continue delivering behavior as requirements change.

### Principles covered

- **Behavior value.** The system must satisfy current requirements. This is necessary, but it is not sufficient.
- **Architecture value.** The system must remain soft: easy to reshape when business needs change.
- **Shape should not dominate scope.** A small requirement change should not become expensive just because it cuts against the system's current structure.
- **Important can lose to urgent.** Architecture work is often important but not immediately urgent, so teams must actively protect it.
- **Developers are stakeholders.** The development team has a duty to defend the system's long-term changeability, even when pressured by urgent features.

### Visual models and diagrams

- **Importance/urgency matrix.** The model separates urgent/important work from urgent/unimportant work. The key relationship is that features often appear urgent, while architecture often lacks urgency but carries high importance. The diagram teaches architects to avoid letting urgency erase structural responsibility.

### Key architectural concepts and terms

- **Behavior:** The visible functions the system performs for users and stakeholders.
- **Architecture/structure:** The internal arrangement that determines whether future changes are cheap or expensive.
- **Softness:** The ability of software to be changed with effort proportional to the real size of the change.
- **Scope vs shape:** Scope is how large the change is in business terms; shape is how well the request fits the current code structure.

### Anti-patterns warned against

- **Feature-first absolutism.** Treating every feature as more valuable than structure eventually destroys feature delivery itself.
- **Architectural passivity.** Waiting for nontechnical stakeholders to protect architecture is a mistake; they often cannot evaluate the risk until it is too late.
- **Confusing urgency with importance.** Teams may spend all their time on urgent tasks while the system decays.

### Actionable architectural guidance

- Discuss architecture in business language: change cost, risk, time-to-market, defect risk.
- Reserve capacity for structural work before the system becomes hard to change.
- Challenge feature plans that force the system into a bad shape.
- Make the cost of architectural neglect visible with trend data.
- Treat architecture defense as part of the architect's job, not as optional polish.

### Connections to other chapters and to Clean Code

This chapter provides the moral and business frame for the rest of the book. Chapter 15 expands it into development, deployment, operation, and maintenance. Chapter 17 shows how boundaries preserve changeability. *Clean Code* connects here because local mess reduces softness; poor naming, large functions, and hidden dependencies all make the shape of the system harder to change.

---

# Part II - Starting with the Bricks: Programming Paradigms

## Chapter 3 - Paradigm Overview - Part II

### Central argument

Architecture begins in code. The three major programming paradigms - structured, object-oriented, and functional programming - are not primarily about adding power; they impose useful constraints. Each removes a dangerous freedom and thereby makes larger systems more understandable and controllable.

### Principles covered

- **Structured programming disciplines direct control flow.** It limits arbitrary jumps and supports decomposable, testable functions.
- **Object-oriented programming disciplines indirect control flow.** It makes runtime polymorphism safe enough to use for dependency inversion and boundary crossing.
- **Functional programming disciplines assignment.** It reduces the risks caused by mutable state, especially in concurrent or distributed systems.
- **Paradigms are subtractive.** They help by restricting harmful practices, not by magically adding new computational capability.

### Visual models and diagrams

- This chapter is mainly conceptual rather than diagram-heavy. The model is a three-part relationship: structured programming supports function and algorithms; OO supports component separation; functional programming supports disciplined data handling.

### Key architectural concepts and terms

- **Programming paradigm:** A discipline that tells programmers which structures to prefer and which freedoms to avoid.
- **Direct transfer of control:** Explicit jumps or branching that can make logic hard to reason about.
- **Indirect transfer of control:** Calls through pointers, interfaces, virtual dispatch, or polymorphic mechanisms.
- **Assignment/mutation:** Changing stored values over time, creating temporal complexity.

### Anti-patterns warned against

- **Believing new paradigms solve architecture automatically.** Paradigms are disciplines; architecture still requires design decisions.
- **Ignoring constraints.** Uncontrolled jumps, unchecked function pointers, and uncontrolled mutable state all scale poorly.
- **Language worship.** The chapter implies that architecture is deeper than language choice.

### Actionable architectural guidance

- Use structured programming to keep algorithms decomposable and testable.
- Use polymorphism to invert dependencies across architectural boundaries.
- Localize mutable state and prefer immutable data where possible.
- Treat paradigms as design constraints, not slogans.
- Ask what freedom each architectural rule removes and what risk that removal controls.

### Connections to other chapters and to Clean Code

Chapters 4-6 expand the three paradigms. Chapter 11 depends on polymorphism for dependency inversion. Chapter 22's Dependency Rule is made practical through OO-style interfaces and controlled data crossing. *Clean Code* aligns with this chapter through small functions, clear control flow, and minimizing side effects.

---

## Chapter 4 - Structured Programming - Part II

### Central argument

Structured programming matters because it makes code decomposable into pieces that can be reasoned about and tested. Dijkstra's deeper contribution was not simply opposition to arbitrary jumps; it was the idea that software can be made more reliable when its control structures make correctness falsifiable.

### Principles covered

- **Sequence, selection, and iteration are sufficient.** These control structures can express programs without unrestricted jumps.
- **Functional decomposition.** Large problems can be broken into smaller functions, then smaller still, until each part is understandable.
- **Falsifiability over proof.** Most software is not formally proven correct; instead, tests try to expose defects. Structure makes those tests meaningful.
- **Testability is architectural.** The same principle that makes a function testable also applies to components and services.

### Visual models and diagrams

- The chapter is mostly historical and conceptual. The visual model is a recursive decomposition tree: a large behavior is split into smaller functions, and each function is constrained by simple control structures. At architecture scale, the same idea becomes decomposed modules and components.

### Key architectural concepts and terms

- **Structured programming:** A discipline that avoids unrestricted jumps and uses simple control constructs.
- **Functional decomposition:** Breaking behavior into nested functions or modules by responsibility.
- **Falsifiable unit:** A unit small and structured enough that tests can meaningfully challenge it.
- **Proof vs testing:** Formal proof attempts to demonstrate correctness; testing attempts to find counterexamples.

### Anti-patterns warned against

- **Unstructured control flow.** Arbitrary jumps make reasoning and testing difficult.
- **Large, non-decomposed procedures.** When logic cannot be split cleanly, tests become broad and brittle.
- **Assuming tests prove correctness.** Tests increase confidence by failing to find defects; they do not guarantee absence of defects.

### Actionable architectural guidance

- Keep functions small enough to test and reason about.
- Prefer clear sequencing, branching, and looping over clever control flow.
- Design modules so defects can be isolated quickly.
- Treat testability as a design constraint from the beginning.
- Apply decomposition at every scale: function, class, component, service.

### Connections to other chapters and to Clean Code

This chapter is the foundation for Chapter 28's test boundary and Chapter 15's maintainability goal. It also reinforces *Clean Code* practices: small functions, clear intent, minimal hidden state, and code that can be understood without tracing arbitrary jumps.

---

## Chapter 5 - Object-Oriented Programming - Part II

### Central argument

The architectural value of OO is not merely combining data and functions or modeling the real world. Its decisive architectural contribution is controlled polymorphism. Polymorphism lets high-level policies call lower-level details through abstractions while keeping source dependencies pointed toward the higher-level policy.

### Principles covered

- **Encapsulation is only partial in many OO languages.** OO can support hiding, but it does not automatically guarantee it.
- **Inheritance is useful but not the essence of OO.** Inheritance existed conceptually before modern OO and can be misused.
- **Polymorphism is the architectural lever.** Runtime dispatch lets control flow and source-code dependency point in opposite directions.
- **Dependency inversion through interfaces.** High-level code can define what it needs; low-level implementations conform to that contract.
- **Plugins depend on policies, not the reverse.** Details such as databases and UIs can be made replaceable by depending on business-rule abstractions.

### Visual models and diagrams

- **Source dependency vs control flow.** The key model shows that a call may travel from a high-level module to a low-level implementation at runtime, while source code points toward an interface owned by the high-level side.
- **Dependency inversion model.** An interface sits between policy and implementation. The policy uses the interface; the implementation depends on it.
- **Database/UI as plugins.** The business rules sit at the center, while external devices or mechanisms depend inward on them.

### Key architectural concepts and terms

- **Encapsulation:** Hiding implementation details behind a public contract.
- **Inheritance:** Reusing or specializing behavior by deriving one type from another.
- **Polymorphism:** Calling behavior through a common abstraction while the concrete implementation is chosen at runtime.
- **Source-code dependency:** A compile-time or import-time dependency between code units.
- **Flow of control:** The runtime direction of execution.
- **Plugin architecture:** A structure where replaceable details depend on stable policies.

### Anti-patterns warned against

- **Equating OO with real-world modeling.** That definition does not explain the architectural power of OO.
- **Letting business rules depend on devices.** When policies import UI, database, or framework details, change ripples inward.
- **Inheritance-first design.** Inheritance can create brittle hierarchies if used where polymorphic boundaries would be better.

### Actionable architectural guidance

- Use interfaces at boundaries where policy must not know details.
- Put abstractions on the side that needs protection from change.
- Separate runtime call direction from source-code dependency direction.
- Make UI, database, gateways, and external services plugins to the business rules.
- Use inheritance sparingly; prefer polymorphic contracts that express stable roles.

### Connections to other chapters and to Clean Code

Chapter 11 formalizes this as the Dependency Inversion Principle. Chapter 17 uses it to draw boundaries, and Chapter 22 relies on it for Clean Architecture. *Clean Code* supports this through expressive abstractions, small classes, and avoiding concrete dependency leakage.

---

## Chapter 6 - Functional Programming - Part II

### Central argument

Functional programming matters architecturally because mutation is dangerous. Mutable state creates race conditions, temporal coupling, and complex coordination. Architecture should isolate mutation, reduce shared writable state, and make state transitions explicit.

### Principles covered

- **Immutability reduces complexity.** If values do not change, many concurrency problems disappear.
- **Mutation should be segregated.** Systems often cannot be fully immutable, but mutable areas can be isolated from pure computation.
- **State changes should be explicit.** Event-sourced approaches model changes as a sequence of facts, reducing hidden in-place mutation.
- **Concurrency safety is architectural.** Race conditions and deadlocks are not just coding problems; they result from how state is shared.

### Visual models and diagrams

- **Mutable state and transactional memory.** The chapter models many threads competing to update shared state. Conceptually, this shows why coordination mechanisms are needed when mutable data is shared.
- **Event history model.** Rather than storing only the current state, the system can store the sequence of state-changing events and derive current state from them.

### Key architectural concepts and terms

- **Immutability:** Data that cannot be changed after creation.
- **Mutable component:** A part of the system where state changes are allowed.
- **Pure function:** Logic that depends only on inputs and produces outputs without side effects.
- **Race condition:** A defect caused by timing-dependent access to shared state.
- **Deadlock:** A state where concurrent actors wait on each other indefinitely.
- **Event sourcing:** Persisting changes as append-only events rather than overwriting current state directly.

### Anti-patterns warned against

- **Global mutable state.** Shared writable state creates hidden coupling across the system.
- **Uncontrolled concurrent mutation.** When multiple threads or processes can update the same data freely, defects become timing-dependent.
- **Mixing mutation into core logic.** Business rules become harder to test and reason about when they mutate external state directly.

### Actionable architectural guidance

- Prefer immutable data structures for request/response models and domain events.
- Keep mutation near boundaries or inside explicit state-management components.
- Separate pure decision logic from persistence and side effects.
- Use event logs or command histories when auditability and replay matter.
- Design concurrent systems around ownership, queues, transactions, or immutability rather than shared writable memory.

### Connections to other chapters and to Clean Code

This chapter connects to Chapter 20's request/response models and Chapter 23's Humble Object approach, both of which separate logic from side effects. It also aligns with *Clean Code* guidance to avoid hidden side effects and keep functions predictable.

---

# Part III - Design Principles

## Chapter 7 - SRP: The Single Responsibility Principle - Part III

### Central argument

The Single Responsibility Principle is about change ownership, not merely doing one tiny thing. A module should be responsible to one actor or closely aligned group of stakeholders. When one class serves unrelated actors, their changes collide.

### Principles covered

- **Single Responsibility Principle.** A module should have one reason to change, and that reason is tied to one actor or stakeholder group.
- **Actor-based cohesion.** Code belongs together when it changes for the same stakeholder-driven reason.
- **Separation by responsibility.** Distinct business concerns should not be forced into one class just because they operate on related data.
- **Facade as coordination.** A facade can offer a simple API while delegating to separate responsibility-specific classes.

### Visual models and diagrams

- **Employee class example.** The model shows one class serving multiple departments or actors. Shared data and shared methods create accidental coupling.
- **Shared algorithm collision.** A common internal routine used by two responsibilities can become a hidden dependency between stakeholder groups.
- **Separated classes.** Each actor-facing responsibility is placed into a separate class so changes do not collide.
- **Facade alternative.** A small front-facing class coordinates specialized classes without merging their reasons for change.

### Key architectural concepts and terms

- **Actor:** A person or group that wants the system to change for a particular business reason.
- **Responsibility:** A reason for change, not simply a task.
- **Accidental duplication:** Similar-looking code that actually belongs to different responsibilities and should not necessarily be shared.
- **Merge conflict:** A development conflict caused by unrelated changes hitting the same file or class.
- **Facade:** A wrapper that provides a simpler interface over several specialized components.

### Anti-patterns warned against

- **God class by stakeholder accumulation.** One class serves payroll, HR, reporting, policy, or other unrelated actors.
- **False DRY.** Removing duplication too aggressively can tie unrelated business rules together.
- **Shared helper trap.** A helper used by multiple actors becomes a hidden coordination point.
- **High-conflict files.** Frequent merge conflicts reveal mixed responsibilities.

### Actionable architectural guidance

- Identify the actor behind each change request.
- Split classes when different actors require changes for different reasons.
- Do not share code until the reason for change is truly shared.
- Use facades to preserve ergonomic APIs without collapsing responsibilities.
- Watch version-control conflicts as evidence of poor responsibility separation.

### Connections to other chapters and to Clean Code

SRP is the class-level foundation for Chapter 13's Common Closure Principle and Chapter 16's use-case separation. *Clean Code* connects through small classes, meaningful names, and avoiding classes with multiple unrelated duties.

---

## Chapter 8 - OCP: The Open-Closed Principle - Part III

### Central argument

Software should be designed so common changes extend behavior without forcing widespread modification of existing stable code. OCP is not about never editing code; it is about arranging dependencies so high-level policy is protected from lower-level details and foreseeable variations.

### Principles covered

- **Open-Closed Principle.** A software artifact should be easy to extend while minimizing changes to stable existing code.
- **Strategic closure.** Total closure against all changes is impossible. Architects choose which kinds of changes to protect against.
- **Directional control.** Dependencies should point toward stable policy and away from volatile details.
- **Information hiding.** A module should expose only what others need, hiding volatile internals.
- **Component partitioning by change.** Different actors and change reasons should be separated into different classes and components.

### Visual models and diagrams

- **Report generation thought experiment.** The chapter models a system that computes data and presents it in multiple formats. The goal is to allow new presentations without altering the core calculation.
- **Classes separated by role.** Controllers, interactors, presenters, and data mappers are separated so policy is not coupled to output format or storage details.
- **Unidirectional component dependencies.** The diagrams show dependencies flowing from lower-level presentation/data details toward higher-level rules.

### Key architectural concepts and terms

- **Extension point:** A designed seam where new behavior can be added.
- **Policy:** The rule or decision that should remain stable.
- **Detail:** A replaceable mechanism such as formatting, storage, or delivery.
- **Information hiding:** Restricting knowledge of implementation decisions to reduce coupling.
- **Directional control:** Arranging dependency arrows so changes flow safely.

### Anti-patterns warned against

- **Shotgun surgery.** A small feature requires edits across many modules.
- **Policy depends on presentation.** Core rules change whenever UI or report format changes.
- **Leaky internals.** Modules expose implementation details that invite external coupling.
- **Unstrategic abstraction.** Trying to anticipate every possible future variation creates unnecessary complexity.

### Actionable architectural guidance

- Identify which changes are likely and design extension points around them.
- Put stable business decisions behind abstractions.
- Keep formatters, databases, and delivery mechanisms outside core policies.
- Use dependency direction to protect high-level code.
- Hide data structures and helper details that are not part of a stable contract.

### Connections to other chapters and to Clean Code

OCP depends on SRP and DIP. It becomes concrete in Chapter 22's boundary-crossing structure and Chapter 33's case study. In *Clean Code*, OCP appears through small abstractions, avoiding switches spread across the system, and minimizing reasons to edit working code.

---

## Chapter 9 - LSP: The Liskov Substitution Principle - Part III

### Central argument

Subtypes must be safely usable anywhere their base type is expected. LSP is not only an inheritance rule; it is an architectural rule about promises. If a caller must know which subtype or implementation it has, the abstraction is broken.

### Principles covered

- **Liskov Substitution Principle.** Implementations of an abstraction must honor the behavioral expectations of that abstraction.
- **Contract compatibility.** Subtypes should not surprise clients by weakening guarantees or changing meaning.
- **Architecture-level substitutability.** Services, APIs, plugins, and implementations must conform to shared expectations, not just method signatures.
- **Semantic consistency over type compatibility.** A program can compile and still violate LSP if behavior is inconsistent.

### Visual models and diagrams

- **License hierarchy.** The model shows different license types substitutable through a common abstraction because they preserve expected behavior.
- **Square/rectangle problem.** The diagram illustrates how an inheritance relationship that seems mathematically correct can fail behaviorally in code.
- **API violation example.** The chapter uses service/API behavior to show that LSP extends beyond classes into architectural contracts.

### Key architectural concepts and terms

- **Subtype:** A specialized implementation used through a more general abstraction.
- **Behavioral contract:** The expectations callers rely on, including side effects and invariants.
- **Invariant:** A condition that must remain true for an object or abstraction.
- **Substitutability:** The ability to replace one implementation with another without caller-specific logic.

### Anti-patterns warned against

- **Inheritance based on taxonomy instead of behavior.** A real-world "is-a" relationship may not be a safe code relationship.
- **Type checks against implementations.** Caller logic that branches on concrete subtype reveals a broken abstraction.
- **API inconsistency.** Similar endpoints or services that handle edge cases differently force clients to know implementation details.

### Actionable architectural guidance

- Define abstractions by caller expectations, not by object taxonomy.
- Test every implementation against the same contract tests.
- Avoid base classes whose methods mean different things in different subtypes.
- Treat API behavior as part of the contract, not just schema shape.
- Remove implementation-specific conditionals from high-level code.

### Connections to other chapters and to Clean Code

LSP supports DIP: dependency inversion works only if implementations are truly substitutable. It also supports Chapter 29's embedded interface design and Chapter 27's service boundaries. *Clean Code* connects through meaningful abstractions and avoiding misleading inheritance.

---

## Chapter 10 - ISP: The Interface Segregation Principle - Part III

### Central argument

Clients should not be forced to depend on methods or capabilities they do not use. Oversized interfaces create unnecessary coupling: when an unused method changes, unrelated clients may still be affected.

### Principles covered

- **Interface Segregation Principle.** Split interfaces so each client depends only on the operations it actually needs.
- **Dependency minimization.** A dependency is a liability; unused dependency surface is unnecessary risk.
- **Language sensitivity.** Statically typed languages expose interface coupling at compile time, but dynamically typed systems can still suffer conceptually.
- **Architectural ISP.** At architecture scale, depending on a large module, library, service, or framework can pull in unnecessary transitive dependencies.

### Visual models and diagrams

- **Large operations interface.** Several clients depend on one broad interface, though each uses only part of it.
- **Segregated operation interfaces.** The broad interface is split into smaller contracts, so each client sees only what it needs.
- **Problematic architecture.** A high-level component depends on a lower-level package and indirectly becomes vulnerable to unrelated changes in that package's dependencies.

### Key architectural concepts and terms

- **Fat interface:** An interface with too many unrelated methods.
- **Client-specific interface:** A contract designed around one client's needs.
- **Transitive dependency:** A dependency inherited indirectly through another dependency.
- **Unused dependency:** Code you do not call but still depend on for compile, deploy, validation, or runtime reasons.

### Anti-patterns warned against

- **Kitchen-sink interfaces.** One interface tries to serve every caller.
- **Header/package dependency bloat.** Depending on a module for one operation drags in unrelated details.
- **Shared service APIs with broad contracts.** Clients become coupled to operations they never use.

### Actionable architectural guidance

- Design interfaces from the client's point of view.
- Split large interfaces by role, use case, or actor.
- Audit dependencies for unused imports, unused service methods, and broad SDKs.
- Avoid convenience packages that bundle unrelated capabilities.
- Use adapter layers to narrow external APIs before they reach core policy.

### Connections to other chapters and to Clean Code

ISP connects directly to CRP in Chapter 13: both say not to depend on unused things. It also supports Chapter 32's framework caution. *Clean Code* connects through small interfaces, focused classes, and avoiding functions/classes with unrelated responsibilities.

---

## Chapter 11 - DIP: The Dependency Inversion Principle - Part III

### Central argument

High-level policies should not depend on low-level details. Both should depend on abstractions chosen to protect the policy. DIP is the mechanism that allows architectures to keep business rules stable while details such as databases, frameworks, and devices remain replaceable.

### Principles covered

- **Dependency Inversion Principle.** Source-code dependencies should point toward stable abstractions, not volatile concretes.
- **Stable abstractions.** Interfaces that represent policy needs are safer dependency targets than concrete implementations.
- **Avoid volatile concrete dependencies.** Concrete classes change often, so depending on them spreads volatility.
- **Abstract Factory pattern.** Creation of concrete implementations can be isolated so high-level code does not instantiate details directly.
- **Boundary crossing.** DIP often creates an architectural seam where one side owns the abstraction and the other side implements it.

### Visual models and diagrams

- **Abstract factory diagram.** The application uses an interface and a factory interface; concrete details live on the other side of the boundary. The main/configuration area wires the concrete objects.
- **Boundary line between abstract and concrete.** The model shows abstractions on the policy side and implementations on the detail side.

### Key architectural concepts and terms

- **High-level policy:** Core business or application rule that should be insulated from mechanisms.
- **Low-level detail:** Concrete implementation such as database access, UI, transport, hardware, or framework code.
- **Stable abstraction:** A contract that changes less often than implementations.
- **Concrete component:** Code with implementation details and direct dependencies on tools or frameworks.
- **Factory:** A component responsible for creating objects without forcing callers to know concrete classes.

### Anti-patterns warned against

- **Business logic instantiates details directly.** Constructors for databases, HTTP clients, frameworks, or device drivers appear in core rules.
- **Depending on volatile concretes.** A low-level change forces high-level recompilation or redesign.
- **Abstractions owned by details.** If the database package defines the interface, policy still depends on database vocabulary.

### Actionable architectural guidance

- Define interfaces at the policy boundary, in the direction of the policy's needs.
- Move object construction to main/composition code or factories.
- Keep concrete classes in outer layers or plugins.
- Depend on abstractions only when they protect against real volatility.
- Make dependency direction visible in module imports and build dependencies.

### Connections to other chapters and to Clean Code

DIP is the engine behind Chapter 17's boundaries, Chapter 19's policy-level separation, and Chapter 22's Dependency Rule. *Clean Code* supports DIP by keeping constructors, factories, and dependencies explicit and by avoiding hidden global access.

---

# Part IV - Component Principles

## Chapter 12 - Components - Part IV

### Central argument

Components are deployable units of software. The chapter explains how historical advances in linking and relocatable binaries made componentization possible. In architecture, components matter because they give teams a practical unit for release, deployment, and dependency management.

### Principles covered

- **Component as deployable unit.** A component is not just a folder; it is something that can be independently built, released, or deployed depending on the language and platform.
- **Relocatability enables composition.** Software units can be compiled separately and assembled later.
- **Linking shapes architecture.** The ability to link separately developed code lets systems be structured into replaceable units.
- **Physical packaging matters.** Architecture must eventually map to build artifacts, libraries, packages, services, or source modules.

### Visual models and diagrams

- **Early memory layout.** The chapter shows how programs once occupied fixed memory regions, making reuse and separate compilation difficult.
- **Splitting into address segments.** The model shows code split into independently placed pieces, foreshadowing modern libraries and components.

### Key architectural concepts and terms

- **Component:** A deployable software unit such as a library, package, jar, gem, DLL, service, or build module.
- **Relocatable binary:** Compiled code that can be loaded or linked at different memory addresses.
- **Linker:** Tool that assembles separately compiled pieces into a runnable system.
- **Release unit:** A unit that can be versioned and delivered to users or other teams.

### Anti-patterns warned against

- **Component as arbitrary grouping.** A folder or package is not architecturally meaningful unless it has release and dependency meaning.
- **Ignoring build/deploy reality.** Architecture diagrams that cannot map to actual build artifacts become aspirational only.
- **Monolithic packaging by accident.** Everything is built and released together because no one created meaningful component seams.

### Actionable architectural guidance

- Decide what your real deployable and releasable units are.
- Align source organization with build and release boundaries.
- Give components clear ownership and dependency rules.
- Avoid creating components that cannot be built, tested, or reasoned about independently.
- Use tooling to enforce component dependencies where possible.

### Connections to other chapters and to Clean Code

This chapter prepares for Chapters 13 and 14, which define how components should cohere and depend. *Clean Code* focuses on code units; this chapter raises the same concern to release units.

---

## Chapter 13 - Component Cohesion - Part IV

### Central argument

Component cohesion is about deciding what belongs together. No single rule is enough: reuse, release, and change forces pull components in different directions. Good architects balance these tensions rather than blindly maximizing one.

### Principles covered

- **Reuse/Release Equivalence Principle (REP).** Code that is reused together should be released together. If users depend on a component, they need versioning, documentation, and release discipline.
- **Common Closure Principle (CCP).** Classes that change together for the same reason should live together. This localizes maintenance and redeployment.
- **Common Reuse Principle (CRP).** Do not force users to depend on code they do not use. Classes reused together belong together; unrelated classes should be separate.
- **Cohesion tension.** REP and CCP tend to grow components; CRP tends to shrink them. Component design is a trade-off.

### Visual models and diagrams

- **Cohesion tension triangle.** The chapter uses a triangular model with REP, CCP, and CRP pulling component boundaries in different directions. The conceptual lesson is that component granularity is context-dependent: early development may favor change locality, while library design may emphasize reuse boundaries.

### Key architectural concepts and terms

- **Cohesion:** The degree to which things inside a component belong together.
- **Release documentation:** Information users need to decide whether to upgrade.
- **Common closure:** Shared reasons and timing of change.
- **Common reuse:** Shared reuse by clients.
- **Component granularity:** The size and scope of a component.

### Anti-patterns warned against

- **Random component contents.** A component contains unrelated classes with no common release or change reason.
- **Utility dumping ground.** A shared component accumulates unrelated helpers, forcing unnecessary dependencies.
- **Over-bundling.** Users depend on a large component for one class and must revalidate on unrelated changes.
- **Premature library design.** Trying to optimize reuse before understanding change patterns can lead to poor components.

### Actionable architectural guidance

- Group classes by release reason, change reason, and reuse pattern.
- Avoid shared utility components unless everything inside is genuinely reused together.
- Watch which files change together in commits; use that evidence to refine components.
- Keep components small enough to avoid unused dependencies but large enough to release coherently.
- Revisit component boundaries as the system evolves.

### Connections to other chapters and to Clean Code

CCP is the component-level form of SRP. CRP generalizes ISP. REP connects design to release management. *Clean Code* connects through cohesion: classes and functions should contain things that belong together for the same reason.

---

## Chapter 14 - Component Coupling - Part IV

### Central argument

Component coupling is about controlling the dependency graph. A system with cycles, unstable dependency direction, or unstable abstractions becomes difficult to release and change. The chapter introduces principles and metrics for keeping component dependencies manageable.

### Principles covered

- **Acyclic Dependencies Principle (ADP).** The component dependency graph should not contain cycles. Cycles force components to change, build, and release together.
- **Breaking cycles.** Use dependency inversion or extract a new component containing shared abstractions to restore an acyclic graph.
- **Stable Dependencies Principle (SDP).** Dependencies should point toward more stable components. A volatile component should not be depended on by something that is hard to change.
- **Stability by incoming dependencies.** Stability is about resistance to change; many dependents make a component stable because changes affect many users.
- **Stable Abstractions Principle (SAP).** Highly stable components should also be abstract enough to be extendable. Concrete stable components become rigid.
- **Main Sequence.** A healthy component tends to balance stability and abstraction. The extremes create painful or useless zones.
- **Distance metric.** Components can be measured against the stability/abstraction balance to spot architectural drift.

### Visual models and diagrams

- **Typical component graph.** Components are nodes; arrows are dependencies.
- **Dependency cycle.** A loop illustrates why one component change can force a chain of rebuilds and releases.
- **Dependency inversion cycle break.** The model extracts an interface so formerly cyclic components depend on a new abstraction.
- **Stable vs unstable components.** A component with many incoming arrows and few outgoing arrows is stable; one with no incoming arrows and many outgoing arrows is unstable.
- **I/A graph and zones.** The stability/abstraction graph shows desirable balance and two danger areas: stable concrete rigidity and abstract unused irrelevance.
- **Trend plot over time.** The chapter suggests tracking whether a component drifts away from healthy balance.

### Key architectural concepts and terms

- **Directed acyclic graph (DAG):** A dependency graph with no cycles.
- **Fan-in:** Number of external dependencies coming into a component.
- **Fan-out:** Number of dependencies leaving a component.
- **Instability:** A metric expressing how dependent a component is relative to how depended-on it is.
- **Abstractness:** A measure of how much of a component is abstract contracts rather than concrete implementation.
- **Zone of Pain:** Stable but concrete code; hard to change and hard to extend.
- **Zone of Uselessness:** Abstract but unstable/unused code; flexible but irrelevant.

### Anti-patterns warned against

- **Cyclic component dependencies.** Components become inseparable for build and release.
- **Stable component depends on volatile detail.** A hard-to-change package is forced to change with an easy-to-change package.
- **Concrete stable core.** Many dependents rely on implementation details that cannot evolve safely.
- **Abstract dead zones.** Abstractions are created without users or policy value.
- **Top-down component graph design too early.** Component structure should evolve with real classes and change patterns.

### Actionable architectural guidance

- Generate and inspect component dependency graphs.
- Break cycles immediately; do not normalize them.
- Put abstractions in stable locations when multiple components need them.
- Make stable components abstract enough to allow extension.
- Keep volatile plugins dependent on stable policies, not the reverse.
- Track instability and abstraction metrics for critical components over time.

### Connections to other chapters and to Clean Code

ADP and SDP are large-scale dependency hygiene. DIP is the mechanism used to fix many violations. Chapter 22's Dependency Rule applies these ideas at architectural boundaries. *Clean Code* connects through dependency clarity, small modules, and avoiding hidden coupling.

---

# Part V - Architecture

## Chapter 15 - What Is Architecture? - Part V

### Central argument

Architecture is the shape of a system: its components, their arrangement, and their communication. Its purpose is not merely to make the system work; many badly architected systems work. Its deeper purpose is to make the system easy to develop, deploy, operate, and maintain while keeping important options open.

### Principles covered

- **Architects remain programmers.** An architect must stay close to code to understand the consequences of decisions.
- **Architecture supports the system life cycle.** Development, deployment, operation, and maintenance all matter.
- **Keep options open.** Delay irreversible decisions about details until there is enough information.
- **Independent replaceability of details.** UI, database, devices, frameworks, and transport mechanisms should not dominate core policy.
- **Policy before mechanism.** The core rules of the system deserve more protection than the tools used to deliver them.

### Visual models and diagrams

- This chapter is more argumentative than diagrammatic. Its conceptual model is a system life cycle with four forces: development, deployment, operation, and maintenance. Architecture should reduce friction in all four.

### Key architectural concepts and terms

- **Software architect:** A senior programmer who guides structure while continuing to understand code-level reality.
- **Development:** How easily teams can build and extend the system.
- **Deployment:** How easily the system can be packaged and released.
- **Operation:** Runtime concerns such as performance, scaling, and monitoring.
- **Maintenance:** The cost of understanding and changing the system over time.
- **Option value:** The benefit of delaying detail decisions until necessary.

### Anti-patterns warned against

- **Architect detached from code.** Decisions become theoretical and impose pain on developers.
- **Premature detail commitment.** Choosing databases, frameworks, transport, or devices too early limits design freedom.
- **Operation-only architecture.** Focusing only on runtime behavior while ignoring development and maintenance cost.
- **Team topology mismatch.** Architecture that ignores how teams actually work increases coordination cost.

### Actionable architectural guidance

- Keep architects involved in implementation.
- Evaluate architecture by development, deployment, operation, and maintenance impact.
- Delay framework/database/UI decisions until the business rules are clear.
- Choose boundaries that match likely team and release boundaries.
- Prefer structures that allow components to be replaced or deferred.

### Connections to other chapters and to Clean Code

This chapter expands Chapters 1-2 into a full lifecycle model. Chapter 16 elaborates independence. Chapter 30-32 explain why databases, web, and frameworks are details. *Clean Code* connects because maintainability begins with readable, disciplined implementation.

---

## Chapter 16 - Independence - Part V

### Central argument

A good architecture separates concerns so use cases, layers, teams, and deployments can vary independently. Independence is not only a code organization ideal; it affects team velocity, deployment flexibility, operational scalability, and maintainability.

### Principles covered

- **Use-case independence.** Use cases should be separable so changes in one do not force changes in another.
- **Layer independence.** UI, application rules, business entities, databases, and external services should be separable by level of policy.
- **Independent developability.** Teams should be able to work with minimal interference.
- **Independent deployability.** Components should be deployable separately when the cost/benefit justifies it.
- **Decoupling mode choice.** Decoupling can happen at source, deployment, process, service, or other levels. Stronger decoupling has higher cost.
- **Duplication may be acceptable.** Duplication that belongs to different change reasons may be safer than premature unification.

### Visual models and diagrams

- The chapter's main visual model is conceptual: layers and use cases form two axes of separation. Another model is decoupling modes, where separation can range from source-level separation inside a monolith to independently deployed services.

### Key architectural concepts and terms

- **Use case:** Application-specific goal or workflow.
- **Layer:** A horizontal separation by level of policy or technical role.
- **Decoupling mode:** The physical/runtime mechanism used to separate components.
- **Independent developability:** Ability for teams to change code without stepping on each other.
- **Independent deployability:** Ability to release a component without releasing everything.

### Anti-patterns warned against

- **Premature service extraction.** Strong runtime separation before real need adds communication and deployment cost.
- **Shared code by coincidence.** Unifying similar code from different use cases can create false coupling.
- **One-size-fits-all decoupling.** Treating services, packages, and layers as interchangeable without considering cost.
- **Ignoring team structure.** Architecture that requires constant cross-team coordination reduces throughput.

### Actionable architectural guidance

- Separate use cases that change for different reasons.
- Separate layers by policy level and technical volatility.
- Choose the weakest decoupling mode that satisfies current needs while preserving future options.
- Permit duplication when concepts are similar but change independently.
- Reassess deployment boundaries as traffic, team size, and release cadence change.

### Connections to other chapters and to Clean Code

Independence depends on SRP, CCP, DIP, and the Dependency Rule. Chapter 18 explains physical boundary anatomy; Chapter 27 cautions against assuming services automatically provide independence. *Clean Code* connects through avoiding forced sharing and keeping responsibilities focused.

---

## Chapter 17 - Boundaries: Drawing Lines - Part V

### Central argument

Architectural boundaries separate things that change for different reasons and at different rates. The best boundaries protect business rules from details such as databases, UIs, frameworks, and external systems. Draw lines early enough to preserve options, but not so early that the system is burdened with speculative complexity.

### Principles covered

- **Boundary as change firewall.** A boundary prevents volatile details from forcing changes in stable policy.
- **Plugin architecture.** Low-level details plug into high-level policies by depending on abstractions defined by those policies.
- **Dependency direction matters.** The less important or more volatile side depends on the more important or more stable side.
- **Input/output are details.** UI and database are delivery/persistence mechanisms, not the purpose of the system.
- **Deferred decisions.** Boundaries let teams postpone database, UI, framework, and external integration choices.

### Visual models and diagrams

- **Business rules behind database interface.** The database is accessed through an abstraction owned by the business side.
- **Boundary line.** A line separates business rules from database details; dependencies cross toward the business rules.
- **Business/database components.** The model turns the line into components with directed dependencies.
- **GUI boundary.** UI plugs into business rules rather than business rules knowing the UI.
- **Plugin example.** External tools depend on the host application, showing the plugin relationship.

### Key architectural concepts and terms

- **Boundary:** A source, deployment, process, or service separation between different responsibilities or policy levels.
- **Plugin:** A replaceable low-level module that depends on a host policy.
- **Detail:** A mechanism that should be replaceable or deferrable.
- **Policy:** A rule that expresses the purpose of the system.
- **Boundary interface:** An abstraction used to cross a boundary without reversing dependency direction.

### Anti-patterns warned against

- **Database-centered architecture.** Business rules become shaped around persistence details.
- **UI-centered architecture.** Workflows and rules become inseparable from screens.
- **Framework-first design.** Framework conventions determine system structure before business rules are understood.
- **Late boundary drawing.** Once details are entangled, separation is expensive.
- **Overdrawn speculative boundaries.** Too many premature boundaries create ceremony without value.

### Actionable architectural guidance

- Identify volatile decisions and draw boundaries around them.
- Put interfaces on the high-level side of the boundary.
- Treat databases and UIs as plugins to business policy.
- Use boundaries to delay decisions, not to avoid decisions forever.
- Revisit boundaries as concrete change patterns appear.

### Connections to other chapters and to Clean Code

This chapter operationalizes DIP, OCP, and SDP. Chapter 22 gives the canonical clean architecture form. Chapter 30-32 explain why database, web, and frameworks belong outside. *Clean Code* connects through hiding details and keeping dependencies explicit.

---

## Chapter 18 - Boundary Anatomy - Part V

### Central argument

Boundaries can exist in different physical forms: source-level separation in a monolith, deployable components, threads, local processes, or services. The more physically separated the boundary, the higher the communication and operational cost. Architecture must choose boundaries intentionally.

### Principles covered

- **Boundary crossing.** Data and control cross boundaries through carefully designed interfaces.
- **Source-level boundaries can be real.** A monolith can still have strong architectural boundaries if dependencies are controlled.
- **Deployment boundaries add release independence.** Libraries and packages can be deployed independently while still running in one process.
- **Process/service boundaries add communication cost.** Crossing address spaces or networks changes latency, failure modes, and protocol design.
- **Boundary strength should match need.** Do not use remote services when source-level separation would solve the problem.

### Visual models and diagrams

- **Flow of control crossing boundary.** Runtime calls may cross from one side to another.
- **Dependency against control flow.** Interfaces allow the runtime call direction and source dependency direction to differ.
- **Monolith/deployment/process/service forms.** The chapter conceptually ranks boundaries from cheapest to most expensive.

### Key architectural concepts and terms

- **Boundary crossing:** A call or data transfer across an architectural line.
- **Monolith:** A system deployed as one unit, which may still contain internal boundaries.
- **Deployment component:** A separately deliverable binary or package inside a larger system.
- **Thread:** An execution path inside a process; not necessarily an architectural boundary.
- **Local process:** Separate address space on the same machine.
- **Service:** Independently communicating process, often over a network.

### Anti-patterns warned against

- **Assuming services equal architecture.** Physical separation does not guarantee clean dependencies.
- **Chatty remote boundaries.** Fine-grained calls across slow boundaries create performance and reliability problems.
- **No source-level discipline in monoliths.** A monolith without dependency rules becomes a tangled ball.
- **Boundary overkill.** Using heavy process/service separation when simple modules would suffice.

### Actionable architectural guidance

- Start with source-level boundaries unless deployment or runtime needs justify more.
- Design data transfer objects for boundary crossing.
- Keep remote calls coarse-grained and failure-aware.
- Treat service boundaries as costly and explicit.
- Enforce monolith boundaries with module rules, package visibility, or build constraints.

### Connections to other chapters and to Clean Code

Chapter 16 introduces decoupling modes; this chapter explains their anatomy. Chapter 27 expands the service warning. *Clean Code* connects through reducing coupling even when all code lives in one deployment unit.

---

## Chapter 19 - Policy and Level - Part V

### Central argument

Architecture is largely about separating policies by level. Higher-level policies are more abstract, more central to the business, and less dependent on details. Lower-level policies handle mechanisms. Dependencies should point toward higher-level policies so details plug into the core.

### Principles covered

- **Policy-level ordering.** Higher-level policies should not depend on lower-level mechanisms.
- **Distance from I/O indicates level.** Code closer to input/output devices is lower level; code expressing business or application decisions is higher level.
- **Lower-level plugins.** IO, devices, databases, and delivery mechanisms should depend on policy abstractions.
- **DIP plus stability.** Interfaces and component stability help dependencies point toward higher-level code.

### Visual models and diagrams

- **Simple encryption program.** A low-level program reads characters, transforms them, and writes them. The initial structure mixes policy with device handling.
- **Improved architecture.** Encryption policy is separated from IO devices through interfaces.
- **Lower-level components plug in.** IO device components depend on encryption policy, not the reverse.

### Key architectural concepts and terms

- **Policy:** A rule or decision that guides behavior.
- **Level:** The distance of a policy from raw input/output mechanisms; higher-level policies are more abstract and central.
- **Mechanism:** Technical detail used to execute a policy.
- **Central transform:** Core processing independent of device details.

### Anti-patterns warned against

- **Policy mixed with IO.** Core decisions are tangled with file, device, network, or UI handling.
- **Low-level details own abstractions.** The interface vocabulary is shaped around the mechanism rather than the policy.
- **Dependency from high level to low level.** Business rules import device or transport code.

### Actionable architectural guidance

- Rank code by policy level before drawing dependencies.
- Separate core transformations from input/output handling.
- Put interfaces near the higher-level policy.
- Make device, IO, and transport implementations plugins.
- Check imports: higher-level modules should not import lower-level details.

### Connections to other chapters and to Clean Code

This chapter synthesizes SRP, OCP, DIP, SDP, and SAP. Chapter 22's circles are a policy-level model. *Clean Code* connects through separating side effects from core logic and using meaningful abstractions.

---

## Chapter 20 - Business Rules - Part V

### Central argument

Business rules deserve the center of the architecture. The chapter distinguishes enterprise-wide rules from application-specific use cases. Entities capture the most general business rules; use cases orchestrate those rules for a specific application workflow.

### Principles covered

- **Entities contain critical business rules.** They should be independent of UI, database, and application delivery mechanisms.
- **Use cases contain application-specific business rules.** They orchestrate entities to satisfy a particular user goal.
- **Request/response models isolate the use case.** Data crossing into and out of use cases should not be framework or database objects.
- **Business rules are not database schemas.** Persistence structures may support rules but should not define them.

### Visual models and diagrams

- **Loan entity class.** The model shows business data and behavior that should remain valid across applications.
- **Use case example.** The chapter shows a workflow description with inputs, steps, and outcomes. Conceptually, a use case is a policy script for an application goal.

### Key architectural concepts and terms

- **Critical business rule:** A rule central to the business, independent of any one application.
- **Critical business data:** Data required by those central rules.
- **Entity:** Object or data/function cluster containing enterprise-wide rules.
- **Use case:** Application-specific rule set that coordinates entities to produce an outcome.
- **Request model:** Input data structure for a use case.
- **Response model:** Output data structure from a use case.

### Anti-patterns warned against

- **Anemic core controlled by frameworks.** Business rules live in controllers, ORMs, or UI code instead of entities/use cases.
- **Database model equals domain model.** Schema constraints or ORM entities become the business rule layer.
- **Use cases returning framework objects.** The core becomes coupled to web, database, or UI libraries.
- **Entity polluted by application workflow.** Enterprise rules are changed for one app-specific process.

### Actionable architectural guidance

- Identify enterprise rules separately from application workflows.
- Put critical rules in entities with no framework dependencies.
- Put workflow orchestration in use-case interactors/services.
- Use plain request and response models at use-case boundaries.
- Keep database records, HTTP requests, and UI models outside the core.

### Connections to other chapters and to Clean Code

This chapter defines the inner circles used in Chapter 22. It supports Screaming Architecture in Chapter 21: the codebase should reveal use cases and domain concepts. *Clean Code* connects through naming domain objects clearly and keeping behavior near the rules it protects.

---

## Chapter 21 - Screaming Architecture - Part V

### Central argument

A system's architecture should make its purpose obvious. Looking at the top-level structure should reveal the application's use cases and domain, not merely the frameworks, delivery mechanisms, or database technology it uses.

### Principles covered

- **Architecture should express intent.** The dominant structure should reflect what the system is for.
- **Frameworks are tools.** They should not define the architecture's identity.
- **Use cases are central.** A clean architecture makes application behavior visible and testable.
- **Testability without details.** The core system should be testable without web servers, databases, or UI frameworks.

### Visual models and diagrams

- This chapter is mainly conceptual. The mental model is architectural signage: a church looks like a church, a library like a library, and a software system should visibly express its domain rather than shouting "Rails," "Spring," or "database."

### Key architectural concepts and terms

- **Screaming architecture:** Architecture whose top-level structure communicates the system's purpose.
- **Framework-centric structure:** Organization where framework categories dominate package names and boundaries.
- **Use-case-centric structure:** Organization where business capabilities are visible and primary.
- **Testable architecture:** A system whose core behavior can be tested without external mechanisms.

### Anti-patterns warned against

- **Framework as identity.** The codebase structure primarily advertises the web framework or database layer.
- **Web-first thinking.** Treating the system as a web app instead of an application delivered through the web.
- **Hidden use cases.** Business workflows are buried inside controllers, views, or framework callbacks.
- **Untestable core.** Tests require a web server or database even for business rules.

### Actionable architectural guidance

- Name top-level modules after business capabilities and use cases.
- Keep frameworks in outer layers or plugins.
- Make use cases visible in package/module structure.
- Ensure business rules can run in tests without UI, database, or web server.
- Review architecture diagrams: they should reveal the domain before technology.

### Connections to other chapters and to Clean Code

This chapter connects directly to Chapter 20's entities/use cases and Chapter 34's package-by-component advice. *Clean Code* connects through intention-revealing names at every scale: variables, functions, classes, packages, and system architecture.

---

## Chapter 22 - The Clean Architecture - Part V

### Central argument

Clean Architecture integrates earlier boundary ideas into a layered model where dependencies point inward toward higher-level policy. The inner code contains entities and use cases; outer code contains adapters, frameworks, databases, and devices. The Dependency Rule governs every crossing.

### Principles covered

- **Dependency Rule.** Source-code dependencies must point inward toward higher-level policy. Outer details may know inner policies; inner policies must not know outer details.
- **Entities at the center.** Enterprise-wide rules are most protected.
- **Use cases outside entities.** Application-specific rules orchestrate entities without depending on delivery or persistence.
- **Interface adapters convert data.** Controllers, presenters, gateways, and data mappers translate between inner models and external formats.
- **Frameworks and drivers outside.** Web, database, UI, devices, and frameworks are details.
- **Boundary data should be simple.** Data crossing inward should not carry framework objects or database row structures.

### Visual models and diagrams

- **Concentric circles.** The central model has policy increasing inward and details increasing outward. The exact number of circles is not fixed; the direction of dependency is the invariant.
- **Typical web/database scenario.** Controllers receive input, use cases execute business workflow, presenters shape output, and gateways access persistence through interfaces. The important relationship is that source dependencies still point inward even when runtime control moves outward and inward.

### Key architectural concepts and terms

- **Entity layer:** Core enterprise business rules.
- **Use case layer:** Application-specific orchestration.
- **Interface adapter layer:** Translation between internal models and external representations.
- **Frameworks/drivers layer:** External mechanisms such as UI, database, web framework, devices.
- **Input port/output port:** Boundary abstractions for invoking use cases and returning results.
- **Gateway:** Interface through which use cases access external resources.
- **Presenter:** Component that converts use-case output into view-ready form.

### Anti-patterns warned against

- **Inner circle knows outer circle.** Business logic imports framework, database, or UI code.
- **Framework data crosses inward.** HTTP requests, ORM entities, or UI widgets enter the use-case layer.
- **Database schemas shape use cases.** Persistence concerns dictate application rules.
- **Rigid four-layer literalism.** Treating the diagram as a fixed package recipe rather than a dependency rule.

### Actionable architectural guidance

- Place business entities and use cases in modules with no framework imports.
- Define ports/gateways at the use-case boundary.
- Implement adapters outside the core.
- Pass simple data structures across boundaries.
- Ensure every dependency arrow points inward or is inverted through an interface.
- Test use cases without the web, database, or framework.

### Connections to other chapters and to Clean Code

This chapter is the synthesis of SRP, OCP, DIP, component stability, policy level, and boundaries. Chapter 33 applies it in a case study; Chapter 34 warns that code organization must enforce it. *Clean Code* connects through keeping code intention-revealing and free of hidden framework coupling.

---

## Chapter 23 - Presenters and Humble Objects - Part V

### Central argument

The Humble Object pattern separates hard-to-test behavior from easy-to-test logic. Presenters, views, database gateways, data mappers, and service listeners are all examples of boundaries where volatile or hard-to-test details are kept thin while meaningful behavior is moved into testable components.

### Principles covered

- **Humble Object pattern.** Put untestable or framework-bound code into a minimal object; move logic into a separate testable object.
- **Presenter/View separation.** Presenters format data; views display it with minimal decision-making.
- **Testing drives architecture.** Boundaries should make logic testable without external mechanisms.
- **Database gateways isolate persistence.** Use cases depend on gateway interfaces, not concrete databases.
- **Data mappers translate representations.** Mapping logic prevents database records from becoming business objects.
- **Service listeners are adapters.** External service entry points should translate and delegate rather than contain business rules.

### Visual models and diagrams

- The chapter's conceptual model is a split object: one side is thin and difficult to test because it touches UI/database/framework; the other side contains logic and can be unit tested. This pattern repeats across UI, persistence, and service boundaries.

### Key architectural concepts and terms

- **Humble object:** A minimal wrapper around hard-to-test external detail.
- **Presenter:** Converts application data into display-ready data.
- **View model:** Data structure shaped for the view, without business decisions.
- **View:** UI mechanism that displays the view model.
- **Gateway:** Interface for accessing external data or services.
- **Data mapper:** Component that converts between database shape and domain/application shape.
- **Service listener:** Adapter that receives external calls and invokes use cases.

### Anti-patterns warned against

- **Smart UI.** Business decisions live in views or UI callbacks.
- **Smart database layer.** Persistence code owns business rules.
- **Untestable adapters.** Framework-bound code contains complex logic.
- **Leaking external data structures.** Database rows or API payloads become core models.

### Actionable architectural guidance

- Keep views passive; move formatting decisions into presenters.
- Keep controllers/listeners thin; delegate to use cases.
- Put database access behind gateway interfaces.
- Use mappers to isolate schema and DTO shapes.
- Design tests around use cases and presenters, not full external stacks.

### Connections to other chapters and to Clean Code

This chapter applies Chapter 22's boundary rules. It also connects to Chapter 28's test boundary. *Clean Code* connects through separating side effects from logic and keeping classes small and focused.

---

## Chapter 24 - Partial Boundaries - Part V

### Central argument

Full architectural boundaries can be expensive. Sometimes a team should prepare for a boundary without paying the entire cost of independent deployment or complete separation. Partial boundaries preserve some options while avoiding premature overhead.

### Principles covered

- **Skip the last step.** Build the dependency inversion and interface structure, but defer physical separation if not yet needed.
- **One-dimensional boundary.** A boundary may control dependency direction without fully separating deployment.
- **Facade boundary.** A facade can simplify access to a subsystem, though it is weaker than a full boundary.
- **Boundary cost trade-off.** Every boundary has cost; use enough boundary to protect likely change.

### Visual models and diagrams

- **Strategy-like boundary.** An interface separates caller from implementation, allowing substitution.
- **Facade boundary.** A facade stands in front of a subsystem but may not fully invert dependencies or isolate all internals.

### Key architectural concepts and terms

- **Partial boundary:** A design seam that exists in code but not necessarily in deployment or process separation.
- **One-dimensional boundary:** A dependency direction rule without full runtime/deployment isolation.
- **Facade:** A simplifying front door to a subsystem.
- **Boundary maturation:** Strengthening a boundary later when the need becomes real.

### Anti-patterns warned against

- **Boundary overinvestment.** Building full services or deployable components before evidence justifies them.
- **No seam at all.** Ignoring a likely future split until the cost becomes high.
- **Facade illusion.** Believing a facade is a complete boundary when internals are still widely coupled.

### Actionable architectural guidance

- Add interfaces and dependency rules before physical separation when uncertainty exists.
- Use facades for simplicity, but know their limits.
- Defer independent deployment until there is a real release/team/runtime need.
- Keep partial boundaries easy to upgrade into full boundaries.
- Document which boundaries are partial and what would trigger promotion.

### Connections to other chapters and to Clean Code

This chapter refines Chapter 17: draw lines pragmatically. It also connects to Chapter 18's boundary anatomy and Chapter 16's decoupling modes. *Clean Code* connects through creating seams without unnecessary complexity.

---

## Chapter 25 - Layers and Boundaries - Part V

### Central argument

Real systems often require multiple boundaries, not just one clean set of concentric layers. The chapter uses a game example to show that UI, storage, networking, and policy may each need separate streams and boundaries. Architecture evolves as hidden dimensions of change become visible.

### Principles covered

- **Multiple axes of separation.** UI, persistence, networking, and policy can be independent change dimensions.
- **Dependency Rule still governs.** Even when diagrams become more complex, dependencies should point toward higher-level policies.
- **Streams should be split when they represent different concerns.** Data flow and control flow may need separate pathways for input, output, state, and network interactions.
- **Higher-level policy coordinates lower-level details.** The rules of the game/application should not depend on delivery or storage details.

### Visual models and diagrams

- **UI components reuse game rules.** Multiple UIs depend on the same core rules.
- **Storage behind an API.** Game rules use an abstraction to save/load state without knowing the storage mechanism.
- **Revised diagrams.** As networking and additional flows are added, the diagrams evolve to split streams and preserve dependency direction.
- **Microservice API addition.** A network API is added as another delivery mechanism, not as the owner of the rules.

### Key architectural concepts and terms

- **Layer:** A policy-level grouping.
- **Boundary:** A line separating independently changing concerns.
- **Data stream:** A path along which data moves through the system.
- **Crossing streams:** Mixing flows or concerns in ways that obscure dependency direction.
- **Policy coordinator:** Higher-level rule that manages lower-level details through abstractions.

### Anti-patterns warned against

- **Single-boundary oversimplification.** Treating every architecture as one set of layers hides real change axes.
- **UI/storage/network leakage.** Core rules know details of screens, persistence, or transport.
- **Confused data flow.** Input, output, network, and persistence concerns are tangled into one path.
- **Microservice as policy owner.** Network API shape starts to define core rules.

### Actionable architectural guidance

- Identify all volatile axes: UI, persistence, network, devices, external integrations.
- Draw separate boundaries for concerns that change independently.
- Keep core rules reusable across delivery mechanisms.
- Split data flows when one model becomes overloaded.
- Rework diagrams as understanding improves; do not force all systems into one picture.

### Connections to other chapters and to Clean Code

This chapter extends Clean Architecture from Chapter 22 into messier real-world cases. It connects to Chapter 27's service warning and Chapter 34's implementation mapping. *Clean Code* connects through avoiding mixed responsibilities and naming flows clearly.

---

## Chapter 26 - The Main Component - Part V

### Central argument

The main component is the lowest-level detail that wires the system together. It creates objects, chooses implementations, reads configuration, and hands control to the application. Because it knows all details, it should be kept small and separate from policy.

### Principles covered

- **Main is a detail.** Startup code is not the architecture's center; it is a plugin/configuration mechanism.
- **Composition root.** Object construction and dependency injection should be centralized near the outside of the system.
- **High-level policy should not know construction details.** Use cases should receive dependencies, not create them.
- **Configuration belongs at the edge.** Environment choices should not leak into business rules.

### Visual models and diagrams

- This chapter is mainly conceptual. The model is a dependency graph where main sits at the outermost edge and points inward to everything it configures, while the inner system remains unaware of main.

### Key architectural concepts and terms

- **Main component:** Startup module that creates and connects the system.
- **Composition root:** The place where concrete implementations are assembled and injected.
- **Dependency Injection framework:** Tool that may assist wiring, but should not dominate core architecture.
- **Ultimate detail:** A detail so external that the application policy should know nothing about it.

### Anti-patterns warned against

- **Scattered construction.** Concrete dependency creation is spread throughout use cases and entities.
- **DI framework leakage.** Core policy depends on injection annotations or container APIs.
- **Configuration in business rules.** Environment, framework, or deployment choices affect core logic.

### Actionable architectural guidance

- Centralize object graph construction in main/composition root.
- Keep main thin and replaceable.
- Inject dependencies into use cases; do not instantiate details inside them.
- Keep DI framework annotations out of the domain when possible.
- Treat startup wiring as outer-layer code.

### Connections to other chapters and to Clean Code

This chapter depends on DIP and Clean Architecture. Chapter 32 expands framework risk, including DI frameworks. *Clean Code* connects through explicit dependencies and avoiding hidden global state.

---

## Chapter 27 - Services: Great and Small - Part V

### Central argument

Services are not automatically architectural boundaries. A system can be composed of services and still be tightly coupled or poorly designed. Real architecture comes from dependency management, boundaries, and component structure inside and across services.

### Principles covered

- **Services do not guarantee decoupling.** Separate deployment and network calls do not automatically separate reasons for change.
- **Services do not guarantee independent development or deployment.** Shared data, protocols, and cross-cutting features can still couple them.
- **Cross-cutting concerns expose false boundaries.** A new feature may cut across many services, proving the service split was not aligned with policy changes.
- **Component-based services.** Each service should have internal clean boundaries and dependency direction.
- **Dependency Rule applies to services.** Service interfaces and implementations should still point toward higher-level policy.

### Visual models and diagrams

- **Taxi aggregator services.** Services are split by function, but a new feature cuts across many of them.
- **OO/component approach to cross-cutting concern.** Derivative classes or components allow the new feature to extend behavior without modifying every service in the same way.
- **Services with internal component design.** Services remain deployable units, but architecture is inside them and between them, not identical to the service map.

### Key architectural concepts and terms

- **Service:** Independently running process or network-accessible unit.
- **Microservice:** Small service, often independently deployable, but not inherently clean.
- **Cross-cutting concern:** Feature or rule that affects several functional areas.
- **Component-based service:** A service whose internal code follows component and boundary rules.
- **False decoupling:** Physical separation without independent changeability.

### Anti-patterns warned against

- **Service worship.** Believing that a distributed system is automatically well architected.
- **Functionally sliced services that ignore policies.** Every new policy requires edits across many services.
- **Distributed monolith.** Services are separately deployed but must change together.
- **Chatty service mesh.** Fine-grained network calls reproduce in-process coupling with worse latency and reliability.

### Actionable architectural guidance

- Do not equate service boundaries with architectural boundaries.
- Analyze change patterns before splitting services.
- Keep each service internally clean and testable.
- Use service boundaries for deployment/runtime reasons, not as a substitute for design.
- Design cross-cutting features through extension points and internal components.

### Connections to other chapters and to Clean Code

This chapter applies Chapter 18's boundary anatomy and Chapter 16's independence warnings. It also uses SOLID and the Dependency Rule inside service designs. *Clean Code* connects through avoiding duplicated conditional logic and maintaining focused components.

---

## Chapter 28 - The Test Boundary - Part V

### Central argument

Tests are part of the system and must be designed as such. A clean architecture protects tests from unnecessary fragility and gives tests a stable API. Test code should depend on the application in controlled ways, not on volatile UI or database details.

### Principles covered

- **Tests are system components.** They have dependencies and architecture, not just scripts.
- **Design for testability.** Use cases and policies should be invocable without external details.
- **Testing API.** Provide stable test-facing seams that let tests exercise business behavior without coupling to internals.
- **Avoid fragile tests.** Tests should not break because of irrelevant UI, schema, or implementation changes.
- **Dependency Rule applies to tests.** Tests should depend inward on stable policy APIs, not on outer details unless specifically testing them.

### Visual models and diagrams

- The chapter's conceptual model is a test component outside the system boundary, using a controlled API to exercise inner behavior. The important relationship is that tests can be independent of UI/database/framework volatility.

### Key architectural concepts and terms

- **Test boundary:** Architectural line between test code and production code.
- **Testing API:** Stable surface designed to support tests.
- **Fragile test:** A test that fails for reasons unrelated to the behavior it claims to verify.
- **Test double:** Replacement for an external detail used in tests.
- **System component:** A deployable or source component that participates in dependency rules.

### Anti-patterns warned against

- **UI-only testing.** Business tests depend on screens and workflows unnecessarily.
- **Tests coupled to internals.** Refactoring breaks many tests even though behavior is unchanged.
- **No test architecture.** Test suites become slow, brittle, and hard to understand.
- **Database-required business tests.** Core policy cannot be tested without infrastructure.

### Actionable architectural guidance

- Design use cases to be tested directly.
- Create stable test APIs for high-value workflows.
- Use fakes/adapters for databases, services, and devices.
- Keep test dependence on UI and infrastructure limited to integration tests.
- Refactor tests when they become more fragile than the code they protect.

### Connections to other chapters and to Clean Code

This chapter builds on structured programming's falsifiability and the Humble Object pattern. *Clean Code* connects through readable tests, focused assertions, and tests as documentation of behavior.

---

## Chapter 29 - Clean Embedded Architecture - Part V

### Central argument

Embedded systems need clean architecture as much as enterprise systems do. Hardware and real-time operating systems are details. Application logic should not be trapped behind target hardware, vendor headers, or OS APIs. A clean embedded architecture separates app policy from hardware and firmware details.

### Principles covered

- **App-titude test.** The application should be recognizable and testable apart from the hardware.
- **Hardware is a detail.** Hardware-specific code should be isolated behind interfaces.
- **HAL boundary.** A hardware abstraction layer prevents hardware details from leaking into application code.
- **Firmware boundary.** Firmware sits between pure software and hardware and should be managed carefully.
- **OS is a detail.** The application should not depend directly on a particular RTOS where avoidable.
- **Program to interfaces.** Hardware and OS implementations should be substitutable.
- **Conditional compilation should be contained.** Preprocessor/platform conditionals should not scatter through application logic.

### Visual models and diagrams

- **Three-layer model.** The chapter separates application, firmware/OS, and hardware concerns.
- **Hardware separation line.** Hardware-dependent code is placed behind a boundary.
- **Fuzzy software/firmware line.** Firmware has both software and hardware characteristics, making disciplined boundaries important.
- **HAL and OSAL diagrams.** Hardware and operating-system details are wrapped by abstraction layers that application code depends on.

### Key architectural concepts and terms

- **Embedded architecture:** Software architecture for systems tied to hardware devices.
- **Target-hardware bottleneck:** Development slowdown caused by requiring real hardware for most work.
- **Hardware Abstraction Layer (HAL):** Interface layer hiding hardware specifics.
- **Operating System Abstraction Layer (OSAL):** Interface layer hiding OS/RTOS specifics.
- **Firmware:** Low-level code closely tied to hardware behavior.
- **Conditional compilation:** Compile-time switches for platform-specific code.

### Anti-patterns warned against

- **Hardware-driven application.** Business/application behavior directly calls device registers or vendor APIs.
- **Target-only testing.** Developers cannot test meaningful behavior without hardware.
- **Leaky HAL.** Hardware details appear in application-facing interfaces.
- **RTOS lock-in.** Application logic imports operating-system APIs directly.
- **Scattered compile flags.** Platform conditionals contaminate policy code.

### Actionable architectural guidance

- Put application rules above hardware and OS abstractions.
- Design HAL interfaces in application terms, not register terms.
- Use simulators/fakes to test without target hardware.
- Isolate vendor libraries and RTOS calls in outer layers.
- Keep conditional compilation near the platform boundary.

### Connections to other chapters and to Clean Code

This chapter applies Chapter 30-32's "details" argument to hardware and OS. It also depends on LSP and DIP for substitutable hardware abstractions. *Clean Code* connects through isolating platform-specific code and keeping application logic readable.

---

# Part VI - Details

## Chapter 30 - The Database Is a Detail - Part VI

### Central argument

The database is not the architecture's center. A database is an implementation detail for storing and retrieving data. Business rules should not depend on the database model, SQL, ORM, or persistence framework. The system should be designed as if storage choices may change.

### Principles covered

- **Database independence.** Core policy should not know the database technology.
- **Data model is not database model.** Domain/application data structures should not be forced to mirror tables or documents.
- **Performance does not justify premature coupling.** Performance concerns are real, but they should be handled with careful boundaries and measured trade-offs.
- **Persistence is a plugin.** Database access belongs in outer layers behind gateway interfaces.

### Visual models and diagrams

- This chapter is mostly conceptual. The mental model is a business system whose rules can run with memory, files, SQL, NoSQL, or other storage because persistence is outside the core.

### Key architectural concepts and terms

- **Relational database:** A data storage technology based on relations/tables and query operations.
- **Database system:** A mechanism for persistence, indexing, querying, transactions, and durability.
- **Data model:** The structure used by business/application logic.
- **Schema:** The database's storage structure.
- **Persistence detail:** Storage mechanism hidden behind a gateway.

### Anti-patterns warned against

- **Database-centric design.** Tables and queries dictate use cases and entities.
- **ORM entity as business entity.** Persistence annotations and lazy loading leak into core policy.
- **SQL in business rules.** Core logic directly contains database queries.
- **Schema-driven architecture.** The system is designed from tables outward rather than use cases inward.

### Actionable architectural guidance

- Design use cases and entities before database schema details.
- Place SQL/ORM code in adapter/gateway layers.
- Convert between persistence models and domain/application models.
- Keep business tests independent of the real database.
- Optimize persistence behind boundaries using measurement, not assumption.

### Connections to other chapters and to Clean Code

This chapter is a direct application of Chapter 17 and Chapter 22. It also reinforces Chapter 21: the architecture should not scream the database. *Clean Code* connects through separating concerns and avoiding data structure leakage.

---

## Chapter 31 - The Web Is a Detail - Part VI

### Central argument

The web is a delivery mechanism, not the application itself. Web technologies have swung between server-heavy and client-heavy forms, and they will keep changing. The architecture should protect business rules from that volatility.

### Principles covered

- **Delivery mechanism independence.** The same application should be deliverable through web, CLI, desktop, mobile, service API, or other interfaces.
- **UI volatility.** Web frameworks and client/server styles change often.
- **Use cases outlive delivery trends.** Business workflows should not be rewritten because the web stack changes.
- **Boundary around web.** Controllers, routes, templates, and browser-specific code belong outside the core.

### Visual models and diagrams

- This chapter uses a pendulum concept: web architecture repeatedly shifts between work done on server and work done in browser/client. The visual idea is not a fixed diagram but a moving center of gravity, showing why the core should not depend on the current swing.

### Key architectural concepts and terms

- **Web:** A delivery mechanism involving HTTP, browsers, servers, clients, and related frameworks.
- **GUI delivery:** User interface mechanism separate from core rules.
- **Client/server pendulum:** The recurring movement of responsibility between server-side and client-side code.
- **Web boundary:** Adapter layer that converts HTTP/UI concerns into use-case calls.

### Anti-patterns warned against

- **Web app identity.** Treating the web framework as the application architecture.
- **Business logic in controllers.** Use cases live inside route handlers.
- **HTTP-shaped core.** Business rules accept request/response objects or web-specific models.
- **Framework churn damage.** A web stack migration forces core logic rewrites.

### Actionable architectural guidance

- Keep controllers thin and use-case focused.
- Convert HTTP requests into plain input models.
- Convert use-case output into web responses outside the core.
- Test use cases without web servers or browsers.
- Design the application so a CLI or alternate UI could reuse the same core.

### Connections to other chapters and to Clean Code

This chapter applies the Dependency Rule to delivery. It connects to Chapter 21's framework warning and Chapter 23's presenters/views. *Clean Code* connects through keeping controller functions small and free of business-rule clutter.

---

## Chapter 32 - Frameworks Are Details - Part VI

### Central argument

Frameworks are useful but dangerous. Their authors want users to couple deeply to them, but the relationship is asymmetric: your system may depend on the framework heavily, while the framework does not care about your architecture. Protect the core from framework coupling.

### Principles covered

- **Frameworks are tools, not architecture.** Use them, but do not let them own your system shape.
- **Asymmetric relationship.** The framework imposes constraints on your code; it has no reciprocal duty to protect your business rules.
- **Delay framework commitment.** Keep options open until a framework decision is necessary.
- **Keep frameworks outside the core.** Core policy should not inherit from framework base classes or use framework annotations when avoidable.
- **Use adapters/proxies.** Wrap framework APIs at boundaries.

### Visual models and diagrams

- This chapter's conceptual model is a marriage contract with unequal risk. The framework invites deep integration, but the application bears the long-term migration and coupling cost.

### Key architectural concepts and terms

- **Framework:** A reusable infrastructure that calls or shapes application code.
- **Inversion of control:** The framework owns parts of execution flow and calls user code.
- **Framework coupling:** Direct dependence on framework types, annotations, lifecycle, or conventions.
- **Proxy/adapter:** A wrapper that prevents framework details from entering the core.

### Anti-patterns warned against

- **Framework-first architecture.** Package structure, entities, and use cases are dictated by framework conventions.
- **Core inherits framework classes.** Business objects extend framework base types.
- **Annotation pollution.** Domain objects are filled with persistence, routing, injection, or serialization annotations.
- **Irreversible adoption.** The framework is chosen before architecture has protected the core.

### Actionable architectural guidance

- Treat framework APIs as outer-layer details.
- Wrap framework behavior in adapters.
- Keep domain and use-case code free of framework inheritance and annotations where practical.
- Defer framework choice until the architecture can absorb it safely.
- Evaluate frameworks by exit cost, not only entry speed.

### Connections to other chapters and to Clean Code

This chapter reinforces Chapters 15, 17, 21, and 22. It also connects to Chapter 26 because DI frameworks can leak into the core if misused. *Clean Code* connects through avoiding unnecessary dependencies and keeping domain objects simple.

---

## Chapter 33 - Case Study: Video Sales - Part VI

### Central argument

This chapter applies the book's principles to a sample video sales system. The architecture separates actors, use cases, components, and dependencies so policies remain protected and deployment options remain flexible.

### Principles covered

- **Use-case analysis by actor.** Different users or roles imply different reasons for change.
- **SRP at system scale.** Components are separated by actor-driven change reasons.
- **Dependency Rule in component design.** Controllers, presenters, interactors, and gateways depend toward policy.
- **OCP through inheritance/abstraction.** Implementations can vary while high-level policies remain stable.
- **Deployment flexibility.** Components can be grouped into deployables in multiple ways after source dependencies are controlled.

### Visual models and diagrams

- **Use-case analysis diagram.** The model maps actors to use cases and identifies shared or abstract use cases.
- **Preliminary component architecture.** Components such as views, presenters, controllers, interactors, and data layers are arranged with dependencies toward higher-level policy.
- **Control flow vs dependency direction.** Input flows from controllers to interactors, and output flows through presenters to views, while source dependencies still point toward policy.

### Key architectural concepts and terms

- **Actor:** Role or stakeholder group that drives use cases.
- **Abstract use case:** Shared use-case behavior used by concrete use cases.
- **Interactor:** Use-case implementation component.
- **Component architecture:** Arrangement of deployable/source units and their dependencies.
- **Open arrow/closed arrow distinction:** Conceptually, one relationship represents use and another represents inheritance/implementation, showing how dependency direction is controlled.

### Anti-patterns warned against

- **Actor-blind grouping.** Components are grouped by technical role only, ignoring who asks for changes.
- **Deployment decisions before dependency design.** Packaging choices are made before source dependencies are clean.
- **Control flow mistaken for dependency direction.** Runtime calls are allowed to dictate compile-time imports.
- **Single-dimensional separation.** Only layer separation is used, while actor/use-case separation is ignored.

### Actionable architectural guidance

- Start architecture from actors and use cases.
- Separate components by both change reason and policy level.
- Use abstractions so dependency direction points toward interactors/use cases.
- Decide deployment grouping after component dependencies are clean.
- Check every boundary crossing for correct data and dependency direction.

### Connections to other chapters and to Clean Code

This chapter combines SRP, OCP, DIP, Clean Architecture, and component principles. It prepares for Chapter 34's warning: diagrams are not enough unless implementation structure enforces them. *Clean Code* connects through keeping use-case code readable and technology-independent.

---

## Chapter 34 - The Missing Chapter - Part VI

### Central argument

Even good architectural intentions fail if the code organization does not enforce them. This chapter focuses on how to map architecture into packages, modules, visibility, source trees, and compiler-enforced boundaries.

### Principles covered

- **Implementation details can destroy architecture.** A good diagram is insufficient if packages allow illegal dependencies.
- **Package by layer.** Organizes code by technical role, such as web, service, repository. Simple, but often hides the domain and can permit weak boundaries.
- **Package by feature.** Organizes code vertically around features or domain concepts. Better at expressing purpose, but may still lack dependency enforcement.
- **Ports and adapters.** Splits inside/domain from outside/infrastructure so dependencies point inward.
- **Package by component.** Groups all code for a business component behind a narrow public interface and hides internals using language/module visibility.
- **Compiler enforcement.** Use language access modifiers and module systems to prevent architectural violations.
- **Organization vs encapsulation.** Folder structure alone does not guarantee encapsulation; visibility rules matter.
- **Pragmatic decoupling.** Choose source, module, or runtime separation based on team, skill, complexity, and budget.

### Visual models and diagrams

- **Package by layer UML model.** Web depends on service; service depends on repository. Dependencies point downward, but the business concept is not prominent.
- **Package by feature model.** Related feature types sit together, making the business concept visible.
- **Inside/outside model.** Domain code sits inside; infrastructure surrounds it and depends inward.
- **View orders use case examples.** The same use case is modeled under different packaging strategies.
- **Relaxed layered architecture.** Weaker layering allows bypasses that can damage boundaries.
- **Identical public exposure model.** Several structures can look architecturally different but expose the same public types, meaning the compiler cannot enforce the intended boundary.
- **Restricted access model.** Grayed-out/private/internal types show how encapsulation can force correct dependency use.
- **Domain/infrastructure source trees.** Splitting source trees can enforce inside/outside dependencies but has cost.

### Key architectural concepts and terms

- **Package by layer:** Horizontal technical packaging.
- **Package by feature:** Vertical packaging around a feature/domain concept.
- **Ports and adapters:** Architecture with domain inside and infrastructure outside.
- **Package by component:** Packaging around a business component with a narrow public interface.
- **Public vs published types:** Types may be technically public inside a module but not intended for external use; proper module systems can distinguish this.
- **Périphérique anti-pattern:** Infrastructure code bypasses the domain by calling other infrastructure directly around the outside.
- **Access modifiers:** Language features used to hide implementation details.

### Anti-patterns warned against

- **Package by layer as default forever.** The system becomes technical buckets rather than a business architecture.
- **Relaxed layering bypasses.** Controllers call repositories directly or infrastructure talks around the domain.
- **Public everything.** Any class can be used from anywhere, so architecture relies only on discipline.
- **Diagram-code mismatch.** The diagram shows boundaries that the codebase cannot enforce.
- **Infrastructure ring road.** Outer-layer components communicate with each other while bypassing domain policy.

### Actionable architectural guidance

- Choose package structure that reveals domain and enforces dependency direction.
- Hide implementation types aggressively.
- Use compiler/module visibility to enforce boundaries.
- Prefer package-by-component when it gives a clear public API and strong encapsulation.
- Split source trees only when the enforcement benefit exceeds complexity cost.
- Regularly compare diagrams against actual imports and access rules.

### Connections to other chapters and to Clean Code

This chapter grounds the entire book in implementation reality. It is especially connected to Chapters 21, 22, and 33. *Clean Code* connects through encapsulation, naming, package organization, and preventing accidental coupling.

---

# Appendix A - Architecture Archaeology - Part VII

This appendix is not a numbered chapter, but it reinforces the book's claim that architectural principles recur across different eras and technologies. Through historical projects, it shows the consequences of dependencies, boundaries, hardware constraints, database choices, layering, plugin structures, and deployment realities. The lesson is that architecture is not tied to modern frameworks; the same dependency and policy questions appear in old systems, embedded systems, enterprise systems, tools, and communications software.

---

# Master List of Principles

## SOLID principles

| Principle | Chapter / Part | Study definition | Architectural use |
|---|---:|---|---|
| **SRP - Single Responsibility Principle** | Chapter 7 / Part III | A module should answer to one actor or one coherent reason for change. | Separate classes, modules, use cases, and components by stakeholder-driven change reason. |
| **OCP - Open-Closed Principle** | Chapter 8 / Part III | Structure code so expected changes extend behavior without forcing widespread modification of stable code. | Use abstractions and dependency direction to protect policies from details. |
| **LSP - Liskov Substitution Principle** | Chapter 9 / Part III | Implementations must honor the behavioral expectations of their abstractions. | Make plugins, services, APIs, and subtypes safely replaceable. |
| **ISP - Interface Segregation Principle** | Chapter 10 / Part III | Clients should depend only on the operations they use. | Keep interfaces, packages, SDKs, and service contracts narrow. |
| **DIP - Dependency Inversion Principle** | Chapter 11 / Part III | High-level policy should not depend on low-level details; both meet through abstractions owned to protect policy. | Enables boundaries, plugins, clean architecture, and testable cores. |

## Component cohesion principles

| Principle | Chapter / Part | Study definition | Architectural use |
|---|---:|---|---|
| **REP - Reuse/Release Equivalence Principle** | Chapter 13 / Part IV | Things reused together should be released together under coherent versioning. | Design reusable packages/components with release discipline. |
| **CCP - Common Closure Principle** | Chapter 13 / Part IV | Things that change for the same reason and at the same time should be packaged together. | Minimize number of components touched by a change. |
| **CRP - Common Reuse Principle** | Chapter 13 / Part IV | Do not force clients to depend on component contents they do not use. | Avoid bloated packages and utility dumping grounds. |

## Component coupling principles

| Principle | Chapter / Part | Study definition | Architectural use |
|---|---:|---|---|
| **ADP - Acyclic Dependencies Principle** | Chapter 14 / Part IV | Component dependency graphs should not contain cycles. | Keep build, release, and change impact manageable. |
| **SDP - Stable Dependencies Principle** | Chapter 14 / Part IV | Depend in the direction of greater stability. | Keep volatile components from being trapped by stable dependents. |
| **SAP - Stable Abstractions Principle** | Chapter 14 / Part IV | Stable components should be abstract enough to be extended. | Avoid rigid, concrete, heavily depended-on components. |

## Architectural principles and rules

| Principle / Rule | Chapter / Part | Study definition | Architectural use |
|---|---:|---|---|
| **Architecture minimizes lifetime effort** | Ch. 1 / Part I | Good structure keeps build/change/maintain effort low. | Evaluate architecture economically. |
| **Architecture preserves softness** | Ch. 2 / Part I | Software must remain easy to change as requirements shift. | Protect structure against urgent feature pressure. |
| **Keep options open** | Ch. 15 / Part V | Delay irreversible detail decisions until necessary. | Defer database, UI, framework, and deployment commitments. |
| **Use-case independence** | Ch. 16 / Part V | Use cases should be separable by change reason and workflow. | Enables independent development and testing. |
| **Layer independence** | Ch. 16 / Part V | Separate policy levels and technical details. | Keeps UI/database/framework changes from affecting rules. |
| **Boundary drawing** | Ch. 17 / Part V | Draw lines between things that change for different reasons/rates. | Protects policy from volatile details. |
| **Plugin rule** | Ch. 17, Ch. 19 / Part V | Low-level details should plug into high-level policies. | Makes UI, database, devices, and frameworks replaceable. |
| **Policy-level direction** | Ch. 19 / Part V | Dependencies point toward higher-level policies. | Orders components by abstraction and importance. |
| **Business rules at the center** | Ch. 20 / Part V | Entities and use cases deserve central protection. | Prevents framework/database-driven systems. |
| **Screaming architecture** | Ch. 21 / Part V | The system structure should reveal its purpose. | Organize around domain/use cases, not frameworks. |
| **Dependency Rule** | Ch. 22 / Part V | Source dependencies point inward toward higher-level policy. | Governs clean architecture boundaries. |
| **Humble Object separation** | Ch. 23 / Part V | Keep hard-to-test detail wrappers thin; move logic into testable objects. | Improves UI, database, service, and framework testability. |
| **Partial boundary trade-off** | Ch. 24 / Part V | A seam can exist without full physical separation. | Preserves options without overengineering. |
| **Main is a detail** | Ch. 26 / Part V | Startup/composition code is outermost wiring. | Keeps object construction out of policy. |
| **Services are not architecture by themselves** | Ch. 27 / Part V | Network/process boundaries do not guarantee clean design. | Avoids distributed monoliths. |
| **Tests are system components** | Ch. 28 / Part V | Tests need stable boundaries and architecture. | Reduces fragile test suites. |
| **Hardware/OS/database/web/frameworks are details** | Ch. 29-32 / Parts V-VI | Mechanisms belong outside business policy. | Keeps core independent from volatile platforms/tools. |
| **Implementation must enforce architecture** | Ch. 34 / Part VI | Package/module/access rules must match the intended design. | Prevents diagram-code mismatch. |

---

# Master List of Architectural Patterns Discussed

## Clean Architecture

A layered, policy-centered architecture where the most important business rules sit at the center and volatile mechanisms sit outside. The key is not the exact number of layers but the inward dependency direction. Entities and use cases should not depend on UI, database, frameworks, or external services. Adapters translate between outer formats and inner models.

## Hexagonal Architecture / Ports and Adapters

A structure that treats the domain/application as the inside and external systems as the outside. Ports are interfaces expressing what the inside needs or offers; adapters implement those ports for web, database, messaging, files, or third-party services. Its goal is to allow delivery and infrastructure mechanisms to be replaced without rewriting the core.

## Plugin Architecture

A design where lower-level details depend on and plug into higher-level policy. The host policy defines abstractions; plugins implement them. This keeps business rules independent from UI, database, device, framework, or tool implementations.

## Layered Architecture

A structure that organizes code into horizontal layers such as UI, application/service, domain, and persistence. It can be useful, but the book warns that simple technical layering can hide the domain and can permit dependency direction problems unless strictly enforced.

## Relaxed Layered Architecture

A weaker version of layered architecture where upper layers may skip intermediate layers. It can reduce boilerplate in small systems but can also create bypasses, such as controllers talking directly to repositories, weakening policy boundaries.

## Package by Feature

A code organization style that groups code around features or domain concepts rather than technical layers. It makes business purpose more visible and often improves locality of change, but it may not by itself enforce clean dependency direction.

## Package by Component

A code organization style that groups a business component behind a narrow public API while hiding implementation classes. It uses package/module visibility to make the compiler enforce boundaries. It aims to combine domain visibility with strong encapsulation.

## Humble Object Pattern

A testing and boundary pattern that keeps hard-to-test objects thin. UI views, database adapters, framework listeners, and external service handlers should contain minimal logic and delegate meaningful decisions to testable objects.

## Presenter / View Model Pattern

The presenter converts use-case output into a format the view can display. The view model contains display-ready data. This keeps UI rendering separate from business and formatting decisions, improving testability.

## Gateway Pattern

A gateway is an interface that represents access to an external resource such as a database, file system, remote service, or hardware device. Use cases depend on the gateway abstraction; adapters implement it.

## Data Mapper Pattern

A mapper translates between persistence/external data structures and internal domain/application structures. It prevents schemas, ORM objects, or API payloads from leaking into core policy.

## Abstract Factory Pattern

A factory abstraction creates implementations without forcing high-level code to name concrete classes. It is used to manage dependency inversion when object creation would otherwise violate boundaries.

## Strategy Pattern

A behavior is selected through an interface rather than hardcoded conditionals. In the book, it also appears as a way to create partial boundaries: callers use an abstraction while implementations vary.

## Facade Pattern

A facade provides a simple front door to a subsystem. It can reduce dependency surface and simplify clients, though it is weaker than a full boundary if internals remain accessible or dependencies are not inverted.

## Event Sourcing

A persistence/state pattern where state changes are stored as a sequence of events rather than only as overwritten current state. It supports audit, replay, and isolation of mutation, but has complexity trade-offs.

## Component-Based Services

Services are designed internally as components with clean boundaries rather than as flat bags of endpoint logic. This prevents microservices or distributed processes from becoming a distributed monolith.

## Hardware Abstraction Layer (HAL)

An embedded architecture pattern that hides hardware details behind application-facing interfaces. It allows testing, simulation, and hardware substitution without rewriting application policy.

## Operating System Abstraction Layer (OSAL)

A pattern that hides RTOS or operating-system APIs behind a stable interface. It keeps application code from being locked to a specific OS mechanism.

## Composition Root / Main Component

A startup pattern where object graph construction, configuration, and dependency injection happen in one outermost location. It keeps construction details outside use cases and entities.

---

# Dependency Rule Deep-Dive

## What it is

The Dependency Rule says that source-code dependencies must point inward toward higher-level policy. Inner code represents the more abstract and important rules of the system. Outer code represents mechanisms: UI, databases, frameworks, devices, web servers, and external services.

The rule governs source dependencies: imports, references, compile-time dependencies, package dependencies, inheritance dependencies, annotations, and type usage. Runtime control can move in any direction, but source dependencies must point toward the core or be inverted through abstractions.

## Why it exists

The rule exists to protect the software's reason for existing from the tools used to deliver it. Business rules usually change for business reasons. Databases, frameworks, UI styles, protocols, and devices change for technical or market reasons. If business rules depend on those details, every external change can force inner policy changes. The result is high change cost, fragile tests, painful migrations, and architecture that cannot keep options open.

## The policy gradient

In a clean architecture, code becomes more abstract and policy-rich as you move inward:

1. **Frameworks and drivers**: web, database, UI, devices, external tools.
2. **Interface adapters**: controllers, presenters, gateways, data mappers.
3. **Use cases**: application-specific workflows.
4. **Entities**: enterprise or core business rules.

The exact layers can vary, but the gradient remains: details outside, policy inside.

## How it is applied

- Entities do not import use cases, adapters, frameworks, or databases.
- Use cases may use entities and define ports/gateways, but do not import concrete adapters.
- Controllers translate external input into use-case request models.
- Presenters translate use-case response models into view models.
- Gateways are interfaces used by use cases; database adapters implement them.
- Framework code is restricted to the outermost layer.
- Main/composition root wires concrete implementations to inner abstractions.
- Data crossing inward is simple and framework-free.

## What crosses boundaries

Data can cross boundaries, but the form matters. Inner layers should receive simple structures that do not depend on outer frameworks. For example, a use case can accept a plain input model, not an HTTP request object. It can return a response model, not a web response or UI widget. Database rows, ORM entities, framework contexts, and device handles should stay outside.

## How control flow can oppose dependency direction

A controller may call a use case, and the use case may need to send output to a presenter. At runtime, the use case can call an output port interface. The presenter implements that interface. Source dependency points inward or toward the abstraction, while runtime control reaches the outer implementation through polymorphism. This is the practical use of DIP.

## What violates it

- Entity imports an ORM annotation or database type.
- Use case directly opens SQL connections or calls a repository implementation class.
- Use case accepts HTTP request/response objects.
- Business rules inherit from framework base classes.
- Domain objects depend on UI widgets, serializers, or routing frameworks.
- Controllers bypass use cases and call database adapters directly for business behavior.
- Infrastructure classes call each other around the outside while bypassing domain policy.
- Tests can only exercise business rules through UI or real database infrastructure.
- Main/composition framework leaks into entities or use cases.

## Why it is not dogma about number of layers

The rule does not require exactly four layers, a specific folder structure, or a specific framework. It requires that dependencies point toward higher-level policy. A small monolith can follow it through packages and interfaces. A distributed service system can violate it. A single process can be clean; many services can be a mess.

## Practical enforcement methods

- Separate source modules for domain/use cases/adapters.
- Import-linter or architecture tests.
- Package-private/internal visibility.
- Narrow public APIs.
- Dependency inversion at boundaries.
- Build-system module dependencies that only point inward.
- Contract tests for adapters.
- Code review checks for framework/database imports in core modules.

---

# Master List of Anti-Patterns and Bad Practices

| Anti-pattern / bad practice | Chapter source | Consequence |
|---|---:|---|
| Shipping mess now and promising cleanup later | Ch. 1 | Productivity collapses as mess compounds. |
| Treating behavior as the only value | Ch. 2 | System becomes hard or impossible to change. |
| Ignoring architecture because it is not urgent | Ch. 2 | Important structural work is displaced by urgent features. |
| Unstructured control flow | Ch. 4 | Code becomes difficult to reason about and test. |
| Treating OO as only data + functions or real-world modeling | Ch. 5 | Misses dependency inversion and boundary power. |
| Business rules depend on UI/database | Ch. 5, 17, 22 | Details control policy and ripple changes inward. |
| Uncontrolled mutable state | Ch. 6 | Race conditions, deadlocks, temporal bugs. |
| God class serving multiple actors | Ch. 7 | Merge conflicts and accidental coupling. |
| False DRY across different responsibilities | Ch. 7, 16 | Unrelated changes become coupled. |
| Shotgun surgery | Ch. 8 | Small changes require edits everywhere. |
| Inheritance based on taxonomy not behavior | Ch. 9 | Substitutability breaks. |
| Type-checking implementations behind abstractions | Ch. 9 | Callers know too much; abstraction fails. |
| Fat interfaces | Ch. 10 | Clients depend on unused operations. |
| Transitive dependency bloat | Ch. 10 | Unused code still creates build/deploy risk. |
| High-level policy instantiates low-level details | Ch. 11 | Core depends on volatile implementation. |
| Random component grouping | Ch. 13 | Releases and reuse do not make sense. |
| Utility dumping ground | Ch. 13 | Everyone depends on unrelated code. |
| Component dependency cycles | Ch. 14 | Components cannot be released independently. |
| Stable concrete component | Ch. 14 | Hard-to-change and hard-to-extend core. |
| Abstract unused component | Ch. 14 | Overengineering with no value. |
| Architect detached from code | Ch. 15 | Architecture decisions become unrealistic. |
| Premature commitment to details | Ch. 15, 17, 30-32 | Options close before facts are known. |
| Premature service extraction | Ch. 16, 27 | Distributed complexity without independence. |
| Database-centered architecture | Ch. 17, 30 | Schema drives business rules. |
| Framework-first architecture | Ch. 21, 32 | Framework conventions dominate the system. |
| Smart UI | Ch. 23 | Business logic becomes hard to test and reuse. |
| Smart database layer | Ch. 23, 30 | Persistence owns policy. |
| Boundary overinvestment | Ch. 24 | Too much ceremony and deployment complexity. |
| Confused data streams | Ch. 25 | Boundaries and responsibilities become unclear. |
| Scattered construction and wiring | Ch. 26 | Dependency graph is hidden and hard to change. |
| Distributed monolith | Ch. 27 | Services must change and deploy together. |
| Fragile tests | Ch. 28 | Refactoring breaks tests unrelated to behavior. |
| Target-hardware bottleneck | Ch. 29 | Embedded development slows and testing suffers. |
| Leaky HAL/OSAL | Ch. 29 | Application code becomes hardware/OS dependent. |
| ORM/domain model fusion | Ch. 30 | Persistence details pollute business rules. |
| Web-shaped core | Ch. 31 | Delivery mechanism changes force core rewrites. |
| Deep framework marriage | Ch. 32 | Migration becomes expensive and risky. |
| Package by layer as permanent default | Ch. 34 | Domain intent is hidden and boundaries weaken. |
| Public everything | Ch. 34 | Compiler cannot enforce architecture. |
| Infrastructure ring road / Périphérique | Ch. 34 | Infrastructure bypasses domain policy. |
| Diagram-code mismatch | Ch. 34 | Architecture exists only in documentation. |

---

# Overarching Themes Across the Book

## 1. Architecture is about preserving changeability

The book repeatedly frames architecture as the discipline of keeping software soft. Behavior matters, but structure determines whether behavior can continue evolving.

## 2. Dependency direction is the central control mechanism

From DIP to component stability to Clean Architecture, the same theme appears: dependencies should point toward stable, high-level policy and away from volatile details.

## 3. Details must be delayed and isolated

Databases, web frameworks, UI, devices, operating systems, and frameworks are necessary, but they should not define the core. Good architecture makes them plugins.

## 4. Boundaries are tools for managing change

A boundary exists to separate different reasons and rates of change. Boundaries can be source-level, deployment-level, process-level, or service-level, and each has cost.

## 5. Testability is evidence of good architecture

When use cases and policies can be tested without external mechanisms, the architecture is likely separating concerns well. Fragile tests reveal poor boundaries.

## 6. Names and organization should reveal intent

Architecture should communicate the domain and use cases. A system should not be organized primarily around frameworks or technical buckets.

## 7. Implementation details decide whether architecture is real

A diagram is not enough. Package structure, module visibility, build dependencies, and compiler enforcement determine whether the intended boundaries survive daily development.

---

# Architect Checklist by Category

## Component design

- Do components have a clear release/reuse/change reason?
- Are REP, CCP, and CRP balanced rather than blindly optimized?
- Are components small enough to avoid unused dependencies?
- Are components large enough to release coherently?
- Are component owners and versioning rules clear?

## Layer separation

- Are entities independent of application, UI, database, and framework details?
- Are use cases independent of delivery and persistence mechanisms?
- Are adapters responsible only for translation and delegation?
- Do layers represent policy levels rather than arbitrary technical buckets?
- Does the architecture reveal domain/use-case intent?

## Dependency management

- Do source dependencies point toward higher-level policy?
- Are component dependency graphs acyclic?
- Do stable components avoid depending on volatile components?
- Are stable components abstract enough to extend?
- Are imports/build dependencies checked automatically?
- Are implementation details hidden with module/package visibility?

## Testability

- Can use cases be tested without web, database, UI, or hardware?
- Are hard-to-test details wrapped in humble objects?
- Is there a stable testing API for important workflows?
- Are tests coupled to behavior rather than implementation details?
- Are external services/devices replaceable with fakes or simulators?

## Boundaries

- What decisions are volatile enough to deserve boundaries?
- Are boundaries full or partial by intention?
- Is data crossing boundaries simple and framework-free?
- Do boundary interfaces live on the side that needs protection?
- Can a partial boundary be promoted later if needed?

## Use cases

- Are use cases explicit in code organization?
- Does each use case have clear input and output models?
- Are use cases separated by actor/change reason where appropriate?
- Do controllers/listeners delegate to use cases rather than contain them?
- Do use cases orchestrate entities without depending on details?

## Frameworks

- Is framework code restricted to outer layers?
- Are domain and use-case classes free of framework base classes and annotations where practical?
- Is the dependency injection container kept near main/composition root?
- Is there an exit strategy or adapter seam for major frameworks?
- Are framework conventions prevented from becoming the architecture?

## Databases

- Does the core avoid SQL, ORM, and schema dependencies?
- Are database models mapped to domain/application models?
- Are persistence gateways defined by use-case needs?
- Can business rules run without a real database?
- Are performance optimizations measured and kept behind boundaries?

## UI / Web

- Are controllers thin translators?
- Are presenters responsible for view-ready formatting?
- Are views humble and low-logic?
- Does the core avoid HTTP request/response types and UI widgets?
- Could another UI reuse the same use cases?

## Embedded / hardware

- Can application logic run without target hardware?
- Does the HAL expose application-meaningful operations rather than raw hardware details?
- Are OS/RTOS calls isolated behind an abstraction when appropriate?
- Are platform conditionals kept out of core policy?
- Are simulators/fakes available for hardware-dependent tests?

---

# Suggested Study Path

1. Read Chapters 1-2 to understand the business argument for architecture.
2. Study Chapters 3-6 as the code-level foundation.
3. Learn SOLID in Chapters 7-11, but focus on change reasons and dependency direction rather than memorizing slogans.
4. Study component principles in Chapters 12-14 with real package graphs from your own system.
5. Read Chapters 15-22 as the core architecture section.
6. Use Chapters 23-29 to evaluate UI, tests, services, and embedded boundaries.
7. Use Chapters 30-34 as a practical audit checklist: database, web, frameworks, case study, and actual code organization.

---

# Practical Architecture Audit Questions

- What are the core business rules, and where do they live?
- Which modules import frameworks, databases, UI, or device code?
- Can the main use cases run in a unit test without infrastructure?
- Where are the dependency cycles?
- Which package has too many unrelated reasons to change?
- Which interface or component forces users to depend on unused things?
- Which component is stable but too concrete?
- Which detail decision has been made too early?
- Does the code organization scream the business domain or the framework?
- Can the compiler enforce the intended architecture?