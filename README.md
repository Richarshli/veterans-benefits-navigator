# Veterans Benefits Navigator

An independent, open-source dashboard that helps Veterans, service members, survivors, dependents, and caregivers find official U.S. Department of Veterans Affairs benefit information.

## Features

- Searchable benefit cards
- Filters for major benefit categories
- Direct links to official VA pages
- VA facility and office locator links
- Claims and application shortcuts
- Crisis-support banner
- Daily official-source availability checks
- Automated debugger and unit tests
- GitHub Pages-ready static website
- Accessible, responsive interface

## Important Notice

This project is informational only. It does not determine eligibility, submit claims, provide legal advice, or represent the U.S. Department of Veterans Affairs. Always confirm requirements and decisions directly with VA or an accredited representative.

## Run Locally

```bash
python -m http.server 8000
```

Open `http://localhost:8000`.

## Automation

- `.github/workflows/daily-update.yml` checks official sources daily and commits updated source-health data.
- `.github/workflows/debugger.yml` runs repository validation and tests.

## Project Structure

```text
.github/workflows/  GitHub Actions
config/           Benefit and source configuration
data/current/       Current dashboard data
data/history/       Update history
docs/               Documentation
reports/            Debug reports
scripts/            Updater and debugger
tests/              Automated tests
```

## License

MIT License. See `LICENSE`.
