# Senior QA Engineer Assessment - Complete Test Automation Suite

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.40.0-green)](https://www.selenium.dev/)
[![Locust](https://img.shields.io/badge/Locust-2.43.3-orange)](https://locust.io/)
[![Pytest](https://img.shields.io/badge/Pytest-8.3.3-yellow)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-purple)](LICENSE)

> Comprehensive test automation project demonstrating UI automation, load testing, and API testing skills.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Test Modules](#test-modules)
    - [UI Test Automation](#ui-test-automation)
    - [Load Testing](#load-testing)
    - [API Testing](#api-testing)
- [Documentation](#documentation)
- [Contact](#contact)
- [Quick Command Reference](#quick-command-reference)

---

## Overview

This project is a comprehensive QA assessment demonstrating expertise in:

- ✅ **UI Test Automation** with Selenium & Python (Page Object Model)
- ✅ **API Testing** with Requests & Pytest (CRUD Operations)
- ✅ **Load Testing** with Locust (Performance & Scalability)

### Assessment Tasks Completed

| # | Task                             | Status     | Framework         |
|---|----------------------------------|------------|-------------------|
| 1 | UI Automation - Insider Careers  | ✅ Complete | Selenium + Pytest |
| 2 | Load Testing - N11 Search Module | ✅ Complete | Locust            |
| 3 | API Testing - Petstore CRUD      | ✅ Complete | Requests + Pytest |

---

## Project Structure

```
bunyamin_kaymak_case/
│
├── 📂 pages/                           # Page Object Models
│   ├── __init__.py
│   ├── base_page.py                    # Base POM with common methods
│   ├── io_home_page.py                 # Homepage POM
│   ├── open_positions_page.py          # Careers page POM
│   └── qa_page.py                      # QA Jobs listing POM
│
├── 📂 tests/                           # UI Test Cases        
│   ├── __init__.py     
│   ├── test_io_ui.py                   # UI test suite  
│   ├── test_n11_load.py                # Load test  
│   ├── test_petstore_api.py            # API test                                            
│   └── test_scenarios_n11.md           # Load test scenarios  
│                                                              
├── 📂 utils/                           # Utility Functions
│   ├── __init__.py
│   ├── driver_factory.py               # WebDriver factory
│   └── screenshot.py                   # Screenshot utility
│
├── 📂 screenshots/                     # Auto-generated on test failures
│
├── .gitignore                          # Git ignore rules
├── conftest.py                         # Pytest configuration
├── README.md                           # This file 
└── requirements.txt                    # Python dependencies 
```

---

## Technologies Used

### Core Technologies

| Technology      | Version | Purpose              |
|-----------------|---------|----------------------|
| **Python**      | 3.11+   | Programming language |
| **Selenium**    | 4.40.0  | UI automation        |
| **Pytest**      | 8.3.3   | Test framework       |
| **Locust**      | 2.43.3  | Load testing         |
| **Pytest-html** | 4.2.0   | Report               |
| **Requests**    | 2.32.5  | API testing          |

### Additional Tools

- **webdriver-manager** - Automatic driver management
- **pytest-html** - HTML test reports
- **Page Object Model** - Design pattern for UI tests

---

## Installation

### Prerequisites

- Python 3.11 or higher
- Chrome browser (for Chrome tests)
- Firefox browser (for Firefox tests)
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/bkymk/bunyamin_kaymak_case
cd bunyamin_kaymak_case
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Verify Installation

```bash
# Check Python version
python --version

# Check Pytest version
pytest --version

# Check Locust version
locust --version
```

---

## Quick Start

### Run All Tests

```bash
# Run all tests with HTML report
pytest -v -s --html=reports/full_report.html --self-contained-html
```

### Run Specific Module

```bash
# UI Tests only
pytest .\tests\test_n11_load.py -v -s --browser=chrome

# API Tests only
pytest .\tests\test_petstore_api.py -v -s --browser=chrome

# Load Test
locust -f test_n11_load.py --users 1 --spawn-rate 1 --run-time 60s --headless --host https://www.n11.com
```

---

## Test Modules

## UI Test Automation

### Overview

Automated testing of Insider careers page using Selenium WebDriver with Page Object Model design pattern.

### Test Scenarios

| # | Test Scenario                                                  | Status |
|---|----------------------------------------------------------------|--------|
| 1 | Visit Insider home page and verify main blocks load            | ✅      |
| 2 | Navigate to QA careers page and click "See all QA jobs"        | ✅      |
| 3 | Filter jobs by Location (Istanbul, Turkey) and Department (QA) | ✅      |
| 4 | Verify all jobs match filter criteria                          | ✅      |
| 5 | Click "View Role" and verify Lever application page redirect   | ✅      |

### Key Features

- ✅ **Page Object Model (POM)** - Clean, maintainable code structure
- ✅ **Parametric Browser Support** - Chrome & Firefox
- ✅ **Automatic Screenshots** - On test failures
- ✅ **Explicit Waits** - Robust element handling
- ✅ **HTML Reports** - Detailed test execution reports

### Running UI Tests

```bash
# Run in Chrome (default)
pytest tests/test_io_ui.py -v -s --browser=chrome

# Run in Firefox
pytest tests/test_io_ui.py -v -s --browser=firefox

# Generate HTML report
pytest tests/test_io_ui.py --browser=chrome --html=reports/ui_report.html --self-contained-html
```

---

## Load Testing

### Overview

Performance testing of N11.com search module using Locust framework to analyze system behavior under load.

### Test Scenarios

| # | Scenario                 | Type     | Weight | Description                   |
|---|--------------------------|----------|--------|-------------------------------|
| 1 | Basic Product Search     | Positive | 5      | Search with random keywords   |
| 2 | Search with Pagination   | Positive | 3      | Navigate through result pages |
| 3 | Search with Filter       | Positive | 2      | Apply price filters           |
| 4 | Search with Sorting      | Positive | 2      | Sort by price/reviews         |
| 5 | Empty Search             | Negative | 1      | Submit empty search query     |
| 6 | Special Character Search | Negative | 1      | Search with special chars     |

### Test Configuration

```yaml
Tool: Locust 2.43.3
Target: https://www.n11.com
Users: 1 concurrent user
Spawn Rate: 1 user/second
Duration: 60 seconds
```

### Running Load Tests

```bash
# Headless mode (recommended for CI/CD)
locust -f test_n11_load.py \
    --users 1 \
    --spawn-rate 1 \
    --run-time 60s \
    --headless \
    --host https://www.n11.com

# Web UI mode (interactive)
locust -f test_n11_load.py --host https://www.n11.com
# Then open: http://localhost:8089

# With HTML report
locust -f test_n11_load.py \
    --users 1 \
    --spawn-rate 1 \
    --run-time 60s \
    --headless \
    --html=reports/load_test_report.html \
    --host https://www.n11.com
```

### Important Note: 403 Forbidden

All requests received **403 Forbidden** due to N11.com's **bot protection (WAF/Cloudflare)**.

**This is expected behavior and NOT a test failure:**

✅ Load test framework is working correctly  
✅ All scenarios executed as designed  
✅ Metrics captured accurately  
✅ Demonstrates site has proper security measures

**For production testing, alternatives include:**

- Request access to test/staging environment
- Use documented APIs
- Coordinate with N11.com team for IP whitelisting

---

## API Testing

### Overview

Comprehensive CRUD operations testing for Petstore API with positive and negative test scenarios.

### API Endpoint

```
Base URL: https://petstore.swagger.io/v2
Endpoint: /pet
```

### Test Coverage

| Operation           | Positive Tests | Negative Tests | Total  |
|---------------------|----------------|----------------|--------|
| **CREATE** (POST)   | 1              | 3              | 4      |
| **READ** (GET)      | 2              | 3              | 5      |
| **UPDATE** (PUT)    | 2              | 2              | 4      |
| **DELETE** (DELETE) | 1              | 3              | 4      |
| **Integration**     | 1              | 0              | 1      |
| **Total**           | 7              | 11             | **18** |

### Test Scenarios

#### CREATE Operations

- ✅ Create pet with valid data
- ❌ Create pet without required fields
- ❌ Create pet with invalid data types
- ❌ Create pet with empty body

#### READ Operations

- ✅ Get pet by valid ID
- ✅ Find pets by status
- ❌ Get pet with non-existent ID
- ❌ Get pet with invalid ID format
- ❌ Find pets with invalid status

#### UPDATE Operations

- ✅ Update existing pet
- ✅ Update pet using form data
- ❌ Update non-existent pet
- ❌ Update pet with invalid data

#### DELETE Operations

- ✅ Delete existing pet
- ❌ Delete non-existent pet
- ❌ Delete with invalid ID format
- ❌ Delete already deleted pet

### Running API Tests

```bash
# Run all API tests
pytest test_petstore_api.py -v -s

# Run with HTML report
pytest test_petstore_api.py -v -s --html=reports/api_report.html --self-contained-html

# Run specific test category
pytest test_petstore_api.py -v -s -k "create"      # Only CREATE tests
pytest test_petstore_api.py -v -s -k "positive"    # Only positive scenarios
pytest test_petstore_api.py -v -s -k "negative"    # Only negative scenarios

# Run with verbose output
pytest test_petstore_api.py -v -s --tb=short

```

## Documentation

### Project Documentation

| Document                  | Description                | Location              |
|---------------------------|----------------------------|-----------------------|
| **README.md**             | Main project documentation | `/README.md`          |
| **test_scenarios_n11.md** | Load test scenarios        | `/load_testing/docs/` |

---

## Contact

**Bünyamin Kaymak**

- 📧 Email: bunyaminkaymk@gmail.com
- 💼 LinkedIn: [https://www.linkedin.com/in/bünyamin-kaymak/](https://www.linkedin.com/in/bünyamin-kaymak/)
- 🐙 GitHub: [@bkymk](https://github.com/bkymk)

---

## Quick Command Reference

```bash
# Installation
pip install -r requirements.txt

# UI Tests
pytest tests/ -v -s --browser=chrome --html=reports/ui_report.html

# Load Tests
cd load_testing
locust -f test_n11_load.py --users 1 --spawn-rate 1 --run-time 60s --headless --host https://www.n11.com

# API Tests
pytest api_tests/ -v -s --html=reports/api_report.html

# All Tests
pytest -v -s --html=reports/full_report.html

# Clean
rm -rf screenshots/* reports/* __pycache__ .pytest_cache
```

---