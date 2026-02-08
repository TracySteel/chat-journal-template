# Contributing

Thank you for helping make this project better. Contributions of all sizes are welcome.

## Ways To Contribute
- Fix bugs or improve the docs
- Improve the UI/UX or styling
- Add data import helpers
- Improve accessibility or performance
- Add examples or sample data

## Getting Started
1. Fork the repo and create a branch.
2. Make your changes.
3. Ensure the site runs locally:
   ```bash
   cd site
   python -m http.server 8000
   ```
4. Open a pull request with a clear description and screenshots if UI changes are involved.

## Project Structure
- `site/` host-ready static site
- `site/index.html` journal view
- `site/archive/index.html` archive view
- `site/data/` conversation data
- `site/archive/md/` archive markdown content
- `scripts/` helpers for building data

## Code Style
- Keep HTML/JS/CSS tidy and readable.
- Prefer clear, small functions.
- Avoid adding heavy dependencies.

## Content & Privacy
- Do not include real user data in commits or examples.
- Use the sample data in `site/data/` for testing.

## Reporting Issues
When filing an issue, include:
- Steps to reproduce
- Expected vs actual behavior
- Browser + OS
- Screenshots or console errors if relevant

Thank you for contributing.
