+++
date = '2026-10-21T12:00:00+02:00'
draft = false
title = "Understanding the IT Industry — Software Houses, Product Companies, Brokers, and Holdings"
tags = ["it-industry", "software-engineering", "software-houses", "product-companies", "business-models", "it-consulting"]
categories = ["software-engineering", "business"]
summary = "A practical look at software houses, product companies, brokers, and holdings: how they make money, where responsibility sits, and what those differences mean for software engineers and clients."
comments = true
ShowToc = true
TocOpen = true
image = "banner.png"
weight = 40
+++

![banner](banner.png)

> Understanding an IT company starts with understanding what it sells, what it owns, and what it is responsible for delivering.

From the outside, many IT companies look similar.

They hire software engineers.

They advertise technical expertise.

They talk about innovation, partnerships, and digital transformation.

Yet behind similar language, they may operate very different businesses.

One company builds software for clients.

Another develops a product it sells to many customers.

A third connects engineers with organizations that need additional capacity.

A fourth owns companies operating across several of these models.

These differences influence how work is sold, how decisions are made, and what engineers are expected to achieve.

This post explores four common labels:

* software houses,
* product companies,
* brokers,
* holdings.

They are useful labels, provided we understand that they do not all describe the same dimension of a business.

## 🧭 Start with the Business Model

Before looking at job titles or technology stacks, I would ask four questions.

What does the company sell?

Who owns the software or product being developed?

Who decides what should be built?

Who is accountable when the work does not deliver the expected result?

The answers reveal more than a company's marketing description.

| Label | What it primarily describes | Typical commercial role |
| --- | --- | --- |
| Software house | A software development services business | Builds and maintains software for clients |
| Product company | A business built around its own product | Develops and sells access to, or licenses for, that product |
| Broker or intermediary | A role connecting demand with supply | Arranges access to specialists or suppliers |
| Holding company | An ownership structure | Holds interests in operating companies |

The last row matters.

**A holding is an ownership structure. The other labels mainly describe how an operating business serves its customers.**

A holding can own software houses, product companies, and intermediaries at the same time.

A single operating company can also combine several business models.

## 🛠️ Software Houses: Selling Software Development Services

Imagine a retailer that needs a new order-management system.

It understands its business, but it does not have enough engineering capacity to build the system internally.

It hires a software house.

The software house may provide:

* discovery and requirements work,
* software design,
* implementation and integration,
* testing,
* maintenance and support.

Its commercial offering is the ability to deliver software development work for a client.

The client typically controls the business context and priorities. The supplier contributes engineering expertise and, depending on the agreement, delivery management.

Ownership and usage rights depend on the contract. We should not assume that every component or piece of intellectual property automatically transfers to the client.

### The Contract Changes the Incentives

Two software houses can operate very differently.

One might provide engineers who join a client's existing team.

Another might take responsibility for delivering an agreed system.

| Arrangement | What the client buys | Important question |
| --- | --- | --- |
| Time and materials | Engineering work billed by time spent | How are priorities, progress, and spending controlled? |
| Dedicated team | Reserved team capacity | Who manages the backlog and accepts the work? |
| Fixed-price project | Defined deliverables for an agreed price | How are scope changes and acceptance handled? |
| Managed service | Ongoing service under agreed responsibilities | What service levels and remedies apply? |

These arrangements distribute uncertainty differently.

A fixed price does not remove uncertainty. It makes the definition of scope and the handling of changes especially important.

Time-based billing provides flexibility, but the parties still need a way to judge whether the work is producing useful results.

**The useful distinction is how much responsibility the supplier actually accepts.**

## 📦 Product Companies: Building an Asset They Sell Repeatedly

Now imagine a company developing its own order-management platform.

Instead of building a separate system for one retailer, it sells the platform to many retailers.

Its revenue may come from subscriptions, licenses, usage charges, support, or a combination of these.

The company invests in a product and tries to recover that investment across its customer base.

That changes the decision-making context.

A feature requested by one customer may help many others.

It may also introduce complexity that the rest of the customer base does not need.

Product teams must weigh those consequences.

### Ownership Extends Beyond Shipping a Feature

A product company needs to consider:

* which customer problems to address,
* how the product is priced,
* how customers adopt it,
* how reliably it operates,
* how it evolves over time.

Engineering decisions can affect support costs, customer retention, and the ability to introduce future features.

Suppose one large retailer requests a custom approval workflow.

The implementation might be straightforward.

The harder questions are about the product.

Should every customer receive the feature?

Should it be configurable?

Will it require permanent customer-specific behavior?

Who will maintain it three years from now?

A product company must reconcile individual requests with the direction of a shared product.

However, the label alone does not guarantee engineering autonomy. A product organization can still have centralized decisions, short planning horizons, or teams with limited influence.

## 🤝 Brokers: Connecting Demand with Capacity

Return to the retailer.

This time, it already has engineering managers, architects, and an established development process.

It needs three additional engineers for six months.

An intermediary finds suitable specialists and arranges their engagement.

In this context, I use **broker** as a descriptive term for an intermediary. Companies may describe themselves as staffing firms, recruitment agencies, consultancies, or technology partners, depending on the services they provide.

Those terms are not interchangeable.

A recruiter placing a permanent employee has a different commercial relationship from a supplier contracting specialists to a client.

