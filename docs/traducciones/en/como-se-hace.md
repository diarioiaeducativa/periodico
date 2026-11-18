<!-- origen: 8926fe5a836f7d0b -->
# How Educational AI Daily is made

[Educational AI Daily](https://diarioiaeducativa.github.io/) gathers every morning what was discussed the previous day in three open Telegram groups for teachers: ChatGPT-IA-edu (AI in education in general), Vibe Coding Educativo (teachers who build their own applications with AI) and EduMedia-IAG (images, audio and video with AI). It is written, reviewed, illustrated and translated by AI agents; a person supervises it and answers for what is published.

This document brings together the paper's rules and how they are applied, so that readers can understand how it is produced and help improve it. How it is written is set out in the [style guide](../encargos/estilo.md) and how it is translated, in the [translator's handbook](../encargos/traduccion.md). The reasons behind each decision are in the [decision records](adr/README.md) (ADR), which are cited by number.

Each rule says **who applies it**, **how it is checked** and, where necessary, **what is missing**. What still needs improving is collected at the end.

## 1. The issue

**What is discussed on one day appears in the paper the next morning**, at 7.00am, in five languages: Spanish, Catalan, Galician, Basque and English (ADR 0026).

An issue contains:

- **The day's articles**: from none to six, and from none to five briefs, depending on what the day has produced, in five sections: Tools, Vibe coding, Multimedia, Debates and Institutions and companies.
- **Library**: one article for each document added that day to the ChatGPT-IA-edu digital library (ADR 0006).
- **Repository**: up to two applications a day from the Vibe Coding Educativo resource repository; on Fridays, a summary of the week's (ADR 0008).
- **“A Year Ago”**: something that was being discussed on the same day a year earlier, compared with how things stand today (ADR 0040).
- **The cartoon** by Chalk and Algorithm, on one of the day's news items (ADR 0023).
- **On Sunday**, in addition, a feature that explains a single subject in depth (ADR 0004 and 0028) and “The Week in Video”, a short video with the week's highlights (ADR 0016 and 0027). On Sunday night a commentary on the most important things of the week is also written (ADR 0038).

The rules for each issue:

| Rule | Who applies it | How it is checked |
| --- | --- | --- |
| **At least three articles.** If there are too few, they are made up with articles kept in store for such cases (the reserve, section 5). | A program, every night, before the translations (ADR 0068) | The program counts the articles. |
| **At least one article from each group.** If a group does not yield any, a stored one from that group is used. | The writing agent tries; the reviewing agent turns a brief from the missing group into an article; if one is still missing, the reserve (ADR 0076 and 0077) | The reviewer and the reserve program. |
| **Only what has been discussed in the groups.** No general AI news. | The writing agent | The reviewer compares each article with the messages. |
| **Not news**: the groups' internal organisation, greetings and personal complaints. The documents in the digital library have their own section. | The writing agent | The reviewer. |
| **Nothing already published is repeated.** If there is something new on a subject already covered, it appears as a brief, with a link to the earlier article (ADR 0011). | The writer and the reviewer, with a search tool covering everything published (ADR 0061) | The reviewer looks up every name and every headline in what has already been published. |
| **No one monopolises an issue**: as a rule, one article per person and two per product or company. | The writing agent | The reviewer. |
| **If a day does not yield a worthy issue, it is not padded out**: stored articles are used instead. | The writer and the reserve | — |

## 2. Who does what

The agents are Claude AI models from Anthropic: Sonnet writes and reviews every day, Opus chooses the best feature, writes the long texts and repairs what breaks, and Fable writes and chooses the cartoon. **The agents that write the paper cannot run programs**: they only read and write texts and consult the internet. That way, nothing that arrives in the groups' messages, which are written by other people, can make them do something else (ADR 0002). The messages are material to report on, never orders.

Only the repairer works with programs. It writes nothing for the paper: it acts when something fails, finds the cause and fixes it in a copy. It cannot change the text of the articles or the cartoon, nor publish, and a program checks its fix before applying it (ADR 0087).

**No agent reviews what it has written itself.** Every text goes through a reviewer who did not write it, who opens each source and removes what cannot be confirmed (ADR 0001).

