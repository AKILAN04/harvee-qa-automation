# Harvee Technologies – QA Automation Assessment

## Stack
Python, Playwright, pytest, Page Object Model, pytest-html.

## Setup
1. Install Python 3.10+.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
4. Copy `.env.example` to `.env` or export the variables in your shell. Defaults are the public Sauce Demo practice credentials. The tests read configuration from `config.py` and environment variables; credentials are not embedded in test bodies.

## Run
```bash
pytest --browser chromium --html=artifacts/report.html --self-contained-html
```
Run a single case:
```bash
pytest -k TC03 --browser chromium
```
The `page` fixture is isolated per test. No fixed sleeps are used; Playwright actions and URL assertions use its auto-waiting behavior. Failed-test screenshots are saved by pytest-playwright's screenshot-on-failure support when configured with `--screenshot only-on-failure`; use:
```bash
pytest --browser chromium --screenshot only-on-failure --html=artifacts/report.html --self-contained-html
```

## Manual-to-automated traceability
| Manual ID | Automated test |
|---|---|
| TC01 | `test_TC01_standard_user_can_log_in` |
| TC02 | `test_TC02_locked_out_user_sees_error` |
| TC03 | `test_TC03_sort_price_low_to_high_checks_entire_list` |
| TC04 | `test_TC04_add_two_remove_one_updates_badge_and_cart` |
| TC05 | `test_TC05_checkout_total_matches_subtotal_plus_tax_and_cart_is_empty` |
| TC06 | `test_TC06_TC07_TC08_checkout_required_fields[missing-first-name]` |
| TC07 | `test_TC06_TC07_TC08_checkout_required_fields[missing-last-name]` |
| TC08 | `test_TC06_TC07_TC08_checkout_required_fields[missing-postal-code]` |
| TC09 | `test_TC09_logged_out_user_cannot_open_inventory_by_url` |
| TC10–TC22 | Manual only; see assessment document and `ANSWERS.md` |

## Growing the suite to 200 tests
Keep page objects focused on reusable page behavior and move repeated business actions into small workflow helpers. Group tests by feature and risk, use data-driven tests for valid/invalid inputs, and add API or service-level tests where supported so most combinations do not require a browser. Run a small smoke suite on every change and distribute the broader regression suite across CI workers. Add stable test data setup/cleanup, tags, ownership, flaky-test quarantine with expiry, and trend reporting. Review selectors for accessible roles or stable test IDs, avoid shared mutable state, and monitor runtime and failure causes so the suite remains maintainable rather than merely growing in count.
