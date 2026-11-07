---
type: regex
pattern: 'ትዕዛዝ\S*\s+(በተሳካ ሁኔታ\s+)?ተቀብሏል'
match: not_contains
target:
  source: file
  path: sms-fixed.txt
---
