import streamlit as st

from src.recomender import (
    recommend_faculty,
    recommend_papers,
    find_skill_gap
)

st.set_page_config(
    page_title="Research Opportunity Discovery Platform",
    layout="wide"
)

st.title("🔬 Research Opportunity Discovery Platform")

st.markdown(
    "Find professors, research papers, and identify skill gaps for your research journey."
)

query = st.text_input(
    "Enter your research interests"
)

student_skills = st.text_input(
    "Enter your current skills (comma separated)"
)

if query:

    st.success(f"Searching for: {query}")

    # =========================
    # FACULTY RECOMMENDATIONS
    # =========================

    faculty_results = recommend_faculty(query)

    st.subheader("🎓 Recommended Faculty")

    if not faculty_results.empty:

        for _, row in faculty_results.iterrows():

            with st.container():

                st.markdown(f"### {row['Name']}")

                if "Match_Score" in faculty_results.columns:
                    st.success(
                        f"Match Score: {row['Match_Score']}%"
                    )

                st.write(
                    f"**University:** {row['University']}"
                )

                st.write(
                    f"**Research Area:** {row['Research_Areas']}"
                )

                st.write(
                    f"**Skills:** {row['Skills']}"
                )

                st.markdown(
                    f"🔗 [Faculty Profile]({row['Profile_URL']})"
                )

                st.divider()

    else:
        st.info("No faculty recommendations found.")

    # =========================
    # PAPER RECOMMENDATIONS
    # =========================

    paper_results = recommend_papers(query)

    st.subheader("📄 Recommended Papers")

    if not paper_results.empty:

        for _, row in paper_results.iterrows():

            st.markdown(
                f"**{row['Title']}**"
            )

            if "Match_Score" in paper_results.columns:
                st.caption(
                    f"Match Score: {row['Match_Score']}%"
                )

    else:
        st.info("No paper recommendations found.")

    # =========================
    # SKILL GAP ANALYSIS
    # =========================

    if student_skills:

        st.subheader("🛠 Your Current Skills")

        st.write(student_skills)

        top_faculty = faculty_results.iloc[0]

        faculty_skills = top_faculty["Skills"]

        missing_skills = find_skill_gap(
            student_skills,
            faculty_skills
        )

        st.subheader("📈 Skill Gap Analysis")

        st.write(
            f"**Recommended Faculty:** {top_faculty['Name']}"
        )

        st.write(
            f"**Faculty Skills:** {faculty_skills}"
        )

        st.write("### Missing Skills")

        if len(missing_skills) == 0:

            st.success(
                "You already have all the required skills!"
            )

        else:

            for skill in missing_skills:
                st.warning(skill)

            st.subheader("🗺️ Suggested Learning Roadmap")

            for i, skill in enumerate(
                missing_skills,
                start=1
            ):
                st.write(
                    f"{i}. Learn {skill}"
                )