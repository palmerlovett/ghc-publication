---
name: Task scope discipline
description: User expects tasks limited strictly to what they asked; no extras, no "make it all pass" additions
---
The user explicitly manages parts of this Django project themselves (templates in particular) and expects each task to do exactly what was asked — e.g. "write the views" means only the views file, not URL routing, placeholder templates, or fixes to their own files.

**Why:** On the web-app views task I added routes, placeholder templates, and edited the user's templates to make all pages return 200. The user pushed back: "i did not ask to do the routes... I wasn't expecting everything to test perfectly."

**How to apply:** Scope plan files and implementation to the literal request. If completion review demands extras beyond the user's ask, prefer explaining the intentional gap (drift_reason) over adding unrequested files. Never modify user-authored templates without asking; flag issues instead.