| Agent | What it does |
| --- | --- |
| Writer and reviewer | The day's articles and briefs. |
| Documentalist and reviewer | The articles for the Library and the Repository, and the stored EduMedia ones. |
| Illustrator and drawings reviewer | A drawing that explains each article; the reviewer looks at it on its page and sends back any that cannot be understood (ADR 0005). |
| Scriptwriter and humour judge | Five scripts for the cartoon; the judge chooses one (ADR 0023 and 0024). |
| Chronicler and verifier | “A Year Ago”. |
| Features editor, reporter, verifier and features judge | The Sunday feature. |
| Commentator and reviewer | The commentary of the week. |
| Video scriptwriter | “The Week in Video”. |
| Translators | One per language, for each text. |
| Repairer | When something fails, fixes it so that the issue goes out; it neither writes nor changes the texts. |
| Spokesperson | Each morning's notices in the three groups and the text for Instagram. |

All of them write following the [style guide](../encargos/estilo.md), and each task also has its own guide.

## 3. A day at the paper

A program checks every five minutes what needs to be done and notes what it has already done, so that nothing is repeated.

| Time | What happens |
| --- | --- |
| 1.00am | The issue is prepared with what was discussed the previous day: the articles and their review, the drawings, the cartoon, the Library, the Repository, “A Year Ago”, the checks, the translations and the notices. If it fails, a second attempt is made. |
| 5.00am | The issue can be viewed before publication, so that the supervising person can review it (ADR 0025). A program checks that the page looks right on screens of different sizes. |
| 6.30am | If the issue is still not ready, preparation is stopped and it goes out with whatever there is or with stored articles. |
| 6.50am | The website is published, and the images for sharing each article and the notices for the groups are prepared. If anything fails, it is retried every 10 minutes until 9.00am. |
| 7.00am | The Bot de IA Educativa posts the notice of the issue in each group and writes privately to the people whose resource appears that day (ADR 0052). The paper's Android app announces the new issue (ADR 0043). |
| 7.05am | The issue goes out on Instagram (ADR 0015). |
| Around 7.10am | The supervising person receives a report: what has gone out, whether stored articles were used and what has failed (ADR 0069). |
| 8.00am | A new article is written to keep in store, if needed. |
| 9.00am, Sunday | “The Week in Video”, with the feature at the end, goes out on Instagram, X, Bluesky and LinkedIn (ADR 0027). |
| From 9.10am | A program that runs separately, on GitHub, checks that the issue has gone out and, if not, publishes it with stored articles. If the paper does not respond, it checks as early as 7.30am (ADR 0021). |
| Wednesday | Published articles are searched for links that have stopped working (ADR 0056). |
| On publication | A copy of each issue is saved in the Internet Archive (ADR 0046). |

## 4. No day without an issue

**An issue always goes out** (ADR 0021 and 0068). If preparation fails twice, or has not finished by 6.30am, the issue goes out with stored articles, all of them or only those that are missing. If publication fails, the program that runs separately, on GitHub, carries it out, and the paper does not do it again on top.

**What did not appear because of a failure appears the next day**: if an issue went out with stored articles because preparation failed, the following night what was discussed on that day is also picked up, and the website says so.

**If an agent damages a file in the issue**, the previous version is recovered and the agent repeats its work once. And if preparation has to start again, it does not treat as published what was written in the first attempt (ADR 0076).

## 5. The reserve: articles kept in store for days without news

The paper has articles and other pieces written in advance, so that an issue is never missing (ADR 0068):

| What | How many | Withdrawn if not used within | Where it comes from |
| --- | --- | --- | --- |
| Articles | Six: two from each group | 60 days; EduMedia ones, 30 | Applications from the Repository and documents from the Library that the paper had not yet covered, and tools shared some time ago in EduMedia-IAG (ADR 0077) |
| Cartoon | One | 60 days | A joke on a subject that never goes out of fashion |
| “A Year Ago” | Those for the next seven nights | That same night | They are written in advance |
| Feature | One per week | 28 days | On a subject that never goes out of fashion (ADR 0028) |

- **When they are used**: every night, if the issue does not reach three articles or lacks a group, and whenever preparation fails. First, those from the groups that are missing.
- **How they are replenished**: every morning one is written for the group with the fewest in store. It goes through documentalist, reviewer, illustrator and translators, like any article.
- **Before one is used**, a program checks that the page of what it covers is still open; if not, it is withdrawn.

## 6. The reviews

