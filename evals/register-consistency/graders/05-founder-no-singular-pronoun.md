---
type: regex
pattern: '(^|\s)(እሱ|እርሱ)(\s|$)'
match: not_contains
target:
  source: file
  path: order-am.md
---
