# Numbers, dates and time

Read this before writing any date, time or number in Amharic.

Readers in Ethiopia live with two calendars and two clocks. Treat any date or time you write as something that can be misread, and make it unambiguous.

- **Digits.** Arabic digits (2018, 15) are normal in modern text. Ge'ez numerals (፲፭, ፳፻፲፰) are for traditional or ceremonial writing, or when asked.
- **Ethiopian calendar.** Months: **መስከረም, ጥቅምት, ኅዳር, ታኅሣሥ, ጥር, የካቲት, መጋቢት, ሚያዝያ, ግንቦት, ሰኔ, ሐምሌ, ነሐሴ**, plus **ጳጉሜ** (not the older ጳጉሜን; 5 days, or 6 in a leap year). The year begins on 11 September (12 September before a Gregorian leap year) and runs 7 or 8 years behind the Gregorian.
  - Formal form: **ጥቅምት 28 ቀን 2018 ዓ.ም.**; short form **ጥቅምት 28/2018**. Days of the week: ሰኞ, ማክሰኞ, ረቡዕ, ሐሙስ, ዓርብ, ቅዳሜ, እሑድ.
- **Converting dates: compute, don't estimate.** Month boundaries don't line up, so mental arithmetic is often a day or a month off. Run a conversion if you can. In JavaScript, `new Intl.DateTimeFormat('am-ET-u-ca-ethiopic', { day: 'numeric', month: 'long', year: 'numeric', weekday: 'long', timeZone: 'UTC' }).format(new Date('2025-11-07'))` gives `ዓርብ፣ ጥቅምት 28 2018` (rearrange it to the formal form above). If you can't compute, keep the source's date, name its calendar (**እ.ኤ.አ.** for Gregorian), and say the Ethiopian date needs checking.
- **Which calendar to use.** For readers in Ethiopia, use the Ethiopian date, or give both: **ዓርብ ጥቅምት 28 ቀን 2018 ዓ.ም. (እ.ኤ.አ. ኖቬምበር 7 ቀን 2025)**. Don't silently relabel a Gregorian date with Ethiopian month names.
- **Ethiopian clock.** It counts from 6 a.m. and 6 p.m.: **ከጠዋቱ 3 ሰዓት** is 9:00 a.m.; **ከቀኑ 7 ሰዓት** is 1:00 p.m.; **ከምሽቱ 2 ሰዓት** is 8:00 p.m. A bare "9:00" in Amharic text is ambiguous. Say which clock you mean, or give both: **ከጠዋቱ 3:00 ሰዓት (9:00 a.m.)**. With a day, the day comes first and ከ stays on the time: **ሰኞ ከጠዋቱ 3:00 ሰዓት**, not ከሰኞ ጠዋቱ.
- Phone numbers, codes, prices and URLs stay exactly as given.
