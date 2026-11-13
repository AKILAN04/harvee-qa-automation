# Section B – Answers

## B1. Review of the AI-generated cart-total test

Problems:
1. It hard-codes the public URL and credentials in the test instead of configuration/environment variables.
2. It does not use a Page Object Model; locators and workflow details are embedded in the test.
3. `text=Add to cart` is ambiguous because several products have an Add to cart button. The test does not identify which product it adds.
4. It does not assert that an item was added or that the cart contains the expected product.
5. `waitForTimeout(3000)` is a fixed sleep: slow, flaky, and unnecessary with Playwright auto-waits.
6. It goes straight to checkout without checking cart contents or the checkout information step.
7. It uses one-character checkout data without checking whether it is valid or meaningful.
8. It reads the total but only checks that some text exists. It never checks the amount, currency, arithmetic, subtotal, or tax.
9. It does not finish the order, verify confirmation, or verify that the cart is empty afterwards.
10. It has no test ID linking it to a manual test case.
11. It has no explicit test isolation strategy or evidence/reporting setup.
12. It has no useful failure message or independent validation of the expected price calculation.

Rewritten approach: use the Page Objects and `test_TC05_checkout_total_matches_subtotal_plus_tax_and_cart_is_empty` in this repository. It adds two specifically named products, completes the customer-information step, parses subtotal/tax/total, asserts `total ≈ subtotal + tax` to the cent, finishes the order, returns to products, and checks the cart badge is zero. The base URL and credentials are configurable.

## B2. AI feature evaluation – Test case generator

I would evaluate the generated JSON test-case output with a versioned golden dataset of representative user stories.

| Check | Evaluation design | Scoring |
|---|---|---|
| Requirement coverage | For each story, maintain an expert-approved checklist of positive, negative, boundary, role and state-transition requirements. Compare generated cases against the checklist and calculate covered requirements / total applicable requirements. | Automatically, with rubric-reviewed expected coverage |
| No invented requirements | Include stories that intentionally omit details. Flag assertions, limits, validations or business rules not present in the story or approved shared requirements. | Human review using a strict rubric; record unsupported-claim rate |
| Duplicate and useful cases | Detect exact duplicates and semantic duplicates; have reviewers judge whether each case adds a distinct condition or outcome. | Automatic similarity/deduplication signal plus human review |
| JSON schema and importability | Validate parseability, required keys, types, enums, escaping, and references using a JSON Schema; then run a safe import into a test workspace. | Automatically; pass/fail and schema-error rate |

I would report both an overall score and separate metrics. A syntactically valid JSON response must not receive a high quality score if it misses important requirements or invents behavior. I would also retain model/version, prompt, input story, output and evaluation result to make regressions reproducible.

## B3. Jira defect report

**Title:** [4.2.0][Products] Price sort – Low to high displays $29.99 before $15.99

**Environment:** Release 4.2.0; Chrome (record exact browser version, OS, and test environment/build URL when filing); Sauce Demo practice application.

**Precondition:** User is logged in as a valid, unlocked standard customer and the Products page is displayed.

**Steps to reproduce:**
1. Open the Products page.
2. Open the product sort dropdown.
3. Select “Price (low to high)”.
4. Review the displayed prices from top to bottom.
5. Repeat the steps to confirm reproducibility.

**Expected result:** All products are ordered by ascending numeric price; each item price is less than or equal to the next item price.

**Actual result:** A product priced at $29.99 appears before a product priced at $15.99. The issue has reproduced on every run since release 4.2.0.

**Severity:** High / major (proposed). Sorting is a core shopping function and consistently presents an incorrect order, which can mislead customers who rely on price ordering. It does not currently appear to block checkout, so it is not classified as critical. Set priority to P1 or P2 according to the client's release policy and affected customer volume.

**Evidence to attach:** Screenshot showing the selected sort option and the two out-of-order prices; short screen recording from page load through sort selection; test run/build ID; Chrome and OS versions; timestamp; console/network errors if present; and the complete ordered price list captured by the automated assertion.

## B4. Message to the product manager (under 150 words)

Hi, our release checks found two issues to consider before tomorrow’s release. First, the price-low-to-high option consistently places a $29.99 item before a $15.99 item in release 4.2.0, so customers may see misleading price order. Second, one checkout test fails roughly 1 time in 10 but passes on rerun; we are investigating whether this is a product issue or test/environment instability.

