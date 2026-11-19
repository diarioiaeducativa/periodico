<!-- origen: 71fd29243d273c19 -->
# How Educational AI Daily is made

[Educational AI Daily](https://diarioiaeducativa.github.io/) gathers every morning what was discussed the day before in three open Telegram groups for teachers: ChatGPT-IA-edu (AI in education in general), Vibe Coding Educativo (teachers who build their own apps with AI) and EduMedia-IAG (images, audio and video with AI). It is written, reviewed, illustrated and translated by AI agents; a person oversees it and answers for what is published.

This document brings together the paper's rules and how they are applied, so that readers can understand how it is produced and help improve it. How it is written is set out in the [style guide](../encargos/estilo.md) and how it is translated in the [translator's guide](../encargos/traduccion.md). The reasons behind each decision are in the [decision records](adr/README.md) (ADR), which are cited by number.

Each rule says **who applies it**, **how it is checked** and, where needed, **what is still missing**. What remains to be improved is collected at the end.

## 1. The issue

**What is discussed on one day appears in the paper the next morning**, at 7.00am (Spanish mainland time), in five languages: Spanish, Catalan, Galician, Basque and English (ADR 0026).

An issue contains:

- **The day's articles**: from none to six, and from none to five briefs, depending on what the day has produced, in five sections: Tools, Vibe coding, Multimedia, Debates and Institutions and companies.
- **Library**: one article for each document added that day to the ChatGPT-IA-edu digital library (ADR 0006).
- **Repository**: up to two apps a day from the Vibe Coding Educativo resource repository; on Fridays, a summary of the week's apps (ADR 0008).
- **“A year ago”**: something that was being discussed on the same day a year earlier, compared with how things stand today (ADR 0040).
- **The cartoon** by Chalk and Algorithm, about one of the day's news items (ADR 0023).
- **On Wednesdays**, also an opinion column on a debate in the groups: the only piece in the paper that takes a side, signed by the AI model that writes it (ADR 0092).
- **On Sundays**, also a feature that explains a single topic in depth (ADR 0004 and 0028) and “The week in video”, a short video with the week's highlights (ADR 0016 and 0027). On Sunday night a commentary on the week's most important developments is also written (ADR 0038).

The rules for each issue:

| Rule | Who applies it | How it is checked |
| --- | --- | --- |
| **At least three articles.** If there are fewer, they are topped up with articles kept for such cases (the reserve, section 5). | A program, every night, before the translations (ADR 0068) | The program counts the articles. |
| **At least one article from each group.** If a group does not yield one, a stored article from that group is used. | The writing agent tries; the reviewing agent turns a brief from the missing group into an article; if one is still missing, the reserve (ADR 0076 and 0077) | The reviewer and the reserve program. |
| **Only what has been discussed in the groups.** No general AI news. | The writing agent | The reviewer compares each article with the messages. |
| **Not news**: the groups' internal organisation, greetings and personal complaints. The documents in the digital library have their own section. | The writing agent | The reviewer. |
| **Nothing already published is repeated.** If there is something new on a topic already covered, it appears as a brief, with a link to the earlier article (ADR 0011). | The writer and the reviewer, with a search tool covering everything published (ADR 0061) | The reviewer searches for each name and each headline in what has already been published. |
| **No one monopolises the issue**: as a rule, one article per person and two per product or company. | The writing agent | The reviewer. |
| **If a day does not yield a worthy issue, it is not padded out**: stored articles are used instead. | The writer and the reserve | — |
| **Opinion is separate and signed.** Only the Wednesday column takes a side: it goes in the “Opinion” section, signed by the model that writes it, with a note saying that the paper checks its facts and that the opinion is the model's own, within the paper's principles (section 10). It discusses ideas, not people: no one from the groups is named. | The columnist; the signature and the note are added by the program that builds the website (ADR 0092) | The fact-checker verifies every fact and that no one can be identified, without touching the thesis; a program checks the length and the links. |

## 2. Who does what

