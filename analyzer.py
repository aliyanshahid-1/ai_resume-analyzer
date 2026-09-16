import json
import os
from typing import Any, Dict

from groq import Groq

from prompts import build_analysis_prompt

MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


class AnalysisError(Exception):
    """Raised when AI analysis cannot be completed or validated."""


def _get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise AnalysisError(
            "GROQ_API_KEY is not configured. Add it to your .env file or environment."
        )
    return Groq(api_key=api_key)


def _extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end <= start:
            raise AnalysisError("The AI returned invalid JSON.") from exc
        try:
            data = json.loads(text[start:end + 1])
        except json.JSONDecodeError as nested_exc:
            raise AnalysisError("The AI returned invalid JSON.") from nested_exc

    if not isinstance(data, dict):
        raise AnalysisError("The AI response must be a JSON object.")
    return data


def _validate_result(data: Dict[str, Any]) -> Dict[str, Any]:
    required = [
        "overall_score",
        "score_breakdown",
        "matching_skills",
        "missing_skills",
        "ats_keywords",
        "problems",
        "recommendations",
        "final_result",
        "resume_summary",
        "job_summary",
    ]
    missing = [key for key in required if key not in data]
    if missing:
        raise AnalysisError(f"AI response is missing fields: {', '.join(missing)}")

    score = int(data["overall_score"])
    if not 0 <= score <= 100:
        raise AnalysisError("Overall score must be between 0 and 100.")

    breakdown = data["score_breakdown"]
    for key in ("skills", "experience", "education", "keywords"):
        breakdown[key] = max(0, min(100, int(breakdown[key])))

    data["overall_score"] = score

    if not isinstance(data["matching_skills"], list):
        raise AnalysisError("matching_skills must be a list.")
    if not isinstance(data["missing_skills"], list):
        raise AnalysisError("missing_skills must be a list.")
    if not isinstance(data["ats_keywords"], list):
        raise AnalysisError("ats_keywords must be a list.")
    if not isinstance(data["problems"], list):
        raise AnalysisError("problems must be a list.")
    if not isinstance(data["recommendations"], list):
        raise AnalysisError("recommendations must be a list.")
    return data


def analyze_resume(resume_text: str, job_description: str) -> Dict[str, Any]:
    """Send the resume and job description to Groq and return validated JSON."""
    client = _get_client()
    prompt = build_analysis_prompt(resume_text, job_description)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise resume analysis engine. "
                        "Follow the requested JSON schema exactly. "
                        "Never invent candidate experience or skills."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
    except Exception as exc:
        raise AnalysisError(f"Groq API request failed: {exc}") from exc

    content = response.choices[0].message.content or ""
    return _validate_result(_extract_json(content))