**Recommendation:** Do not release 4.2.0 with the sorting issue unresolved. A practical option is to hold the release for a focused fix and retest of sorting plus checkout. If Friday’s date cannot move, release only if the product owner accepts the sorting limitation in writing, confirms it does not affect price calculation or payment, and we complete targeted checkout checks with the intermittent failure understood. I’ll share the evidence and an updated risk assessment before the go/no-go decision.

# Section C – Live discussion preparation

## C1. How I would analyze “Checkout has been failing for some users since this morning”

1. **Clarify impact and scope:** Ask when it started, which users/regions/browsers/devices are affected, exact error/message, checkout step, order/payment impact, frequency, whether orders are duplicated or charged, and whether there is a workaround. Ask for one or two affected order/session IDs through the approved secure channel (not passwords or payment details).
2. **Triage severity:** Establish whether customers are unable to place orders, whether payments are being captured, and whether data integrity is at risk. If payment/duplicate-order risk exists, escalate immediately and follow the incident process.
3. **Check recent changes:** Review deployments, feature flags, configuration, secrets/certificates, infrastructure changes, third-party payment/shipping changes, and database migrations since the last known-good time.
4. **Inspect observability:** Correlate application/API logs, traces, metrics, browser/network errors and payment-provider status using timestamps and correlation IDs. Compare successful and failed sessions. Check latency, error rates, database connections, queue depth and resource saturation.
5. **Review test evidence:** Check CI results, smoke/regression runs, monitoring alerts, known defects and whether the issue appeared after a particular build.
6. **Reproduce safely:** Use a non-production environment and representative test accounts/data. Follow the same browser, region, cart, address and payment path. Do not create real charges. Vary one factor at a time.
7. **Narrow the layer:** Determine whether failure is in UI validation, checkout API, inventory/pricing, address/tax, payment integration, database, test data, or environment. Compare API responses and server-side logs with the UI behavior.
8. **Classify:** A product defect is repeatable with valid data in a healthy environment and tied to application behavior. A data issue follows a particular record/account. An environment or dependency issue correlates with infrastructure/configuration/provider health. Preserve evidence before changing anything.
9. **Mitigate and communicate:** Give the client an early acknowledgement with impact known so far, next update time, and immediate containment options. Update at agreed intervals even if there is no root cause yet. Once confirmed, explain customer impact, workaround, fix/rollback plan and validation evidence in plain language.
10. **Close the loop:** Verify the fix, monitor recovery, identify affected transactions, document root cause and add regression/monitoring coverage.

## C2. Recent issue identified – extraction validation

**Context and impact:** During validation of the Citroën/PSA document extraction workflow, I found that extraction could fail when a downloaded `.svgz` asset existed but was empty (0 KB). This prevented the affected asset from being processed and could interrupt or leave gaps in the document extraction/validation output. I would describe this accurately as an issue found in the project workflow during testing/validation, rather than claim it was a customer-facing production outage.

**How I found it:** The extraction run failed while processing an asset. I traced the failure to the PSA reader path that handled SVGZ assets.

**Root cause:** The code used `File.ReadLines(...).First()` and assumed the file contained at least one line. An empty file caused an exception because there was no first line to read. The missing guard meant a malformed or empty downloaded asset was not handled gracefully.

**Client/team communication:** I shared the reproducible failure and the affected processing path with the relevant project stakeholders during investigation. I explained in practical terms that an empty downloaded document could stop its extraction step, so some documents might not be available in the generated output until the issue was handled. I discussed the proposed defensive handling and reviewed the fix with the responsible colleague.

**Prevention and verification:** I updated the handling to check file existence, read the first line safely with `FirstOrDefault`, validate that a usable first row exists before attempting XML-version processing, and log missing, empty or damaged assets. The change was reviewed and committed. I would add regression fixtures for missing files, zero-byte files, malformed SVGZ content and valid SVGZ content, and verify that one bad asset is logged/skipped without silently hiding unrelated extraction failures.

**Looking back:** I would add malformed/empty-file test data earlier in the test strategy and make asset-level failure reporting more visible in the run summary. I would also agree with the client on whether an invalid asset should be skipped, retried or treated as a release-blocking validation failure.

---

# Section A – Manual test suite

## A1. Questions and assumptions

