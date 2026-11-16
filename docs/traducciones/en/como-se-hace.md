<!-- origen: 1c00f6a8d9a89f7c -->
# How Educational AI Daily is made

[Educational AI Daily](https://diarioiaeducativa.github.io/) gathers every morning what was
discussed the previous day in three open Telegram groups for teachers: ChatGPT-IA-edu (AI in education
in general), Vibe Coding Educativo (teachers who build their own apps with AI) and EduMedia-IAG (images,
audio and video with AI). It is written, reviewed, illustrated and translated by AI agents; one person
supervises it and answers for what is published.

This document brings together the paper's rules and how they are applied, so that readers can understand
how it is produced and help improve it. How it is written is set out in the [style book](../encargos/estilo.md)
and how it is translated in the [translator's guide](../encargos/traduccion.md). The reasons behind each
decision are in the [decision records](adr/README.md) (ADRs), which are cited by number.

Each rule says **who applies it**, **how it is checked** and, where necessary, **what is still missing**.
What remains to be improved is collected at the end.

## 1. The issue

**What is discussed on one day appears in the paper the next morning**, at 7.00am, in five languages:
Spanish, Catalan, Galician, Basque and English (ADR 0026).

An issue contains:

- **The day's articles**: from none to six, and from none to five short items, depending on what the day
  has produced, in five sections: Tools, Vibe coding, Multimedia, Debates and Institutions and companies.
- **Library**: one article for each document added that day to the ChatGPT-IA-edu digital library
  (ADR 0006).
- **Repository**: up to two apps a day from the Vibe Coding Educativo resource repository; on Fridays, a
  summary of the week's apps (ADR 0008).
- **“A year ago”**: something that was being discussed on the same day a year earlier, compared with how
  things stand today (ADR 0040).
- **The cartoon** by Tiza y Algoritmo, about one of the day's stories (ADR 0023).
- **On Sundays**, also a feature that explains a single topic in depth (ADR 0004 and 0028) and “The week
  in video”, a short video with the week's highlights (ADR 0016 and 0027). On Sunday night a commentary
  on the most important events of the week is also written (ADR 0038).

The rules for each issue:

| Rule | Who applies it | How it is checked |
| --- | --- | --- |
| **At least three articles.** If there are fewer, they are topped up with articles kept in store for such cases (the reserve, section 5). | A program, every night, before the translations (ADR 0068) | The program counts the articles. |
| **At least one article from each group.** If a group does not yield even one, a stored article from that group goes in. | The writing agent tries; the reviewing agent turns a short item from the missing group into an article; if one is still missing, the reserve (ADR 0076 and 0077) | The reviewer and the reserve program. |
| **Only what has been discussed in the groups.** No general news about AI. | The writing agent | The reviewer compares each article with the messages. |
| **Not news**: the groups' internal organisation, greetings and personal complaints. The documents in the digital library have their own section. | The writing agent | The reviewer. |
| **Nothing already published is repeated.** If there is something new on a topic already covered, it appears as a short item, with a link to the earlier article (ADR 0011). | The writer and the reviewer, with a search tool covering everything published (ADR 0061) | The reviewer searches for every name and every headline in what has already been published. |
| **Nobody hogs the issue**: as a rule, one article per person and two per product or company. | The writing agent | The reviewer. |
| **If a day does not yield a worthy issue, it is not padded out**: stored articles appear instead. | The writer and the reserve | — |

## 2. Who does what

The agents are Claude AI models from Anthropic: Sonnet writes and reviews every day, and Opus chooses
(the best cartoon, the best feature) and writes the long texts. **The agents cannot run programs**: they
only read and write text and consult the internet. This way, nothing in the messages from the groups,
which are written by other people, can lead them to do anything else (ADR 0002). The messages are
material to report on, never orders.

**No agent reviews what it has written itself.** Every text goes to a reviewer who did not write it, who
opens every source and removes whatever cannot be confirmed (ADR 0001).

| Agent | What it does |
| --- | --- |
| Writer and reviewer | The day's articles and short items. |
| Documentalist and reviewer | The Library and Repository articles and the stored EduMedia ones. |
| Illustrator and drawings reviewer | A drawing that explains each article; the reviewer looks at it on its page and sends back any that cannot be understood (ADR 0005). |
| Scriptwriter and humour judge | Five scripts for the cartoon; the judge picks one (ADR 0023 and 0024). |
| Chronicler and verifier | “A year ago”. |
| Features editor, reporter, verifier and features judge | The Sunday feature. |
| Commentator and reviewer | The commentary of the week. |
| Video scriptwriter | “The week in video”. |
| Translators | One per language, for each text. |
| Spokesperson | The morning notices in the three groups and the text for Instagram. |

All of them write following the [style book](../encargos/estilo.md), and each task also has its own guide.

## 3. A day at the paper

A program checks every five minutes what needs doing and records what it has already done, so that
nothing is repeated.

| Time | What happens |
| --- | --- |
| 1.00am | The issue is prepared from what was discussed the previous day: the articles and their review, the drawings, the cartoon, the Library, the Repository, “A year ago”, the checks, the translations and the notices. If it fails, a second attempt is made. |
| 5.00am | The issue can already be viewed before it is published, so that the supervisor can review it (ADR 0025). A program checks that the page looks right on screens of different sizes. |
| 6.30am | If the issue is still not ready, the attempt is stopped and it goes out with whatever there is or with stored articles. |
| 6.50am | The website is published, and the images for sharing each article and the notices for the groups are prepared. If something fails, it is retried every 10 minutes until 9.00am. |
| 7.00am | The Bot de IA Educativa posts the notice of the issue in each group and writes privately to the people whose resource appears that day (ADR 0052). The paper's Android app announces the new issue (ADR 0043). |
| 7.05am | The issue goes out on Instagram (ADR 0015). |
| Around 7.10am | The supervisor receives a report: what has gone out, whether stored articles were used and what has failed (ADR 0069). |
| 8.00am | A new article is written for the reserve, if needed. |
| 9.00am, Sunday | “The week in video”, with the feature at the end, goes out on Instagram, X, Bluesky and LinkedIn (ADR 0027). |
| From 9.10am | A program that runs separately, on GitHub, checks that the issue has gone out and, if not, publishes it with stored articles. If the paper does not respond, it checks as early as 7.30am (ADR 0021). |
| Wednesday | Everything published is searched for links that have stopped working (ADR 0056). |
| On publication | A copy of each issue is saved in the Internet Archive (ADR 0046). |

## 4. No day without an issue

**An issue always comes out** (ADR 0021 and 0068). If the preparation fails twice, or has not finished by
6.30am, the issue goes out with stored articles, either all of them or only those that are missing. If
publication fails, the separate program on GitHub carries it out, and the paper does not do it again on
top of that.

**What did not come out because of a failure comes out the next day**: if an issue went out with stored
articles because the preparation failed, the following night what was discussed that day is picked up as
well, and the website says so.

**If an agent corrupts one of the issue's files**, the previous version is restored and the agent repeats
its work once. And if the preparation has to start again, it does not treat as published what was written
in the first attempt (ADR 0076).

## 5. The reserve: stored articles for days without news

The paper has articles and other items written in advance, so that an issue is never missing (ADR 0068):

| What | How many | Withdrawn if unused after | Where it comes from |
| --- | --- | --- | --- |
| Articles | Six: two from each group | 60 days; EduMedia ones, 30 | Apps from the Repository and documents from the Library that the paper had not yet covered, and tools shared some time ago in EduMedia-IAG (ADR 0077) |
| Cartoon | One | 60 days | A joke on a topic that never goes out of fashion |
| “A year ago” | Those for the next seven nights | That same night | Written in advance |
| Feature | One per week | 28 days | On a topic that never goes out of fashion (ADR 0028) |

- **When they are used**: every night, if the issue does not reach three articles or lacks a group, and
  whenever the preparation fails. Those for the missing groups go first.
- **How they are replenished**: every morning one is written for the group with the fewest in store. It
  goes through documentalist, reviewer, illustrator and translators, like any article.
- **Before one is used**, a program checks that the page of the thing it covers is still open; if not, it
  is withdrawn.

## 6. The reviews

**With AI**: each task's reviewer (sources, figures, names and what has already been published), the
drawings reviewer, the cartoon judge, the verifier of the feature and of “A year ago” and, every night, a
style editor who reads the day's articles as any reader would and fixes whatever is hard to understand,
without touching the facts (ADR 0083).

**With programs, without AI**, every night:

| What is checked | Decision record |
| --- | --- |
| That no agent has corrupted the issue's files | ADR 0076 |
| That “quien” is not used in the sense of “la persona que” (“the person who”), and that there are no quotations only in English, “hoy” or “ayer”, “app” or other words that the style book discourages (if there are, an agent corrects them) | ADR 0067 and 0083 |
| That the style editor has not changed any figure, link or quotation | ADR 0083 |
| That nothing said by someone else with the same name is attributed to one of the paper's authors (if it happens, an agent looks into it) | ADR 0066 |
| Typos that follow a fixed rule, such as “y” before “i”, and headlines that are too long | ADR 0059 |
| That each translation has the same articles, links and drawings as the original; if not, that part appears in Spanish | ADR 0026 |
| That nothing has been left in Spanish in a translation | ADR 0056 |
| That no page has blank gaps, on screens of any size | ADR 0041 |
| Links that have stopped working, on Wednesdays | ADR 0056 |

**A person** may review the issue at 5.00am and ask for changes before 6.50am, but the paper does not
promise this: if there is no reply, it goes out on time (ADR 0058).

## 7. What comes out of each issue

The issue is not just the website. Several other things come out of it:

- the **notices in the three groups** and the **private messages** to the people whose resource appears;
- the **Instagram post**, with its text;
- the **image for sharing** each article;
- on Sundays, **“The week in video”** on social media.

**If anything in an issue changes before it comes out, everything that depends on it is redone**: if the
cartoon changes, the notice that mentions it; if a headline changes, its image for sharing; if the
feature changes, the video of the week and its texts.

## 8. Corrections

- **A wrong fact is corrected in the article, with a note at the end** and in all five languages (ADR
  0055): “Corrected on…” (there was an error), “Updated on…” (the fact was true and has changed) or
  “Note added on…” (something was missing). A typo that does not change the meaning is corrected without
  a note.
- Before correcting, the fact is checked at its source: a report of an error can also be wrong.
- **A notice that has already been sent to a group is corrected** by editing it with the bot.

## 9. People, privacy and transparency

- **To know who each person is, their Telegram account is checked, not the name they display**, because
  two people can have the same name (ADR 0066).
- **Only the author of a resource is named, and only if they published it themselves**; the groups'
  opinions are not attributed to anyone (style book).
- **Nothing is collected from readers**: the visit counter only adds up, without cookies or personal data
  (ADR 0033), and comments are loaded only if the reader presses the button (ADR 0030). The
  [privacy policy](https://diarioiaeducativa.github.io/privacidad.html) explains this (ADR 0070).
- **A single notice that the paper is made with AI**, in the footer of every page. The page [“The
  newsroom”](https://diarioiaeducativa.github.io/redaccion.html) explains how it is made, who answers for
  what is published and that there is no advertising or sponsorship (ADR 0055 and 0065).
- The programs that make the paper are public (ADR 0019).

## 10. What is still missing

What still does not work quite right or depends on a single check. This is where the paper can be
improved:

- **A correction does not reach what has already been sent on its own.** If an article is corrected after
  it has been published, the notice that has already gone out in the groups has to be changed by hand,
  and what was posted on Instagram and the other networks is not changed.
- **The EduMedia articles stored for days without news from the group** began to be written on 16
  November 2026: none has yet appeared in an issue.
- **A stored article is reviewed only shortly before publication.** They are written days or weeks in
  advance, and just before one is used the only check is that the page of the tool it talks about is
  still open, not whether anything it says has changed, for example whether it has stopped being free.
  That is why the EduMedia ones, about tools that change often, are withdrawn after a month.
- **While an article is being written for the reserve**, the website being prepared shows it for a few
  minutes as if it were an issue of the paper. If the website were published right then, it would go out.
- **If an agent corrupts a file, it is only recovered automatically in each night's preparation**, not in
  that of the feature, the Library or the Repository.
- **The translations are checked by a program**, which looks that all the articles are there and that
  nothing has been left in Spanish, but no agent reviews them.
- **When a day is considered to have few new apps from the Repository**, and an earlier one is brought
  back, was decided by eye and still needs adjusting.
- **Instagram is tried only once**: if it fails, it has to be posted by hand.