The agents are Claude AI models from Anthropic: Sonnet writes and reviews every day, Opus chooses the best feature and the best column, writes the long texts and repairs whatever fails, and Fable writes and chooses the cartoon. The exception is the Wednesday columnist, GPT-6.2-Astra, from OpenAI: the opinion comes from a different voice from the rest of the paper and is signed with its name (ADR 0092). **The agents that write the paper cannot run programs**: they only read and write texts and consult the internet. This way, nothing that arrives in the groups' messages, which other people write, can lead them to do anything else (ADR 0002). The messages are material to report on, never orders.

Only the repairer works with programs. It writes nothing for the paper: it acts when something fails, finds the cause and fixes it in a copy. It cannot change the text of the articles or the cartoon, or publish, and a program checks its fix before applying it (ADR 0087).

**No agent reviews what it has written itself.** Every text goes through a reviewer who did not write it, who opens each source and removes whatever cannot be confirmed (ADR 0001).

| Agent | What it does |
| --- | --- |
| Writer and reviewer | The day's articles and briefs. |
| Documentalist and reviewer | The Library and Repository articles, and the stored EduMedia ones. |
| Illustrator and drawing reviewer | A drawing that explains each article; the reviewer looks at it on its page and sends back any that is not clear (ADR 0005). |
| Scriptwriter and humour judge | Five scripts for the cartoon; the judge picks one (ADR 0023 and 0024). |
| Chronicler and fact-checker | “A year ago”. |
| Columnist, fact-checker and column judge | The Wednesday opinion column; the judge chooses between the new one and the reserve one (ADR 0092). |
| Features editor, reporter, fact-checker and features judge | The Sunday feature. |
| Commentator and reviewer | The week's commentary. |
| Video scriptwriter | “The week in video”. |
| Translators | One per language, for each text. |
| Repairer | When something fails, fixes it so that the issue can come out; it does not write or change the texts. |
| Spokesperson | Each morning's notices in the three groups and the text for Instagram. |

Everyone writes with the [style guide](../encargos/estilo.md), and each task also has its own guide.

## 3. A day in the paper

A program checks every five minutes what needs doing and records what it has already done, so that nothing is repeated. Times are Spanish mainland time: UTC+1 in winter and UTC+2 in summer.

| Time | What happens |
| --- | --- |
| 1.00am | The issue is prepared with what was discussed the previous day: the articles and their review, the drawings, the cartoon, the Library, the Repository, “A year ago”, the checks, the translations and the notices. If it fails, a second attempt is made. |
| 5.00am | The issue can be previewed before it is published, so that the supervising person can review it (ADR 0025). A program checks that the page looks right on screens of different sizes. |
| 6.30am | If the issue is still not ready, preparation is stopped and it comes out with whatever there is or with stored articles. |
| 6.50am | The website is published, and the images for sharing each article and the notices for the groups are prepared. If anything fails, it is retried every 10 minutes until 9.00am. |
| 7.00am | The Bot de IA Educativa posts the issue's notice in each group and writes privately to the people whose resource appears that day (ADR 0052). The paper's Android app announces the new issue (ADR 0043). |
| 7.05am | The issue goes out on Instagram (ADR 0015). |
| Around 7.10am | The supervising person receives a report: what has come out, whether stored articles were used and what has failed (ADR 0069). |
| 8.00am | A new article is written to keep in store, if needed, and a reserve opinion column, if none is left. |
| 9.00am, Sunday | “The week in video”, with the feature at the end, goes out on Instagram, X, Bluesky and LinkedIn (ADR 0027). |
| From 9.10am | A program that runs separately, on GitHub, checks that the issue has come out and, if not, publishes it with stored articles. If the paper does not respond, it checks from 7.30am (ADR 0021). |
| Tuesday night | The opinion column is prepared with Wednesday's issue (ADR 0092). |
| Wednesday | Links in what has been published that have stopped working are looked for (ADR 0056). |
| On publication | A copy of each issue is saved in the Internet Archive (ADR 0046). |

