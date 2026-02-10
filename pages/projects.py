"""Example Streamlit page for projects"""

def render(st):
    """Render the projects page

    Args:
        st: Streamlit module
    """
    st.markdown("### 📁 Projects")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Terminal App**")
        st.caption("A retro terminal interface built with Streamlit")
        st.markdown("- Dark green theme")
        st.markdown("- Command processing")
        st.markdown("- Dynamic page rendering")

    with col2:
        st.markdown("**Data Analysis Tools**")
        st.caption("Analytics and visualization projects")
        st.markdown("- ML pipelines")
        st.markdown("- Data pipelines")
        st.markdown("- Interactive dashboards")

    st.divider()
    st.markdown("Visit my GitHub for more projects →")
