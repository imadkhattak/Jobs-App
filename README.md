# AI Job Application Assistant

This project is an AI-powered job application assistant that helps users find and apply for jobs. It scrapes job postings from various platforms, allows users to upload their CV, and uses a large language model (LLM) to match the user's profile with suitable job openings.

## Project Structure

```
AI Job App/
├── .gitignore
├── GEMINI.md
├── README.md
├── requirements.txt
├── user_agents.txt
├── Back_End/
│   ├── data/
│   │   ├── cvs/
│   │   ├── retrieved_data/
│   │   └── saved_jobs/
│   ├── Scrappers/
│   │   ├── glassdoor.py
│   │   ├── indeed.py
│   │   └── Linkedin.py
│   └── src/
│       ├── __init__.py
│       ├── cv_parser.py
│       ├── jobs_cleaner.py
│       ├── llm.py
│       └── Main.py
├── Front_End/
│   ├── app/
│   │   ├── __init__.py
│   │   └── app.py
│   ├── static/
│   │   ├── script.js
│   │   └── styles.css
│   └── templates/
│       ├── index.html
│       ├── job_details.html
│       └── saved_jobs.html
├── uploads/
└── venv/
```

### Root Directory

- **`.gitignore`**: Specifies which files and directories to ignore in Git.
- **`GEMINI.md`**: Potentially contains information or prompts for the Gemini LLM.
- **`README.md`**: This file.
- **`requirements.txt`**: A list of Python packages required to run the project.
- **`user_agents.txt`**: A list of user agents used by the web scrapers.

### `Back_End/`

This directory contains the core logic of the application.

- **`data/`**: Stores all the data used in the application.
    - **`cvs/`**: Stores user-uploaded CVs.
    - **`retrieved_data/`**: Stores the raw job data scraped from different platforms (e.g., `glassdoor.json`, `indeed.json`, `linkedin_jobs.json`).
    - **`saved_jobs/`**: Stores jobs that the user has saved.
- **`Scrappers/`**: Contains the Python scripts for scraping job data from different websites.
    - **`glassdoor.py`**: Scraper for Glassdoor.
    - **`indeed.py`**: Scraper for Indeed.
    - **`Linkedin.py`**: Scraper for LinkedIn.
- **`src/`**: Contains the source code for the back-end.
    - **`cv_parser.py`**: Parses and extracts information from user-uploaded CVs.
    - **`jobs_cleaner.py`**: Cleans and preprocesses the scraped job data.
    - **`llm.py`**: Interacts with the Large Language Model (e.g., Gemini) for job matching and other AI-powered features.
    - **`Main.py`**: The main entry point for the back-end application.

### `Front_End/`

This directory contains the user interface of the application, built with Flask.

- **`app/`**: The main Flask application.
    - **`app.py`**: The main Flask application file that defines the routes and views.
- **`static/`**: Contains static files like CSS and JavaScript.
    - **`script.js`**: JavaScript code for the front-end.
    - **`styles.css`**: CSS styles for the front-end.
- **`templates/`**: Contains the HTML templates for the web pages.
    - **`index.html`**: The main page of the application.
    - **`job_details.html`**: The page for displaying the details of a specific job.
    - **`saved_jobs.html`**: The page for displaying saved jobs.

### `uploads/`

This directory is used to temporarily store user-uploaded files, such as CVs.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.x
- pip

### Installation

1. Clone the repo:
   ```sh
   git clone https://github.com/your_username/AI-Job-App.git
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up your environment variables by creating a `.env` file in the root directory and adding the necessary API keys and configurations.

### Running the Application

1. **Run the Back-End:**
   ```sh
   python Back_End/src/Main.py
   ```
2. **Run the Front-End:**
   ```sh
   python Front_End/app/app.py
   ```
3. Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

1. **Upload your CV:** Go to the home page and upload your CV in PDF format.
2. **Scrape for Jobs:** The application will scrape job postings from LinkedIn, Indeed, and Glassdoor.
3. **View Job Matches:** The application will use an LLM to match your CV with the scraped job postings and display the most relevant jobs.
4. **Save Jobs:** You can save the jobs that you are interested in.
5. **View Saved Jobs:** You can view your saved jobs on the "Saved Jobs" page.
