import streamlit as st
from resume_parser import extract_resume_text, SUPPORTED_TYPES
from analyzer import analyze_resume

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("AI Resume Analyzer")
st.caption("Compare a resume with a job description using structured AI analysis.")

with st.sidebar:
    st.header("About")
    st.write(
        "Upload a PDF or DOCX resume, paste a job description, and get a "
        "job-specific match score, skills, ATS keywords, problems, and recommendations."
    )

resume_file = st.file_uploader("Upload your resume", type=SUPPORTED_TYPES)
job_description = st.text_area(
    "Paste the job description",
    height=280,
    placeholder="Paste the complete job description here..."
)

if st.button("Analyze Resume", type="primary", use_container_width=True):
    if resume_file is None:
        st.error("Please upload a PDF or DOCX resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()

    with st.spinner("Reading and analyzing your resume..."):
        try:
            resume_text = extract_resume_text(resume_file)
            if len(resume_text.strip()) < 50:
                st.error("Could not extract enough text from the resume.")
                st.stop()

            result = analyze_resume(resume_text, job_description)
        except Exception as exc:
            st.error(f"Analysis failed: {exc}")
            st.stop()

    score = result["overall_score"]
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Match", f'{score}/100')
    c2.metric("Skills", f'{result["score_breakdown"]["skills"]}/100')
    c3.metric("Experience", f'{result["score_breakdown"]["experience"]}/100')
    c4.metric("Keywords", f'{result["score_breakdown"]["keywords"]}/100')

    st.subheader("Final Result")
    st.write(result["final_result"])

    left, right = st.columns(2)

    with left:
        st.subheader("Matching Skills")
        for item in result["matching_skills"]:
            st.success(item)

        st.subheader("ATS Keywords")
        for item in result["ats_keywords"]:
            status = item["status"].lower()
            if status == "found":
                st.write(f"✅ **{item['keyword']}** — Found")
            else:
                st.write(f"❌ **{item['keyword']}** — Missing")

    with right:
        st.subheader("Missing Skills")
        if result["missing_skills"]:
            for item in result["missing_skills"]:
                st.warning(item)
        else:
            st.success("No important missing skills identified.")

        st.subheader("Resume Problems")
        for item in result["problems"]:
            st.write(f"• {item}")

    st.subheader("Recommendations")
    for item in result["recommendations"]:
        st.info(item)

    with st.expander("Detailed extracted information"):
        a, b = st.columns(2)
        with a:
            st.markdown("**Resume**")
            st.json(result["resume_summary"])
        with b:
            st.markdown("**Job**")
            st.json(result["job_summary"])

    with st.expander("View extracted resume text"):
        st.text(resume_text)
