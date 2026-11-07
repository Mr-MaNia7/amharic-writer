---
name: amharic-writer
description: 'Writes, translates, localizes and proofreads Amharic (አማርኛ) in Fidel so it reads as natural, suitably polite Amharic rather than translated English. Use when the output or the text being checked is Amharic: drafting messages, posts or notices, translating to or from Amharic, app or site strings, correcting Amharic text, or dates in the Ethiopian calendar, even if the user only says "in Amharic". Not for other Ethiopic-script languages such as Tigrinya, for questions about Amharic answered in English, or for English text that merely mentions Ethiopia.'
---

# Writing Amharic

Write from the meaning, not sentence by sentence, then reread for the points below.

Read a reference file when the task calls for it:
- A date, time or number: [references/dates-numbers.md](references/dates-numbers.md)
- App or site strings: [references/interface.md](references/interface.md)
- A verb whose marking is unclear, or many prepositions: [references/relations.md](references/relations.md)
- Sentence shape, unusual punctuation, abbreviations, loanwords or foreign names: [references/style.md](references/style.md)

## Register

Politeness in Amharic is grammar: it changes the pronoun, the verb ending and the possessive suffix. Settle the reader first, then check every pronoun, verb and suffix against that choice.

- **Public, customer-facing, interface text, or an unknown reader:** polite **እርስዎ**, imperatives like **ያንብቡ, ይግቡ**, possessive **‑ዎ** (ስምዎ, ትዕዛዝዎ). It has no gender, so it avoids guessing between አንተ and አንቺ.
- **Several readers together:** **እናንተ** and plural verbs (ኑ, ተመዝገቡ). A notice to members can use this or the polite singular; keep one.
- **Friends, family, casual chat:** familiar forms. With a woman, every verb, pronoun, possessive and adjective stays feminine, including for a woman you mention: **ሰርተሻል, ፈተናሽን, ደውይልኝ, አዲሷ መምህርትሽ**, not አዲሱ መምህርሽ.
- **A respected person you mention** (an elder, an official, a parent, a teacher, a religious figure, someone who has died): honorific **እሳቸው / እርሳቸው** with plural verbs (ሄዱ, ተናገሩ, ገለጹ), throughout the text.

Mixes to catch: **ትዕዛዝህ** beside **እባክዎ**; **እባክዎ … ይደውሉ** beside **ላደረጋችሁልን**.

## Relations

English and Amharic mark how a noun relates to its verb in different places, so copying English prepositions drops markers English never wrote and keeps ones Amharic doesn't use. For each verb, work out each noun's role: who acts, what is acted on, to or for whom, where, from where, with what, about what. Mark the role the way *that Amharic verb* expects; the English preposition only tells you a relation exists. On rereading, every noun phrase should have its role marked, or be the subject or an indefinite object.

Four patterns, with one example each:
1. **No English preposition, but Amharic needs a marker.** "the Qur'an commanded *the believers* to send blessings" → **ቁርኣን አማኞችን ሶለዋት እንዲያወርዱ አዘዘ**. Without ‑ን, አማኞች reads as a second subject. Verbs of commanding, telling, asking, teaching and helping take the person this way, then an **እንዲ‑** clause. An indefinite object stays bare: **መጽሐፍ አነበብኩ**, but **መጽሐፉን አነበብኩ**.
2. **An English preposition, but a plain object.** "wait *for* the bus" → **አውቶቡሱን ጠበቀ**, not ለአውቶቡሱ.
3. **A different marker from the literal match.** The verb decides: "thank you *for* your patience" → **ስለ ትዕግሥትዎ**.
4. **The preposition moves onto the verb.** With a pronoun, it usually becomes a suffix: "I wrote to him" → **ጻፍኩለት**.

**‑ው marks something the reader already knows; don't copy the English "the".** Ask whether this reader can tell which one is meant. On a website or billboard, "call the office" is **ወደ ቢሮ ይደውሉ**, not ወደ ቢሮው or ለቢሮው. To a school's parents, who know the school, "call the school office" is **ወደ ትምህርት ቤቱ ቢሮ**.

## Sentences

- Don't repeat a pronoun the verb already carries: **ያግኙን**, not "እኛን ያግኙን".
- English passives often become active: "your order has been received" → **ትዕዛዝዎ ደርሶናል** or **ትዕዛዝዎን ተቀብለናል**. **ትዕዛዝዎ ተቀብሏል** means the order received something.
- Translate meaning, not words: "take a decision" → **መወሰን**, not ውሳኔ መውሰድ.

## Spelling and punctuation

When you write new text, use **ስራ** (not ሥራ), **ዓመት** (not አመት) and **ህብረተሰብ** (not ኅብረተሰብ). This goes word by word, so don't respell other words by analogy.

End sentences with **።**, never `::` or `:`. Use **፣** for commas. Put no space before punctuation and one space after.

## Published texts

Scripture, laws, official statements and other published texts have an authoritative Amharic version, and readers will take your rendering as that text. Use the version the user supplies. Otherwise put this placeholder in place of the quotation, character for character, and say so in your reply:

**[እዚህ ላይ የታተመ የአማርኛ ትርጉም ይገባል። Insert a published Amharic translation here.]**

If the user explicitly wants your own working translation, label it as yours.

## Interface strings

Buttons take the polite imperative: **ያስቀምጡ, ይሰርዙ, ይቀጥሉ**. "Cancel" is **ይቅር**. A "Contact us" link or button that starts a message to a company or site is **መገኛችን**; ያግኙን stays only as a verb inside a sentence.

## Proofreading

Fix what is wrong, not what differs from how you would write it: spelling mistakes, agreement and voice errors, a relation marked the English way, mixed registers, calques, `::` or `:` used as a full stop, spaces before punctuation, and a missing final **።**.

**Your spelling preferences above are for new writing.** In someone else's text, leave a valid variant as written: ሥራ stays ሥራ, and ትዕግስት stays ትዕግስት. Keep the author's vocabulary, dialect and style.

Return the corrected text, then each change and why, so the author can accept or reject them one by one.

## Output

Give the Amharic first, ready to copy, then brief notes in the user's language: register, calendar and clock used, placeholders left. For anything published or relied on, list the word choices you are less sure of, with alternatives, and recommend a native speaker's review. Skip notes on a short informal message.
