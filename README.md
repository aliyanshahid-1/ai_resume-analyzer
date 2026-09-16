# AI Resume Analyzer

A modular Streamlit application that compares a PDF/DOCX resume with a job description using the Groq API and returns structured resume-job analysis.

## Features

- PDF and DOCX resume text extraction
- Job description input
- AI-based resume and job analysis
- Overall match score
- Skills score, experience score, education score, and keyword score
- Matching skills
- Missing skills
- ATS keyword status
- Resume problems
- Actionable recommendations
- Final result summary
- Structured JSON from the AI layer
- Modular architecture with separation of concerns

## Project Structure

```text
app.py                 # Streamlit UI and application flow
analyzer.py            # Groq API integration and JSON validation
resume_parser.py       # PDF/DOCX text extraction
prompts.py             # AI prompt and JSON schema
requirements.txt       # Python dependencies
.env.example           # Environment variable template
.gitignore             # Git ignore rules
README.md              # Documentation
```

## Requirements

- Python 3.10 or newer
- A Groq API key
- Internet access for the Groq API

## Setup

### 1. Create the project directory

Put all project files in the same directory.

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Copy `.env.example` to `.env`.

Windows CMD:

```bash
copy .env.example .env
```

PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Then open `.env` and set:

```text
GROQ_API_KEY=your_real_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

Do not commit `.env` to Git.

## Run

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## How It Works

```text
Resume PDF/DOCX + Job Description
              |
              v
       resume_parser.py
              |
              v
          resume text
              |
              +------------------+
              |                  |
              v                  v
         analyzer.py <------ prompts.py
              |
              v
      Structured JSON result
              |
              v
           app.py
              |
              v
       Results Dashboard
```

## Architecture

### `app.py`
Responsible only for the Streamlit interface, user input, displaying results, and coordinating the application flow.

### `resume_parser.py`
Responsible only for reading PDF/DOCX files and extracting text.

### `prompts.py`
Responsible only for constructing the AI prompt and defining the expected JSON structure.

### `analyzer.py`
Responsible for communicating with Groq, requesting JSON output, parsing it, and validating the response.

This separation keeps UI, file parsing, AI logic, and prompt design independent.

## Structured Output

The AI returns an object containing:

- `overall_score`
- `score_breakdown`
- `matching_skills`
- `missing_skills`
- `ats_keywords`
- `problems`
- `recommendations`
- `final_result`
- `resume_summary`
- `job_summary`

## Notes and Limitations

- Scanned/image-only PDFs may not contain machine-readable text. OCR can be added later if needed.
- AI analysis can contain mistakes, so users should verify the result.
- The match score is a job-specific heuristic, not a real ATS score from a particular employer.
- Recommendations should be followed only when they accurately reflect the candidate's real skills and experience.

## Security

Never expose the Groq API key in frontend code, GitHub, screenshots, or public repositories. Keep it in `.env` locally and use Streamlit secrets or environment variables when deploying.

## License

Add the license appropriate for your project before public distribution.