### Where the Value Comes From

An intermediary may provide:

* access to available specialists,
* candidate screening,
* commercial coordination,
* contracting and invoicing,
* replacement arrangements.

For a contract engagement, the intermediary may charge the client a rate and pay the specialist or subcontractor a lower rate.

That difference is a gross spread. It is not automatically profit: operating costs, contractual obligations, and commercial risks still need to be covered.

A recruitment firm may instead charge a placement fee.

The important question is what service the intermediary provides in return.

### Follow the Delivery Responsibility

If engineers work under the retailer's direction, the retailer may remain responsible for architecture, priorities, and delivery.

The intermediary's responsibility may focus on supplying suitable people.

That is a different commitment from accepting responsibility for an entire software system.

Neither arrangement should be inferred from the word “partner.”

Read the actual scope.

Who manages the work?

Who accepts the result?

What happens when someone leaves?

Who resolves a delivery problem?

Those answers define the relationship.

## 🏢 Holdings: Owning the Businesses Behind the Work

Now imagine a group that owns three companies:

* a software development consultancy,
* a subscription software vendor,
* a specialist staffing business.

The parent holding company owns interests in these operating businesses.

It may allocate capital, appoint leadership, coordinate acquisitions, or provide shared functions.

The subsidiaries may retain different brands, management teams, customers, and commercial models.

This is why “holding” belongs on a different axis.

Knowing that a business belongs to a holding tells us something about ownership.

It tells us much less about the engineer's daily work.

That depends on the particular operating company, team, and client or product.

### The Group Name Is Only Part of the Picture

For an engineer, useful questions include:

Who is my contractual counterparty?

Which company manages my work?

Am I building a group-owned product or working for an external client?

Can assignments move between subsidiaries?

For a client, the questions are similar.

Which entity signs the agreement?

Which entity delivers the service?

Does the parent make any contractual commitment?

A recognizable group name does not, by itself, establish responsibility for a subsidiary's delivery.

## 🔗 Follow One Project Through the Different Models

Consider the same requirement:

> A retailer needs customers to track the progress of their orders.

Several commercial paths could support it.

| Model | Possible arrangement | Key responsibility to clarify |
| --- | --- | --- |
| Software house | Builds a tracking system for the retailer | Scope, acceptance, maintenance, and integration |
| Product company | Provides an existing tracking platform | Product capabilities, configuration, and service commitments |
| Broker | Supplies engineers to the retailer's team | Specialist suitability, continuity, and client supervision |
| Holding | Owns one or more of the suppliers involved | Which operating entity is accountable under the agreement |

The customer-facing feature may look similar.

The ownership, commercial relationship, and distribution of work can be very different.

This is also why comparing hourly rates alone can be misleading.

A specialist's time, a managed project, and a product subscription purchase different things.

## 🔄 Real Companies Often Combine the Models

The categories are useful, but their boundaries overlap.

A software house may develop its own product.

A product company may sell implementation services.

A consultancy may supply individual specialists alongside complete delivery teams.

A holding may own businesses that compete for different parts of the same customer's budget.

Even within one company, two teams may have very different working arrangements.

One team owns a product roadmap.

Another works entirely within a client's backlog.

A third maintains a service under contractual operating commitments.

**The company label is a starting point. The actual engagement explains the work.**

## 👨‍💻 What This Means for Software Engineers

For engineers, the business model helps explain the environment in which technical decisions happen.

| Environment | Questions worth asking |
| --- | --- |
| Software house | Will I own delivery, advise the client, or join a client-managed team? |
| Product company | How does engineering influence the roadmap, and who owns the product after release? |
| Intermediary engagement | Who directs my work, and what happens when the assignment ends? |
| Company within a holding | Which subsidiary and team will I join, and how much does the group influence them? |

I would also ask about a concrete recent decision.

How did the team choose between a customer request and technical maintenance?

Who decided the architecture?

What happened when a deadline became unrealistic?

Concrete examples make the working model easier to assess.

They also reveal whether the responsibility described during recruitment matches the authority engineers receive.

## 🔍 What This Means for Clients

For clients, the first step is to identify the gap they need to fill.

Do they need additional people?

A team capable of managing delivery?

An existing product?

An ongoing service?

These needs can overlap, but they require different agreements.

Hiring engineers does not automatically provide product management.

Buying a product does not automatically include every integration.

Commissioning a project does not automatically establish long-term support.

A useful agreement makes the boundaries visible:

* what is included,
* who makes decisions,
* who owns the deliverables and relevant rights,
* how success is accepted,
* how changes and ongoing support are handled.

Clarity here supports both the commercial relationship and the engineering work.

## 🏁 Final Thoughts

The IT industry contains several ways of organizing and selling software work.

Software houses sell development services.

Product companies invest in products they offer to customers.

Brokers connect organizations with specialists or suppliers.

Holdings organize ownership across businesses.

These labels help us understand a company, but they cannot describe every engagement or team.

For me, the most useful questions remain practical.

What does this company sell?

What does it own?

Which decisions does it control?

What is it responsible for delivering?

**Understanding those answers makes it easier to choose an employer, evaluate a supplier, and understand why an organization works the way it does.**

---

🚀 Follow me on [norbix.dev](https://norbix.dev) for more insights on Go, TypeScript, Python, AI, system design, and software engineering.