| Question for product owner | Assumption to test if unanswered |
|---|---|
| 1. Is postal code checked for a country-specific format, or only required? | Treat it as required text; do not assume a country-specific pattern. |
| 2. Can a customer add multiple quantities of the same product, or only one of each? | The UI permits one unit per product in this practice flow; verify badge count reflects cart line-item quantity. |
| 3. Should cart contents persist after logout/login or browser refresh? | Treat persistence across logout as unspecified; test refresh within the same session, and raise persistence as an open requirement. |
| 4. How should tax be rounded, and is the rate fixed or location-dependent? | Use the amount displayed by the application and verify total = displayed subtotal + displayed tax to the cent. |
| 5. What should happen if inventory becomes unavailable during checkout? | Not defined by this use case; document as an integration/business-rule gap and test only if the practice site exposes the condition. |
| 6. Which browsers, devices and viewport sizes are officially supported? | Use current Chrome desktop as baseline; perform responsive checks at a narrow mobile viewport and record observations. |
| 7. Should direct navigation to every inner route be blocked when logged out? | All authenticated inner pages, including Products and Cart, must redirect to login. |
| 8. What should Cancel do at each checkout step? | Cancel from information/overview returns to the previous shopping context without placing an order or clearing the cart. |
| 9. Are accessibility standards or keyboard-only operation required? | Target WCAG 2.1 AA practices for labels, focus, keyboard operation and meaningful accessible names. |
| 10. Are there rate limits or lockout rules after repeated invalid login attempts? | Do not infer a lockout policy beyond the explicitly provided locked-out account; avoid repeated brute-force testing on the public practice site. |

## A1. Test cases

| ID | Area | Type | Title | Pre-conditions | Steps | Test data | Expected result | Priority | Automate? and why |
|---|---|---|---|---|---|---|---|---|---|
| TC01 | Login | Positive | Standard user logs in | Login page open | Enter valid credentials; submit | standard_user / secret_sauce | Products page appears; user is authenticated | P1 | Yes – critical smoke path |
| TC02 | Login | Negative | Locked-out user cannot log in | Login page open | Enter locked-out credentials; submit | locked_out_user / secret_sauce | Clear locked-out error; remain on login page | P1 | Yes – stable negative path |
| TC03 | Sorting | Positive | Sort price low to high | Logged in; Products page | Select Price low to high; read every price | lohi | Entire price list is ascending | P1 | Yes – deterministic regression check |
| TC04 | Sorting | Positive | Sort price high to low | Logged in; Products page | Select Price high to low; read every price | hilo | Entire price list is descending | P2 | Yes – data-driven sort regression |
| TC05 | Sorting | Positive | Sort names A to Z | Logged in; Products page | Select Name A to Z; read all names | az | Names are alphabetically ascending | P2 | Yes – deterministic |
| TC06 | Sorting | Positive | Sort names Z to A | Logged in; Products page | Select Name Z to A; read all names | za | Names are alphabetically descending | P2 | Yes – deterministic |
| TC07 | Cart | Positive | Add two products and remove one on Products page | Logged in; empty cart | Add Backpack and Bike Light; remove Backpack; open cart | Two named products | Badge changes 0→2→1; cart contains only Bike Light | P1 | Yes – core cart workflow |
| TC08 | Cart | Positive | Remove item from Cart page | Logged in; one item in cart | Open cart; click Remove | Backpack | Item disappears; badge is removed/updated to zero | P2 | Yes – repeatable state check |
| TC09 | Cart | Boundary | Cart badge at zero items | Logged in; empty cart | Observe badge; open cart | Empty cart | No misleading positive count; empty state shown | P2 | Yes – simple assertion |
| TC10 | Checkout | Positive | Complete checkout and verify totals | Logged in; product(s) in cart | Checkout; enter details; continue; verify arithmetic; finish | Aki / Kumar / 641001 | Subtotal + tax = total; confirmation shown; cart emptied | P1 | Yes – end-to-end business flow |
| TC11 | Checkout | Negative | First name is required | Item in cart; information page | Leave first name blank; submit | Blank / Kumar / 641001 | Required-field error; remain on information page | P1 | Yes – parameterized validation |
| TC12 | Checkout | Negative | Last name is required | Item in cart; information page | Leave last name blank; submit | Aki / blank / 641001 | Required-field error; remain on information page | P1 | Yes – parameterized validation |
| TC13 | Checkout | Negative | Postal code is required | Item in cart; information page | Leave postal code blank; submit | Aki / Kumar / blank | Required-field error; remain on information page | P1 | Yes – parameterized validation |
| TC14 | Checkout | Positive | Cancel checkout without placing order | Item in cart; checkout information page | Select Cancel; inspect resulting page/cart | Backpack | Returns to cart/products context; no order confirmation; item remains | P2 | Yes – workflow regression |
| TC15 | Navigation/Security | Security | Logged-out user cannot open Products URL | User logged in then logged out | Navigate directly to `/inventory.html` | Direct URL | Redirect to login; protected content not visible | P1 | Yes – authorization smoke check |
| TC16 | Login | Negative | Invalid password is rejected | Login page open | Enter valid username and incorrect password | standard_user / wrong password | Error shown; no authenticated access | P1 | Yes – basic negative login |
| TC17 | Checkout | Boundary | Very long checkout field values | Item in cart; information page | Enter long first/last/postal values; continue | 256-character strings | Application handles input safely; no crash/layout break; validation follows agreed limits | P2 | No – limits unspecified; exploratory/manual until clarified |
| TC18 | Usability | Usability | Error message is understandable and recoverable | Login page open | Submit blank form; read message; correct fields | Blank then valid data | Clear actionable error; user can recover without losing entered data unnecessarily | P2 | No – wording/usability judgement |
| TC19 | Responsive | Browser/screen size | Checkout usable at mobile viewport | Browser at 375×812; item in cart | Complete checkout through overview; inspect layout and controls | 375×812 viewport | No clipped/overlapping controls; key actions reachable and readable | P2 | Partly – viewport smoke automated; visual judgement manual |
| TC20 | Accessibility | Accessibility | Keyboard-only checkout navigation | Logged in; item in cart | Use Tab/Shift+Tab/Enter/Space through cart and checkout | Keyboard only | Logical focus order; visible focus; controls operable; labels/errors announced meaningfully | P2 | No – manual assistive-tech review required |
| TC21 | Security | Security | Authenticated page blocked after logout and browser back | Logged in then logout | Use browser Back and direct URL to inventory/cart | `/inventory.html`, `/cart.html` | Protected content is not accessible; no sensitive cached page usable | P1 | Yes – navigation check; cache behavior also manual |
| TC22 | Compatibility | Browser | Core purchase flow in another supported browser | Supported browser available | Login, add item, checkout to overview | Firefox/Edge if supported | Core controls and totals behave consistently | P2 | No – depends on support matrix; run in cross-browser CI once confirmed |

