# Playwright Agent Testing Guide

This guide provides instructions on how to test the Phase 2 Playwright Agent Orchestrator.

## 1. Start the Environment

Make sure your PostgreSQL database is running via Docker:
```bash
docker compose up -d
```

Start the FastAPI application:
```bash
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

*Note: The first time you trigger Playwright, it might take a few seconds to launch the Chromium browser. The browser will launch in headful mode (you will see it open) to help with debugging and resolving CAPTCHAs if LeetCode presents them.*

## 2. Sample API Calls

You can use PowerShell `Invoke-RestMethod` or `curl` to test the API endpoints.

### A. Check Streak Status

**Request:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/agent/streak-status" -Method Get | ConvertTo-Json
```

**Example Output:**
```json
{
  "solved_today": false,
  "daily_problem": null,
  "recommended_problem": {
    "title": "Two Sum",
    "url": "https://leetcode.com/problems/two-sum",
    "difficulty": "Easy",
    "reason": "Popular Interview Question"
  }
}
```

### B. Run Daily Agent Workflow

This will launch Playwright, click on the daily challenge, extract the problem statement, and save it to the database.

**Request:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/agent/run" -Method Post | ConvertTo-Json
```

**Example Output:**
```json
{
  "status": "success",
  "problem_title": "Count the Number of Good Nodes",
  "difficulty": "Medium",
  "daily_challenge": true
}
```

### C. Scrape Specific Problem

**Request:**
```powershell
$body = @{ url="https://leetcode.com/problems/roman-to-integer/" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/agent/scrape" -Method Post -Body $body -ContentType "application/json" | ConvertTo-Json
```

**Example Output:**
```json
{
  "status": "success",
  "problem_title": "Roman to Integer",
  "difficulty": "Easy",
  "daily_challenge": false
}
```

## 3. Logs

You will see structured logs in your terminal during execution:
```text
2023-10-25 10:15:00 [INFO] app.agents.orchestrator: Starting Agent Orchestrator Workflow
2023-10-25 10:15:02 [INFO] app.playwright_agent.browser: Starting browser (headless=False)
2023-10-25 10:15:05 [INFO] app.playwright_agent.actions: Navigating to https://leetcode.com/problemset/
...
```
