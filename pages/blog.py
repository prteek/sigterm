"""Blog page with links to Regression Room posts"""

def render(st):
    """Render the blog page

    Args:
        st: Streamlit module
    """
    st.markdown("### 📝 Blog Posts")
    st.markdown("Statistical analysis and regression modeling")
    st.divider()

    blog_posts = [
        {
            "title": "rentership ~ occupation, analysis",
            "url": "https://prteek.github.io/regression_room/posts/occupation_impact_on_rentals/index.html",
            "description": "Analyzing the impact of occupation on rental housing using random effects and hierarchical models",
            "tags": ["random effects", "hierarchical models", "glm", "binomial"]
        },
        {
            "title": "MPG ~ manufacturer, analysis",
            "url": "https://prteek.github.io/regression_room/posts/miles_per_gallon/index.html",
            "description": "Examining how manufacturer affects miles per gallon using random effects and hierarchical modeling",
            "tags": ["random effects", "hierarchical models"]
        },
        {
            "title": "gambling spend ~ gender, analysis",
            "url": "https://prteek.github.io/regression_room/posts/teen_gamble/index.html",
            "description": "Statistical analysis of teenage gambling spending patterns across gender using regression and ANOVA",
            "tags": ["regression", "ANOVA"]
        },
        {
            "title": "Likelihood",
            "url": "https://prteek.github.io/regression_room/posts/likelihood_primer/index.html",
            "description": "A primer on likelihood theory, Fisher information, and Newton-Raphson optimization methods",
            "tags": ["likelihood", "fisher information", "newton raphson"]
        },
        {
            "title": "Probabilistic model of User journey",
            "url": "https://prteek.github.io/regression_room/posts/user_behaviour_analysis/index.html",
            "description": "Modeling user behavior and journey prediction using Markov chains and time series analysis",
            "tags": ["markov chain", "timeseries"]
        },
        {
            "title": "Movie runtime ~ year, analysis",
            "url": "https://prteek.github.io/regression_room/posts/movies_getting_longer/index.html",
            "description": "Investigating whether movies are getting longer over time using hypothesis testing and bootstrap methods",
            "tags": ["hypothesis testing", "bootstrap", "regression"]
        }
    ]

    for post in blog_posts:
        st.markdown(f"**[{post['title']}]({post['url']})**")
        st.caption(post['description'])

        tag_str = " · ".join([f"`{tag}`" for tag in post['tags']])
        st.markdown(tag_str)
        st.divider()
