# schema-markup

Source: /Users/wzb/obsidian/marketingskills/skills/schema-markup/SKILL.md

## Skill trigger (prompt intent)
- Use when user wants schema markup, structured data, JSON-LD, rich snippets, FAQ schema, product schema, breadcrumb schema.

## Scope in one line
Implement valid, accurate JSON-LD schema to unlock rich results and improve search understanding.

## Prompt structure deep dive
1. Initial Assessment
   - Page type, existing schema, and target rich results.
2. Core Principles
   - Accuracy, JSON-LD format, Google guidelines, validation.
3. Common Schema Types
   - Organization, WebSite, Article, Product, SoftwareApplication, FAQ, HowTo, BreadcrumbList, LocalBusiness, Review, Event.
4. Multiple Schema Types
   - Use @graph to combine multiple entities.
5. Validation & Testing
   - Rich Results Test and schema.org validator; fix errors.
6. Implementation Patterns
   - Static HTML, React/Next.js SSR, CMS plugins.
7. Output Format
   - Provide JSON-LD block + placement instructions + testing checklist.
8. Questions & Related Skills
   - seo-audit, programmatic-seo, analytics-tracking.

## Best-fit use cases
- “Add FAQ schema to our pricing page.”
- “Implement Product schema for SaaS plans.”
- “Fix schema errors in Search Console.”

## How to use (step-by-step)
1. Identify page type and intent
   - Decide which schema type matches visible content.
2. Audit existing markup
   - Check for current schema and errors.
3. Choose the correct schema type
   - Select from common types; use required properties.
4. Draft JSON-LD
   - Include required and recommended fields, keep data accurate.
5. Place schema in page
   - <head> or end of <body>, SSR if using React/Next.
6. Validate before deploy
   - Rich Results Test, schema validator.
7. Monitor in Search Console
   - Fix warnings and errors quickly.

## Output expectations
- A full JSON-LD code block tailored to the page.
- Clear instructions on placement and validation steps.

## Pitfalls to avoid
- Marking up content that is not visible on the page.
- Using unsupported schema or missing required fields.
- Leaving stale schema after content changes.

## When to pair with other skills
- seo-audit: structured data as part of a full audit.
- programmatic-seo: templated schema at scale.
