# CAMT GUI - Developer & Maintenance Guide

This document is for developers, maintainers, and the team responsible for managing the CAMT Text Generator application. It covers the system architecture, the bi-monthly data update procedure, and the automated build pipeline.

---

## 1. System Architecture Overview

The application is a standalone desktop graphical user interface (GUI) built with Python's built-in `tkinter` library. 

* **Core Logic:** It processes copied text containing publication records, cleans the venue titles, capitalizes article titles using natural language processing via the `spacy` library, and compares citation counts against established baselines.
* **Data Sources:** The baselines are stored locally in two files: `citation_averages.json` and `citation_percentiles.json`.
* **Clipboard Handling:** The app constructs raw HTML strings and uses the `ctypes` library to interact directly with the Windows API to copy formatted text (bolding, italics, underlines) to the user's clipboard.
* **Distribution:** The application is packaged into standalone executables (`.exe` for Windows, `.app`/`.zip` for Mac) using PyInstaller.

---

## 2. Bi-Monthly Data Updates (Critical Maintenance)

The citation baselines used by this application are tied to the Clarivate Essential Science Indicators (ESI) tables. Because Clarivate updates these tables every two months, **this application's JSON data must be updated 6 times a year.**

### How to Update the Data:
1. Export the latest ESI tables for both averages and percentiles.
2. Open `citation_averages.json` and `citation_percentiles.json` in a code editor.
3. Replace the old data with the newly exported data, ensuring the exact JSON structure remains intact:
   * **Averages Structure:** `{"RESEARCH FIELD": {"YEAR": AVERAGE_VALUE}}`
   * **Percentiles Structure:** `{"RESEARCH FIELD": {"PERCENTILE": {"YEAR": THRESHOLD_VALUE}}}`
4. Commit and push the updated `.json` files to the `main` branch on GitHub. 

*(Note: You do not need to manually build the app after pushing the data. The automated pipeline handles it.)*

---

## 3. The Automated Build Pipeline (GitHub Actions)

This project uses a Continuous Integration/Continuous Deployment (CI/CD) pipeline via GitHub Actions.

Whenever a change is pushed to the `main` branch (such as the bi-monthly JSON updates), GitHub automatically spins up a Windows server and a Mac server in the cloud. It installs Python, downloads the required dependencies, runs PyInstaller, and outputs the finished, ready-to-use application files.

### Finding the Built Applications:
1. Go to the **Actions** tab in the GitHub repository.
2. Click the latest successful run of the "Build CAMT Apps" workflow.
3. Scroll to the **Artifacts** section at the bottom to download the new `.exe` and `.zip` files to distribute to the team.

---