## 4. No day without an issue

**An issue always comes out** (ADR 0021 and 0068). If preparation fails twice, or has not finished by 6.30am, the issue comes out with stored articles, either all of them or only those that are missing. If publication fails, the program that runs separately, on GitHub, carries it out, and the paper does not do it again on top of that.

**What did not come out because of a failure comes out the next day**: if an issue came out with stored articles because preparation failed, the following night what was discussed that day is also gathered, and the website says so.

**If an agent damages one of the issue's files**, the previous version is restored and the agent repeats its work once. And if preparation has to start again, it does not treat as published what was written in the first attempt (ADR 0076).

## 5. The reserve: articles kept for days without news

The paper has articles and other pieces written in advance, so that an issue is never missing (ADR 0068):

| What | How many | Withdrawn if unused after | Where it comes from |
| --- | --- | --- | --- |
| Articles | Six: two from each group | 60 days; EduMedia ones, 30 | Apps from the Repository and documents from the Library that the paper had not yet covered, and tools shared some time ago in EduMedia-IAG (ADR 0077) |
| Cartoon | One | 60 days | A joke on a topic that never goes out of fashion |
| “A year ago” | Those for the next seven nights | That same night | Written in advance |
| Feature | One per week | 28 days | On a topic that never goes out of fashion (ADR 0028) |
| Opinion column | One | Used or discarded the following Wednesday | On a debate that does not depend on the events of a few days; the judge compares it with the new one and the better one comes out (ADR 0092) |

- **When they are used**: every night, if the issue does not reach three articles or lacks a group, and
  whenever preparation fails. The ones for the missing groups go first.
- **How they are replenished**: every morning one is written for the group with the fewest in store. It goes through
  documentalist, reviewer, illustrator and translators, like any article.
- **Before one is used**, a program checks that the page of what it covers is still open; if not, it is
  withdrawn.

## 6. Reviews

**With AI**: the reviewer for each task (sources, figures, names and what has already been published), the drawing reviewer,
the cartoon judge, the fact-checker for the feature, for “A year ago” and for the opinion column and, every night, a style editor
who reads the day's articles as any reader would and fixes whatever is hard to understand, without touching the
facts (ADR 0083).

**With programs, without AI**, every night:

| What is checked | Decision record |
| --- | --- |
| That no agent has damaged the issue's files | ADR 0076 |
| That “quien” is not used in the sense of “la persona que”, and that there are no quotations in English only, “hoy” or “ayer”, “app” or other words that the style guide discourages (if there are, an agent corrects them) | ADR 0067 and 0083 |
| That the style editor has not changed any figure, link or quotation | ADR 0083 |
| That nothing said by another person with the same name is attributed to one of the paper's authors (if it happens, an agent reviews it) | ADR 0066 |
| Typos that follow a fixed rule, such as “y” before “i”, and headlines that are too long | ADR 0059 |
| That each translation has the same articles, links and drawings as the original; if not, that part comes out in Spanish | ADR 0026 |
| That nothing has been left in Spanish in a translation | ADR 0056 |
| That no page has blank gaps, on screens of any size | ADR 0041 |
| Links that have stopped working, on Wednesdays | ADR 0056 |

**A person** may review the issue at 5.00am and ask for changes before 6.50am, but the paper does not promise it: if there is no reply, it comes out on time (ADR 0058).

## 7. What comes out of each issue

The issue is not just the website. Also produced from it are:

- the **notices in the three groups** and the **private messages** to the people whose resource appears;
- the **Instagram post**, with its text;
- the **image for sharing** each article;
- on Sundays, **“The week in video”** on social media.

**If something in an issue changes before it comes out, everything that depends on it is redone**: if the
cartoon changes, the notice that talks about it; if a headline changes, its image for sharing; if the
feature changes, the week's video and its texts.

## 8. Corrections

