# AI_USAGE.md

AI assistance was used to help structure the assessment deliverables and draft an initial Python/Playwright Page Object Model test suite.

**Prompt/task given:** Create a traceable QA assessment response for the supplied Sauce Demo shopping/checkout use case, including manual cases, a Python Playwright automation design, AI-output review, AI evaluation checks, defect communication, and incident-analysis notes.

**What I reviewed and changed:** I checked that the automation cases map to the manual IDs; moved locators into page objects; moved base URL and user values into configuration/environment variables; removed fixed sleeps; used Playwright auto-waiting; made the sort assertion inspect the complete price list; made checkout validate subtotal + tax = total; added parameterized required-field checks; and added post-logout direct-URL protection coverage. The incident example is based on a real extraction-validation issue previously described by the candidate; it is explicitly presented as a project testing/validation issue and not overstated as a customer-facing production outage.

**Before submission:** Run the commands in README.md against the public practice site, verify selectors and behavior against the live practice application, and correct any environment-specific differences. AI-generated content is a draft and must be independently validated.
