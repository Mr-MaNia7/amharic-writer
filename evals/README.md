# Testing amharic-writer

`evals/` holds output tests and `trigger-evals/` holds activation tests, both for `claude plugin eval`. Every check is a free regex or tool check. Don't add LLM graders: they failed correct Amharic in testing and were 81% of a run's cost. Whether the Amharic sounds natural is judged by people reading the outputs, not by these checks.

Run from the repository root:

    claude plugin eval . --runs 3 --model claude-sonnet-5-5 --allow-tools Write Edit Bash --no-publish --threshold 0 --max-cost-usd 3
    claude plugin eval . --eval-dir trigger-evals --ablation none --model claude-sonnet-5-5 --no-publish --threshold 0 --max-cost-usd 2

Check names starting `form-` enforce wording the author approved. `pattern-` checks enforce a marker a confirmed rule implies, without fixing the wording. If a check fails on valid Amharic, the check is wrong: Fidel letters change when a suffix attaches, so `ውጤት` won't match ውጤቶቹን. Reviewed forms beat these checks.
