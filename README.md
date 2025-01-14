# Selenium Wrapper

A Python wrapper for Selenium WebDriver with enhanced functionality for web testing and automation.

## Installation

```bash
pip install selenium-wrapper
```

## Build Package

1. Install build dependencies:
```bash
python -m pip install --upgrade pip
python -m pip install build twine
```

2. Build the package:
```bash
python -m build
```
This will create both wheel (.whl) and source (.tar.gz) distributions in the `dist/` directory.

## Publishing to GitHub Packages

1. Configure GitHub authentication:
```bash
# Create or edit ~/.pypirc
[distutils]
index-servers = github

[github]
repository = https://upload.pkg.github.com/usit-support
username = YOUR_GITHUB_USERNAME
password = YOUR_GITHUB_TOKEN
```

2. Upload to GitHub Packages:
```bash
# Ensure you have a valid GITHUB_TOKEN with write:packages permission
python -m twine upload --repository github dist/*
```

3. Install from GitHub Packages:
```bash
# Create or edit ~/.pip/pip.conf
[global]
index-url = https://YOUR_GITHUB_USERNAME:YOUR_GITHUB_TOKEN@pkg.github.com/usit-support/selenium-wrapper/

# Then install the package
pip install selenium-wrapper
```

4. Alternative installation using environment variables:
```bash
export GITHUB_TOKEN=YOUR_GITHUB_TOKEN
pip install --index-url https://YOUR_GITHUB_USERNAME:${GITHUB_TOKEN}@pkg.github.com/usit-support/selenium-wrapper/ selenium-wrapper
```

## Dependencies

### Selenium
https://www.selenium.dev/selenium/docs/api/py/

### Chrome
https://googlechromelabs.github.io/chrome-for-testing/#stable

### ChromeDriver
https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.264/mac-arm64/chromedriver-mac-arm64.zip