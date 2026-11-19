<!-- origen: 3fb0b86e7ca01517 -->
# How Educational AI Daily is made

[Educational AI Daily](https://diarioiaeducativa.github.io/) gathers every morning what was discussed the
previous day in three open Telegram groups for teachers: ChatGPT-IA-edu (AI in education in general), Vibe
Coding Educativo (teachers who build their own applications with AI) and EduMedia-IAG (images, audio and video
with AI). It is written, reviewed, illustrated and translated by AI agents; a person supervises it and is
answerable for what is published.

This document brings together the paper's rules and how they are applied, so that readers can understand how it
is produced and help to improve it. How it is written is set out in the [style book](../encargos/estilo.md) and
how it is translated in the [translator's book](../encargos/traduccion.md). The reasons behind each decision are
in the [decision records](adr/README.md) (ADR), which are cited by number.

Each rule says **who applies it**, **how it is checked** and, where necessary, **what is still missing**. What
remains to be improved is gathered at the end.

## 1. The issue

**What is discussed on one day appears in the paper the next morning**, at 7am CET (UTC+1; Spanish mainland
time), in five languages: Spanish, Catalan, Galician, Basque and English (ADR 0026).

An issue contains:

- **The day's articles**: from none to six, and from none to five briefs, depending on what the day has
  produced, in five sections: Tools, Vibe coding, Multimedia, Debates and Institutions & Industry.
- **Library**: one article for each document added that day to the ChatGPT-IA-edu digital library (ADR 0006).
- **Repository**: up to two applications a day from the Vibe Coding Educativo resource repository; on Fridays,
  a summary of the week's (ADR 0008).
- **“A year ago”**: something that was being discussed on the same day a year earlier, compared with how things
  stand today (ADR 0040).
- **The comic strip** by Chalk and Algorithm, about one of the day's news items (ADR 0023).
- **On Sundays**, in addition, a feature that explains a single topic in depth (ADR 0004 and 0028) and “The week
  in video”, a short video with the week's highlights (ADR 0016 and 0027). On Sunday night a commentary on the
  week's most important developments is also written (ADR 0038).

The rules for each issue:

| Rule | Who applies it | How it is checked |
| --- | --- | --- |
| **At least three articles.** If there are fewer, they are made up with articles kept for these occasions (the reserve, section 5). | A program, every night, before the translations (ADR 0068) | The program counts the articles. |
| **At least one article from each group.** If a group does not yield even one, a stored one from that group goes in. | The writing agent tries; the reviewing agent turns a brief from the missing group into an article; if one is still missing, the reserve (ADR 0076 and 0077) | The reviewer and the reserve program. |
| **Only what has been discussed in the groups.** No general news about AI. | The writing agent | The reviewer compares each article with the messages. |
| **Not news**: the groups' internal organisation, greetings and personal complaints. The documents in the digital library have their own section. | The writing agent | The reviewer. |
| **What has already been published is not repeated.** If there is something new about a topic already covered, it appears as a brief, with a link to the earlier article (ADR 0011). | The writer and the reviewer, with a search tool covering everything published (ADR 0061) | The reviewer searches for every name and headline in what has already been published. |
| **No one monopolises the issue**: as a rule, one article per person and two per product or company. | The writing agent | The reviewer. |
| **If a day does not yield a worthy issue, it is not padded out**: stored articles go out instead. | The writer and the reserve | — |

## 2. Who does what

The agents are Claude AI models from Anthropic: Sonnet writes and reviews every day, Opus chooses the best
feature, writes the long texts and repairs whatever fails, and Fable writes and chooses the comic strip. **The
agents that write the paper cannot run programs**: they only read and write texts and consult the internet. This
way, nothing in the messages from the groups, which other people write, can lead them to do anything else (ADR
0002). The messages are material to report on, never orders.

Only the repairer works with programs. It writes nothing for the paper: it acts when something fails, finds the
cause and fixes it in a copy. It cannot change the text of the articles or of the comic strip, nor publish, and a
program checks its fix before it is applied (ADR 0087).

**No agent reviews what it has written itself.** Every text goes through a reviewer who did not write it, who
opens each source and removes whatever cannot be confirmed (ADR 0001).

| Agent | What it does |
| --- | --- |
| Writer and reviewer | The day's articles and briefs. |
| Documentalist and reviewer | The articles for the Library and the Repository, and the stored EduMedia ones. |
| Illustrator and drawing reviewer | A drawing that explains each article; the reviewer looks at it on its page and sends back any that cannot be understood (ADR 0005). |
| Scriptwriter and humour judge | Five scripts for the comic strip; the judge picks one (ADR 0023 and 0024). |
| Chronicler and verifier | “A year ago”. |
| Features editor, reporter, verifier and features judge | The Sunday feature. |
| Commentator and reviewer | The week's commentary. |
| Video scriptwriter | “The week in video”. |
| Translators | One per language, for each text. |
| Repairer | When something fails, fixes it so that the issue comes out; it neither writes nor changes the texts. |
| Spokesperson | Each morning's alerts in the three groups and the text for Instagram. |

All of them write following the [style book](../encargos/estilo.md), and each task also has its own guide.

## 3. A day at the paper

A program checks every five minutes what needs doing and notes what it has already done, so that nothing is
repeated. Times are Spanish mainland times: CET (UTC+1) in winter and CEST (UTC+2) in summer.

| Time | What happens |
| --- | --- |
| 1.00am | The issue is prepared from what was discussed the previous day: the articles and their review, the drawings, the comic strip, the Library, the Repository, “A year ago”, the checks, the translations and the alerts. If it fails, a second attempt is made. |
| 5.00am | The issue can already be viewed before publication, so that the supervising person can review it (ADR 0025). A program checks that the page looks right on screens of different sizes. |
| 6.30am | If the issue is still not ready, the process is stopped and it goes out with whatever there is or with stored articles. |
| 6.50am | The website is published, and the images for sharing each article and the alerts for the groups are prepared. If anything fails, it is tried again every 10 minutes until 9.00am. |
| 7.00am | The Bot de IA Educativa posts the issue alert in each group and writes privately to the people whose resource appears that day (ADR 0052). The paper's Android app announces the new issue (ADR 0043). |
| 7.05am | The issue goes out on Instagram (ADR 0015). |
| Around 7.10am | The supervising person receives a report: what has come out, whether stored articles have been used and what has failed (ADR 0069). |
| 8.00am | A new article is written to be stored, if needed. |
| 9.00am, Sunday | “The week in video”, with the feature at the end, goes out on Instagram, X, Bluesky and LinkedIn (ADR 0027). |
| From 9.10am | A program that runs separately, on GitHub, checks that the issue has come out and, if not, publishes it with stored articles. If the paper does not respond, it checks from 7.30am (ADR 0021). |
| Wednesdays | What has been published is searched for links that have stopped working (ADR 0056). |
| On publication | A copy of each issue is saved in the Internet Archive (ADR 0046). |

## 4. No day without an issue

**An issue always comes out** (ADR 0021 and 0068). If the preparation fails twice, or has not finished by
6.30am, it goes out with stored articles, all of them or only those that are missing. If publication fails, the
program that runs separately, on GitHub, does it, and the paper does not do it again on top.

**What did not come out because of a failure comes out the next day**: if an issue went out with stored articles
because the preparation failed, the following night what was discussed on that day is also collected, and the
website says so.

**If an agent damages one of the issue's files**, the previous version is recovered and the agent repeats its
work once. And if the preparation has to start again, it does not treat as published what was written in the
first attempt (ADR 0076).

## 5. The reserve: articles kept for days without news

The paper has articles and other pieces written in advance, so that an issue is never missing (ADR 0068):

| What | How many | Withdrawn if not used within | Where it comes from |
| --- | --- | --- | --- |
| Articles | Six: two from each group | 60 days; EduMedia ones, 30 | Repository applications and Library documents that the paper had not yet covered, and tools shared some time ago in EduMedia-IAG (ADR 0077) |
| Comic strip | One | 60 days | A joke on a topic that never goes out of fashion |
| “A year ago” | Those for the next seven nights | That same night | Written in advance |
| Feature | One per week | 28 days | On a topic that never goes out of fashion (ADR 0028) |

- **When they are used**: every night, if the issue does not reach three articles or lacks a group, and
  whenever the preparation fails. The ones for the missing groups go first.
- **How they are replenished**: every morning one is written for the group with the fewest stored. It goes
  through documentalist, reviewer, illustrator and translators, like any article.
- **Before one is used**, a program checks that the page of what it covers is still open; if not, it is
  withdrawn.

## 6. The reviews

**With AI**: each task's reviewer (sources, figures, names and what has already been published), the drawing
reviewer, the comic strip judge, the verifier for the feature and for “A year ago” and, every night, a style
editor who reads the day's articles as any reader would and fixes whatever is hard to understand, without
touching the data (ADR 0083).

**With programs, without AI**, every night:

| What is checked | Decision record |
| --- | --- |
| That no agent has damaged the issue's files | ADR 0076 |
| That “quien” is not used in the sense of “la persona que”, that there are no quotations only in English, “hoy” or “ayer”, “app” or other words that the style book advises against (if there are, an agent corrects them) | ADR 0067 and 0083 |
| That the style editor has not changed any figure, link or quotation | ADR 0083 |
| That nothing is attributed to an author of the paper that belongs to another person with the same name (if it happens, an agent reviews it) | ADR 0066 |
| Typos that follow a fixed rule, such as “y” before “i”, and headlines that are too long | ADR 0059 |
| That each translation has the same articles, links and drawings as the original; if not, that part goes out in Spanish | ADR 0026 |
| That nothing has been left in Spanish in a translation | ADR 0056 |
| That no page has blank gaps, on screens of any size | ADR 0041 |
| Links that have stopped working, on Wednesdays | ADR 0056 |

**A person** can review the issue at 5.00am and ask for changes before 6.50am, but the paper does not promise
it: if there is no reply, it goes out on time (ADR 0058).

## 7. What comes out of each issue

The issue is not just the website. Several other things come out of it:

- the **alerts in the three groups** and the **private messages** to the people whose resource appears;
- the **Instagram post**, with its text;
- the **image for sharing** each article;
- on Sundays, **“The week in video”** on social media.

**If something in an issue changes before it comes out, everything that depends on it is redone**: if the comic
strip changes, the alert that mentions it; if a headline changes, its sharing image; if the feature changes, the
week's video and its texts.

## 8. Corrections

- **A wrong fact is corrected in the article, with a note at the end** and in all five languages (ADR 0055):
  “Corrected on…” (there was an error), “Update of…” (the fact was true and has changed) or “Note added on…”
  (something was missing). A typo that does not change the meaning is corrected without a note.
- Before correcting, the fact is checked against its source: a report of an error can also be mistaken.
- **An alert that has already been sent to a group is corrected** by editing it with the bot.

## 9. People, privacy and transparency

- **To know who each person is, their Telegram account is looked at, not the name they display**, because two
  people can have the same name (ADR 0066).
- **Only the author of a resource is named, and only if they published it themselves**; the groups' opinions
  are not attributed to anyone (style book).
- **Nothing is collected from readers**: the visit counter only adds up, without cookies or personal data (ADR
  0033), and comments are loaded only if the reader presses the button (ADR 0030). This is explained in the
  [privacy policy](https://diarioiaeducativa.github.io/privacidad.html) (ADR 0070).
- **A single notice that the paper is made with AI**, in the footer of every page. The page [“The
  newsroom”](https://diarioiaeducativa.github.io/redaccion.html) explains how it is made, who is answerable for
  what is published, and that there is no advertising or sponsorship (ADR 0055 and 0065).
- The programs that make the paper are public (ADR 0019).

## 10. What remains to be improved

What does not yet work entirely well or depends on a single check. This is where the paper can be improved:

- **A correction does not reach what has already been sent on its own.** If an article is corrected after
  publication, the alert that already went out in the groups has to be changed by hand, and what was published
  on Instagram and the other social networks is not changed.
- **The EduMedia articles kept for days without news from the group** began to be written on 16 November 2026:
  none has yet appeared in an issue.
- **A stored article is checked only shortly before it is published.** They are written days or weeks in
  advance, and just before one is used the only check is that the page of the tool it discusses is still open,
  not whether anything it reports has changed, for example whether it has stopped being free. That is why the
  EduMedia ones, about tools that change often, are withdrawn after a month.
- **While an article is being written for storage**, the website being prepared shows it for a few minutes as
  if it were an issue of the paper. If the website were published just then, it would go out.
- **If an agent damages a file, it is recovered automatically only in each night's preparation**, not in that of
  the feature, the Library or the Repository.
- **The translations are checked by a program**, which looks that all the articles are there and that nothing
  has been left in Spanish, but no agent reviews them.
- **When a day is considered to have few new Repository applications**, and an earlier one is brought back, was
  decided by eye and remains to be fine-tuned.
- **Instagram is tried only once**: if it fails, it has to be posted by hand.
