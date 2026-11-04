---
marp: true
title: A cache for the course search
minutes: 5
---

# A cache for the course search

Priya Rao, platform team

<!--
Thank you to the platform team for the time today.
Every morning at nine, three thousand students open the course search, and the page slows to a crawl.
In the next five minutes I'll show you how we cut that wait to under a second.
-->

---

# Students wait eight seconds at nine

- 3,000 searches in ten minutes
- 8 seconds for each page
- 1 in 5 students gives up

<!--
Students wait eight seconds for each search page when registration opens.
That's at nine every morning, when three thousand students search in ten minutes.
One student in five gives up and tries again later.
And each retry adds more load to the same database, so the next search is slower still.
The wait grows worse for ten minutes, and then it fades.
For you, the wait means more help tickets and angry email.
-->

---

# Database reads cause the wait

![A bar for each step of one search, with the database read the longest bar](timing.png)

Time for each step of one search

<!--
Here's where the eight seconds go.
Each bar is one step of a single search, and the long bar is the database read.
The database reads the same course rows again for every student.
Most students search for the same twenty courses.
As a result, the database repeats one job three thousand times.
The fix had to take that repeated work away.
-->

---

# Cached pages skip the database

- Keep each result page for one minute
- Serve the copy to the next student
- Clear the copy when a course changes

<!--
Our approach was simple, and that was the point.
We keep each result page in memory for one minute.
The next student who asks for the same page gets the copy, with no database read.
When a teacher changes a course, we clear the copies for that course at once.
A student never sees a stale seat count for longer than a minute.
We chose memory over a new database, because memory needs no new server.
The whole change is about two hundred lines of code.
-->

---

# Hit rate sets the load

$$ \text{reads} = (1 - h) \times \text{searches} $$

h is the share of searches that find a copy

<!--
How much does the cache save?
The number of database reads is the share of searches that miss the cache, times the number of searches.
We call the share that finds a copy the hit rate.
At a hit rate of nine in ten, the database does one tenth of the work.
At a hit rate of one half, it does half the work.
So the hit rate is the number to watch.
-->

---

# Short copies failed at first

- Ten-second copies missed most searches
- One-minute copies hit nine in ten

<!--
Our first try didn't work.
We kept each copy for ten seconds, because we feared stale seat counts.
Most searches came too late and missed the copy.
A one-minute copy hit nine searches in ten, and teachers saw no wrong counts.
-->

---

# Search time fell to under a second

![Search time each morning, before and after the cache, with a drop on the day it started](result.png)

Search time at nine, for four weeks

<!--
Here's the result.
Search time at nine fell from eight seconds to under one second.
Help tickets about the search fell by half in the first week.
The database now runs at a third of its old load at peak.
And the students who used to give up now finish their search on the first try.
-->

---

# Timetable page gets the cache next

- Cache the timetable page
- Share the cache between servers

<!--
Next, we'll use the same cache for the timetable page.
We'll also share the cache between servers, so a copy on one server helps them all.
Thank you to Sam and Lee, who built it with me, and to you for listening.
-->
