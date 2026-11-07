---
type: regex
pattern: '(ትዕዛዝ|ትእዛዝ|አድራሻ|ስልክ|ኢሜይል|ደረሰኝ|ቀን)\S*ህ[\s።፣]'
match: not_contains
target:
  source: file
  path: order-am.md
---