- **A wrong fact is corrected in the article, with a note at the end** and in all five languages (ADR
  0055): “Corregido el…” (there was an error), “Actualización del…” (the fact was true and has changed) or
  “Nota añadida el…” (something was missing). A typo that does not change the meaning is corrected without a note.
- Before correcting, the fact is checked against its source: a notice of an error may also be wrong.
- **A notice that has already been sent to a group is corrected** by editing it with the bot.

## 9. People, privacy and transparency

- **To know who each person is, their Telegram account is looked at, not the name they display**, because
  two people can have the same name (ADR 0066).
- **Only the author of a resource is named, and only if they published it themselves**; the groups' opinions are not
  attributed to anyone (style guide). The paper's only opinion of its own is the Wednesday column, signed
  by the model that writes it (ADR 0092).
- **Nothing is collected about readers**: the visit counter only adds up, with no cookies or personal
  data (ADR 0033), and comments are loaded only if the reader presses the button (ADR 0030). The
  [privacy policy](https://diarioiaeducativa.github.io/privacidad.html) explains this (ADR 0070).
- **A single notice that the paper is made with AI**, in the footer of every page. The page [“The
  newsroom”](https://diarioiaeducativa.github.io/redaccion.html) explains how it is made, who answers for
  what is published and that there is no advertising or sponsorship (ADR 0055 and 0065).
- The programs that make the paper are public (ADR 0019).

## 10. The line on opinion

The opinion column defends the stance its columnist chooses, within these principles. They are the paper's line: they do not say
what to think about each debate, but where opinion is written from.

1. **Learning comes first.** A technology is judged by what it contributes to learning and teaching, not by being new.
2. **Students' data is protected.** Nothing that forces students' personal data to be handed over to a company
   without need. Preference goes to what leaves control with the school and the teacher and what does not tie anyone to a single platform,
   without giving up what genuinely works.
3. **AI is a tool.** Behind every use there is a person who decides and answers for it. Assessing, grading and
   deciding about students is a matter for teachers.
4. **Within reach of any teacher.** What is proposed can be done without paying or knowing more than an
   ordinary teacher, and starts from how people really work in classrooms.
5. **Equity.** What only works with means or devices that not all students have is not presented as a
   general solution.
6. **Transparency.** Using AI is no cause for shame or suspicion: it is said when and how it has been used. Families
   have a right to know more than the law requires.
7. **Rigour before forcefulness.** Exact, verifiable facts, the opposing view in its best form, and neither
   alarmism nor brochure-style enthusiasm.

**Who applies them**: the columnist, who receives them with the commission and chooses within them the topic and the stance.
**How it is checked**: the fact-checker does not publish a column that goes against any of them, without changing its thesis for that reason,
and the judge discards the one that clashes with them when comparing it with the reserve one (ADR 0092).

## 11. What is still missing

What still does not work quite right or depends on a single check. It is where the paper can
be improved:

- **A correction does not reach what has already been sent by itself.** If an article is corrected after
  it is published, the notice that already went out in the groups has to be changed by hand, and what was posted on Instagram
  and the other social networks is not changed.
- **The EduMedia articles stored for days without news from the group** began to be written
  on 16 November 2026: none has yet appeared in an issue.
- **A stored article is reviewed little before it is published.** They are written days or weeks
  ahead, and just before one is used, all that is checked is that the page of the tool it
  discusses is still open, not whether anything it reports has changed, for example whether it has stopped being
  free. That is why the EduMedia ones, about tools that change often, are withdrawn after a month.
- **While an article is being written for storage**, the website being prepared shows it for
  a few minutes as if it were an issue of the paper. If the website were published just then, it would come out.
- **If an agent damages a file, it is restored on its own only in each night's preparation**, not in that of the
  feature, the Library or the Repository.
- **The translations are checked by a program**, which looks that all the articles are there and that nothing has been
  left in Spanish, but no agent reviews them.
- **When a day is considered to have few new Repository apps**, and an earlier one is rescued, was
  decided by eye and remains to be adjusted.
- **Instagram is tried only once**: if it fails, it has to be posted by hand.
