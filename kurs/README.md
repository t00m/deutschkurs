# Deutschkurs A1-A2

A German course for levels A1 and A2, built around the everyday life of a parent in Germany: family and parenting, school, football training and handball matches, friends, work, neighbours and the paediatrician. It is a [KB4IT](https://github.com/t00m/KB4IT) site that uses the [deutschkurs theme](https://github.com/t00m/kb4it-theme-deutschkurs) 0.7.0.

## Build

You need KB4IT 0.12.x and the deutschkurs theme 0.7.0:

```bash
pipx install "git+https://github.com/t00m/KB4IT@0.12.0"
kb4it install-theme deutschkurs-0.7.0.zip
kb4it build kurs/config/repo.json
```

Open `kurs/target/index.html` in a browser. `target/` and `var/` are build output and are not committed.

## Contents

| Type | Count | What |
|---|---|---|
| Situation | 10 | Zu Hause, Am Schultor, Kind krank melden, Elternabend, Fußballtraining, Handballspiel, Mit Freunden, Bei der Arbeit, Im Treppenhaus, Beim Kinderarzt |
| Conversation | 20 | Two or three model dialogues per situation, with variations |
| Text | 5 | Team chat, match schedule, birthday invitation, work e-mail, note in the stairwell |
| Word | 123 | Nouns, adjectives, adverbs, pronouns, prepositions, conjunctions, articles, numerals, interjections, particles |
| Verb | 57 | The core verbs of A1-A2, with present forms, Perfekt and separable prefixes |
| Chunk | 36 | Fixed phrases such as *Bescheid sagen*, *Gute Besserung!*, *Lust haben* |
| Grammar | 18 | From *der, die, das* and verb position 2 to Dativ, Perfekt, Nebensätze and reflexive verbs |
| Mistake | 9 | Typical mistakes of Spanish speakers, linked to their grammar entry by `Pattern` |
| Gap | 4 | Sentences to practise saying |
| Inbox | 1 | Captures of November 2026 to process |

Topics (`topics` in `repo.json`): Familie, Schule, Sport, Freunde, Arbeit, Nachbarn, Gesundheit, Alltag. Translations are in English (`native: en`).

## Trust

Every entry was written by an AI assistant: `Checked: assistant`, and every conversation is `Kind: model`. None of them happened. When a native speaker confirms an entry, set `Checked: native`; when you hear or see it in real life, set `Checked: attested`. Speakers are roles, and *Frau A.* or *Familie B.* are placeholders.
