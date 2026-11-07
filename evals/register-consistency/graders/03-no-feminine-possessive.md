---
type: regex
pattern: '(ትዕዛዝ|ትእዛዝ|አድራሻ|ስልክ|ኢሜይል|ደረሰኝ|ቀን)\S*ሽ[\s።፣]'
match: not_contains
target:
  source: file
  path: order-am.md
---
