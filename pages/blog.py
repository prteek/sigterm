"""Dynamic blog page that fetches posts from Regression Room"""

import requests
from bs4 import BeautifulSoup
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_blog_posts():
    """Fetch blog posts from Regression Room website

    Returns:
        list: List of blog post dictionaries with title, url, description, tags
    """
    try:
        url = "https://prteek.github.io/regression_room/index.html"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all post containers (quarto-post elements)
        posts = []
        post_containers = soup.find_all('div', class_='quarto-post')

        for container in post_containers:
            # Extract title and link from h3 > a
            title_elem = container.find('h3', class_='listing-title')
            if not title_elem:
                continue

            link_elem = title_elem.find('a')
            if not link_elem:
                continue

            title = link_elem.get_text(strip=True)
            url = link_elem.get('href', '#')

            # Make relative URLs absolute
            if url.startswith('./'):
                url = "https://prteek.github.io/regression_room/" + url[2:]
            elif url.startswith('/'):
                url = "https://prteek.github.io" + url

            # Extract categories/tags
            categories_elem = container.find('div', class_='listing-categories')
            tags = []
            if categories_elem:
                tag_elems = categories_elem.find_all('div', class_='listing-category')
                tags = [tag.get_text(strip=True) for tag in tag_elems]

            posts.append({
                'title': title,
                'url': url,
                'tags': tags
            })

        return posts if posts else None

    except Exception as e:
        return None


def render(st):
    """Render the dynamic blog page

    Args:
        st: Streamlit module
    """
    st.markdown("### 📝 Blog Posts")
    st.markdown("Statistical analysis and regression modeling from [Regression Room](https://prteek.github.io/regression_room/)")
    st.divider()

    with st.spinner("Loading blog posts..."):
        posts = fetch_blog_posts()

    if posts:
        for post in posts:
            st.markdown(f"**[{post['title']}]({post['url']})**")

            if post['tags']:
                tag_str = " · ".join([f"`{tag}`" for tag in post['tags']])
                st.markdown(tag_str)

            st.divider()
    else:
        st.warning("Could not fetch blog posts. Please try again later.")
