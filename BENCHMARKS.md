# Benchmarks

How amharic-writer 0.1 was tested, what it scored and what the tests don't show.

## Summary

| What was measured | Result |
|---|---|
| Output checks, final version | **349 / 351** |
| Output checks, earlier comparison: without the skill / with it | 154 / 195 → **191 / 195** |
| Activation: right call on whether to use the skill | **86 / 86** |
| Tokens loaded for a short message | about 2,500 |

All runs used Claude Sonnet 5.5, three runs per task, in November 2026.

## How it was tested

Each test gives the model an ordinary request, such as "translate this notice for our community center's Telegram channel", and checks the file it writes. The checks are regular expressions: they look for a form that must appear (ከጠዋቱ 3 for 9:00 a.m.) or must not (`::` instead of ።, a space before ።). They are free to run and give the same answer every time.

No AI grader was used. In early testing, AI graders failed correct Amharic and made up most of a run's cost. The checks can't judge whether a sentence sounds natural; for that, the author reviewed every Amharic example in the skill and read test outputs side by side.

The tests are in [`evals/`](evals/) and [`trigger-evals/`](trigger-evals/); see [`evals/README.md`](evals/README.md) to run them.

## Output quality

Eleven tasks, three runs each, final version of the skill:

| Task | Passed |
|---|---|
| Casual note to a younger sister (feminine agreement) | 27 / 27 |
| Contact page and buttons | 21 / 21 |
| App strings in JSON, with placeholders | 57 / 57 |
| Proofreading a customer SMS | 33 / 33 |
| Proofreading without "fixing" valid spellings | 27 / 27 |
| Flyer quoting the Constitution | 15 / 15 |
| Keeping one register through a message | 27 / 27 |
| Object and preposition marking on unfamiliar verbs | 37 / 39 |
| Closure notice with Ethiopian date and clock | 30 / 30 |
| Parents' newsletter (relation markers) | 36 / 36 |
| Website notice (‑ው and spelling) | 39 / 39 |
| **Total** | **349 / 351** |

Both misses are on one sentence, "The doctor told the patients to drink more water". The check expects ታካሚዎቹን … እንዲጠጡ. Two runs wrote something else, and those outputs weren't saved, so it's not known whether they were wrong or a valid alternative the check is too strict to accept.

### Without the skill

An earlier round ran seven tasks with and without the skill, using the version just before the final small edits:

| | Passed |
|---|---|
| No skill | 154 / 195 |
| With the skill | 191 / 195 |

The final version is not directly comparable: several checks were added or tightened afterwards, and the comparison wasn't rerun.

## Examples

Each pair is the first saved run for that task, with and without the skill, from the earlier round.

### Quoting a law

The request asked for a flyer that quotes Article 25 of the Ethiopian Constitution.

Without the skill, the model wrote its own Amharic version of the article and put it in quotation marks as the text of the law:

```
የኢትዮጵያ ሕገ መንግሥት አንቀጽ 25 እንዲህ ይላል፦ "ሰዎች ሁሉ በሕግ ፊት እኩል ናቸው፤ ያለ ምንም ልዩነትም በሕግ እኩል ጥበቃ ይደረግላቸዋል።"
```

With the skill, it left a marked place for the published translation:

```
የኢትዮጵያ ሕገ መንግሥት አንቀጽ 25 እንዲህ ይላል፦

> [እዚህ ላይ የታተመ የአማርኛ ትርጉም ይገባል። Insert a published Amharic translation here.]
```

The same rule covers scripture and other texts that have an official wording.

### "Call the office" on a website

English "the office" doesn't mean Amharic needs ‑ው. On a public website the reader doesn't know which office, so the skill uses ወደ ቢሮ ይደውሉ.

Without the skill:

```
ለተጨማሪ መረጃ እባክዎ ቢሮውን ይደውሉ።
```

With the skill:

```
ለበለጠ መረጃ ወደ ቢሮ ይደውሉ።
```

### Marking the object

In "The doctor told the patients to drink more water", the patients need ‑ን. Without it, ታካሚዎቹ can read as a second subject.

Without the skill:

```
ዶክተሩ ታካሚዎቹ ብዙ ውሃ እንዲጠጡ ነገራቸው።
```

With the skill:

```
ሐኪሙ ታካሚዎቹን ተጨማሪ ውሃ እንዲጠጡ ነገራቸው።
```

## Activation

A skill also has to switch on when it's needed and stay off when it isn't. Thirty requests were tested, three runs each:

- **Should switch on (15):** for example a condolence message, form labels, a landlord letter, React strings, or a pasted Amharic text to fix.
- **Should stay off (15):** for example Tigrinya text, a question about Amharic grammar asked in English, an English travel blog about Ethiopia, and code that handles Ethiopian-calendar dates.

| | Right call |
|---|---|
| Should switch on | 42 / 42 |
| Should stay off | 44 / 44 |

Four runs didn't finish (stopped early or hit their turn limit) and aren't counted.

The previous description, without the "Not for Tigrinya…" sentence, was also run on the 15 stay-off requests. It scored 45 / 45 as well, so on these requests Sonnet stays off even without being told to. Harder near misses, such as an English request that contains a few Amharic words, haven't been tested.

## Size

The core skill is about 70 lines, about 2,500 tokens for a short message or proofreading task. Reference files load only when needed:

| Task | Tokens loaded (approximate) |
|---|---|
| Short message, translation or proofreading | 2,500 |
| App or website strings | 2,900 |
| Translation with dates | 3,250 |
| Everything | 6,000 |

These are estimates scaled from a measured core of 2,705 tokens.

## What these results don't show

- **Other models.** Only Sonnet was tested. Opus and other vendors' models may behave differently.
- **Naturalness.** The checks catch specific errors. They can't tell a fluent sentence from a stiff one that happens to contain the right forms.
- **Independent tests.** The author wrote the tests with Claude's help, and the skill was tuned on some of the same tasks. Eighteen of the 30 activation requests were held back from tuning the description, and all of their finished runs were right too.
- **Open questions.** A few rules are still being decided, such as how formally to refer to a teacher in a casual family note and which spelling variants to leave alone when proofreading.
