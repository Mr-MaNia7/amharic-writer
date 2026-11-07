---
type: regex
pattern: '^(?=[\s\S]*(እባክዎ|ይደውሉ))(?=[\s\S]*ችሁ)'
match: not_contains
target:
  source: file
  path: newsletter-am.md
---