**With AI**: each task's reviewer (sources, figures, names and what has already been published), the drawings reviewer, the cartoon judge, the verifier of the feature and of “A Year Ago” and, every night, a style editor who reads the day's articles as an ordinary reader would and fixes whatever is hard to understand, without touching the facts (ADR 0083).

**With programs, without AI**, every night:

| What is checked | Decision record |
| --- | --- |
| That no agent has damaged the issue's files | ADR 0076 |
| That “quien” is not used in the sense of “la persona que”, that there are no quotations only in English, no “hoy” or “ayer”, “app” or other words that the style guide discourages (if there are, an agent corrects them) | ADR 0067 and 0083 |
| That the style editor has not changed any figure, link or quotation | ADR 0083 |
| That nothing is attributed to an author of the paper that belongs to another person with the same name (if it happens, an agent reviews it) | ADR 0066 |
| Typos that follow a fixed rule, such as “y” before “i”, and headlines that are too long | ADR 0059 |
| That each translation has the same articles, links and drawings as the original; if not, that part goes out in Spanish | ADR 0026 |
| That nothing has been left in Spanish in a translation | ADR 0056 |
| That no page has blank gaps, on screens of any size | ADR 0041 |
| Links that have stopped working, on Wednesdays | ADR 0056 |

**A person** may review the issue at 5.00am and ask for changes before 6.50am, but the paper does not promise it: if there is no reply, it goes out on time (ADR 0058).

## 7. What goes out from each issue

The issue is not just the website. From it there also go out:

- the **notices in the three groups** and the **private messages** to the people whose resource appears;
- the **Instagram post**, with its text;
- the **image for sharing** each article;
- on Sunday, **“The Week in Video”** on social media.

**If something changes in an issue before it goes out, everything that depends on it is redone**: if the cartoon changes, the notice that mentions it; if a headline changes, its image for sharing; if the feature changes, the week's video and its texts.

## 8. Corrections

- **A wrong fact is corrected in the article, with a note at the end** and in all five languages (ADR 0055): “Corregido el…” (there was an error), “Actualización del…” (the fact was true and has changed) or “Nota añadida el…” (something was missing). A typo that does not change the meaning is corrected without a note.
- Before correcting, the fact is checked at its source: a report of an error may also be wrong.
- **A notice that has already been sent to a group is corrected** by editing it with the bot.

## 9. People, privacy and transparency

- **To know who each person is, their Telegram account is consulted, not the name they display**, because two people can have the same name (ADR 0066).
- **Only the author of a resource is named, and only if they published it themselves**; the groups' opinions are not attributed to anyone (style guide).
- **Nothing is collected from readers**: the visit counter only adds up, with no cookies or personal data (ADR 0033), and comments are loaded only if the reader presses the button (ADR 0030). The [privacy policy](https://diarioiaeducativa.github.io/privacidad.html) explains it (ADR 0070).
- **A single notice that the paper is made with AI**, in the footer of every page. The page [“The editorial team”](https://diarioiaeducativa.github.io/redaccion.html) explains how it is made, who answers for what is published and that there is no advertising or sponsorship (ADR 0055 and 0065).
- The programs that make the paper are public (ADR 0019).

## 10. What still needs improving

What still does not work quite right or depends on a single check. It is where the paper can be improved:

- **A correction does not reach what has already been sent by itself.** If an article is corrected after publication, the notice that already went out in the groups has to be changed by hand, and what was published on Instagram and the other networks is not changed.
- **The EduMedia articles kept in store for days without news from the group** began to be written on 16 November 2026: none has yet appeared in an issue.
- **A stored article is reviewed only shortly before publication.** They are written days or weeks in advance, and just before one is used the only check is that the page of the tool it discusses is still open, not whether anything it reports has changed, for example whether it has stopped being free. That is why the EduMedia ones, about tools that change often, are withdrawn after a month.
- **While an article is being written for storage**, the website being prepared shows it for a few minutes as if it were an issue of the paper. If the website were published at just that moment, it would go out.
- **If an agent damages a file, it is recovered automatically only in each night's preparation**, not in that of the feature, the Library or the Repository.
- **The translations are checked by a program**, which verifies that all the articles are there and that nothing has been left in Spanish, but no agent reviews them.
- **When a day is considered to have few new applications from the Repository**, and an earlier one is brought back, was decided by eye and remains to be adjusted.
- **Instagram is tried only once**: if it fails, it has to be published by hand.
