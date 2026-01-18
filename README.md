# Starter API Automation Repo

This repository is a lightweight, interview-friendly API automation framework built with Python and pytest. It validates REST API endpoints and automatically generates a styled HTML test report that displays test execution results and captured API response evidence.

This project is designed to be approachable even for someone new to API testing. The recommended workflow is:
1) Use Postman first to understand REST requests and responses manually (GET/POST/etc.)
2) Then run the automated pytest suite to validate the same behavior consistently and repeatedly
3) Review evidence + results in the generated HTML report

The demo API used for testing is:
https://jsonplaceholder.typicode.com

Postman is included in the workflow because it helps you visually learn and verify:
- what an endpoint returns (response body)
- how status codes behave (200 vs 404 vs 400)
- how headers and payloads affect the response
- the difference between REST methods (GET, POST, PUT/PATCH, DELETE)
Once you understand the requests in Postman, the pytest automation becomes much easier to read and explain because it mirrors the same steps in code.

To run the project, first create and activate a virtual environment:

python -m venv .venv  
source .venv/bin/activate   (Mac/Linux)  
.venv\Scripts\activate      (Windows)

Then install dependencies:

pip install -r requirements.txt

Run the test suite and generate the report using:

python run_tests.py

Running this command will:
- execute all pytest tests
- write API response evidence to evidence.json
- generate a styled HTML report
- save the report to the reports folder
- optionally open the report in your browser (if enabled)

If the browser does not open automatically, you can open the report manually using:

open starter_api_automation_repo/reports/report.html

The automation validates:
- GET requests with valid and invalid IDs
- POST requests to create new resources
- basic negative and edge cases
- response status codes and payload structure

Each test logs evidence using a shared utility function. Evidence includes:
- timestamp
- test name
- HTTP method
- URL
- response status
- full response payload

Evidence is written to:
starter_api_automation_repo/reports/evidence.json

After pytest completes, the run_tests.py script reads the evidence file and injects the data into an HTML report. The report UI is fully static and uses no JavaScript frameworks or external dependencies.

Project structure:

starter_api_automation_repo  
├── run_tests.py  
├── requirements.txt  
├── README.md  
├── starter_api_automation_repo  
│   ├── config  
│   │   └── config.json  
│   ├── tests  
│   │   ├── conftest.py  
│   │   ├── test_get_post.py  
│   │   ├── test_create_post.py  
│   │   └── test_negative_cases.py  
│   ├── utils  
│   │   ├── helpers.py  
│   │   └── evidence.py  
│   └── reports  
│       ├── evidence.json  
│       ├── report.html  
│       └── report.css  
└── .venv

The config.json file contains base URLs, endpoints, headers, and test data so tests remain clean and readable. The utils folder contains reusable logic for loading configuration, formatting URLs, and writing API evidence. The reports folder acts as the front-end layer and contains the generated report files.

Next steps: Postman setup (manual REST testing)

The goal of this step is to manually practice the same requests the automation runs, so you understand what the tests are proving.

1) Install Postman
Download and install Postman from the official Postman site.

2) Create a new Collection
In Postman:
- Click Collections
- Click New Collection
- Name it: Starter API Automation

3) Create an Environment (optional but recommended)
- Create a new Environment named: Local Demo
- Add variables:
  base_url = https://jsonplaceholder.typicode.com
This lets you reuse {{base_url}} across requests.

4) Add these requests to the collection

Request A: GET a post (valid)
- Method: GET
- URL: {{base_url}}/posts/1
- Send
What to check:
- Status should be 200
- Response should include id, title, body, userId

Request B: GET a post (invalid)
- Method: GET
- URL: {{base_url}}/posts/999999
- Send
What to check:
- Some real APIs return 404
- JSONPlaceholder often returns 200 with an empty object
This is why our automated test allows multiple expected behaviors depending on the API.

Request C: POST create a post
- Method: POST
- URL: {{base_url}}/posts
- Headers:
  Content-Type: application/json
- Body (raw JSON):
  {
    "title": "postman demo title",
    "body": "postman demo body",
    "userId": 1
  }
- Send
What to check:
- Status is usually 201 (or 200 depending on API)
- Response should echo back what you sent and include an id

5) Export your Postman collection (recommended)
Once the requests are created and working:
- Click the collection
- Export
- Save the JSON export into the repo (example: postman/Starter_API_Automation.postman_collection.json)
This proves you can validate the API manually and also automate it.

How Postman connects to the automation

Postman is the manual learning and debugging tool.
Pytest automation is the repeatable regression tool.

They should match conceptually:
- Postman request URL should match what config.json + format_url builds
- Postman request body should match cfg["test_data"] payloads
- Postman response fields should match what pytest asserts
- The HTML report should match what you saw in Postman (status + response payload)

If you want next improvements:
- add pass/fail icons to the HTML UI
- add collapsible JSON responses
- add a Postman collection folder + exported file into the repo
- add a script that generates a Postman collection automatically from config.json
