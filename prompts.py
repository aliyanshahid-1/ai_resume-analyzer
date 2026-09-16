import json


def build_analysis_prompt(resume_text: str, job_description: str) -> str:
    schema = {
        "overall_score": 0,
        "score_breakdown": {
            "skills": 0,
            "experience": 0,
            "education": 0,
            "keywords": 0
        },
        "matching_skills": [],
        "missing_skills": [],
        "ats_keywords": [
            {"keyword": "example", "status": "found"}
        ],
        "problems": [],
        "recommendations": [],
        "final_result": "",
        "resume_summary": {
            "skills": [],
            "experience": "",
            "education": "",
            "certifications": [],
            "projects": []
        },
        "job_summary": {
            "required_skills": [],
            "preferred_skills": [],
            "experience_requirement": "",
            "education_requirement": [],
            "important_keywords": []
        }
    }

    return f"""
Analyze the candidate resume against the supplied job description.

IMPORTANT RULES:
1. Use only evidence present in the resume. Never invent skills, experience,
   education, certifications, projects, or achievements.
2. Distinguish between required and preferred job requirements.
3. A skill is "matching" when the resume provides credible evidence of it.
4. A skill is "missing" when an important job requirement is not supported by
   the resume. Do not call a skill missing if the resume clearly expresses an
   equivalent concept.
5. ATS keywords should be important job-specific terms, not every word in the
   job description. Status must be "found" or "missing".
6. The overall score must be 0-100. Use your analysis of skills, experience,
   education, and keywords. Do not make the score a random guess.
7. Recommendations must be truthful and actionable. Never tell the candidate
   to claim a skill or experience they do not have.
8. Problems should focus on the resume's relevance, clarity, evidence,
   keyword coverage, and presentation for this specific job.
9. Return ONLY valid JSON matching this structure. Do not add markdown.

TARGET JSON STRUCTURE:
{json.dumps(schema, indent=2)}

RESUME:
---BEGIN RESUME---
{resume_text}
---END RESUME---

JOB DESCRIPTION:
---BEGIN JOB DESCRIPTION---
{job_description}
---END JOB DESCRIPTION---
""".strip()
