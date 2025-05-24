# E-commerce Automation Project

This project contains end-to-end automation tests for an E-commerce web application using Selenium, pytest, and Allure reporting.

## Structure

- `pages/`: Page Object Model classes
- `utils/`: Utility/helper functions
- `tests/`: Test cases for various flows
- `conftest.py`: Pytest fixtures
- `requirements.txt`: Project dependencies

## How to Run

1. Install dependencies:
   pip install -r requirements.txt
2. Run tests:
   pytest --alluredir=allure-results
3. View report:
   allure serve allure-results

## Test Report Dashboard

This project supports generating a beautiful test report dashboard using **Allure**.

### How to Generate and View the Dashboard

1. **Run your tests and collect Allure results:**

   ```sh
   pytest --alluredir=allure-results
   ```

2. **Serve the Allure dashboard locally:**

   ```sh
   allure serve allure-results
   ```
   This will open an interactive dashboard in your browser with detailed test results, steps, screenshots, and more.

3. **(Optional) Generate a static HTML report:**

   ```sh
   allure generate allure-results -o allure-report --clean
   open allure-report/index.html
   ```

### Allure Features
- Interactive dashboard with test status, history, and trends
- Step-by-step breakdown of each test
- Attachments (screenshots, logs, etc.)
- Filtering and grouping by suite, feature, or tag

---

**Note:** Make sure you have Allure installed. If not, install it with:

```sh
brew install allure  # macOS
# or
pip install allure-pytest  # Python bindings (already in requirements.txt)
```

For more info, see: [Allure Documentation](https://docs.qameta.io/allure/)