### 15-minute exploratory charter – users with known problems

**Charter:** Explore the shopping journey using the practice site's known-problem accounts to discover failures that a standard-user happy-path suite may miss.

**Timebox:** 15 minutes. **Scope:** login, product listing/sorting, add/remove, cart, checkout navigation, error handling and page responsiveness. Do not test any system other than Sauce Demo.

- 0–3 min: Log in with `problem_user`; note visual anomalies, incorrect product images/names, broken controls and whether actions affect the intended product.
- 3–6 min: Sort in all four directions; compare visible order with actual names/prices; add/remove multiple items and inspect badge/cart consistency.
- 6–9 min: Attempt cart and checkout navigation; observe missing/incorrect controls, field behavior and whether errors identify the right problem.
- 9–12 min: Log out; try `performance_glitch_user` and observe unusually slow interactions without treating slowness alone as a product defect. Record timing and repeat.
- 12–15 min: If time permits, try `error_user` and `visual_user`; capture any error states, layout changes or inconsistent behavior.

**Evidence:** account type (never record password), timestamp, browser, exact steps, screenshot/video, expected versus observed behavior, and reproducibility. Avoid destructive or excessive repeated actions on the shared public site.

## A1. Strategy (under 150 words)

I would automate stable, repeatable business-critical UI flows: valid/locked-out login, all four sort orders, cart add/remove and badge behavior, checkout required-field validation, total arithmetic, order completion/cart clearing, and logged-out route protection. API tests should cover authentication authorization, cart calculations, tax/rounding, required-field validation, order creation and idempotency if the client exposes supported APIs. Unit tests should cover sorting comparators, price/tax calculations, validation rules and error mapping. Keep keyboard/screen-reader accessibility, visual layout/usability, exploratory testing with known-problem users, and ambiguous boundary behavior as manual or specialist checks. The biggest remaining risk is that the public practice site does not define real inventory, payment, tax and postal-code rules; a successful UI flow cannot prove the client’s production integrations or transaction integrity.
