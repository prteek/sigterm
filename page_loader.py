"""Utility module for loading dynamic pages from the pages directory"""

import os
import importlib.util
import sys


def load_page(page_name):
    """Load page content from pages directory
    Returns: (content_type, content) where content_type is 'text' or 'streamlit'
    """
    pages_dir = os.path.join(os.path.dirname(__file__), "pages")

    # Try .py file first (Streamlit pages)
    py_path = os.path.join(pages_dir, f"{page_name}.py")
    if os.path.exists(py_path):
        try:
            spec = importlib.util.spec_from_file_location(f"page_{page_name}", py_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"page_{page_name}"] = module
            spec.loader.exec_module(module)
            if hasattr(module, "render"):
                return ("streamlit", module.render)
        except Exception as e:
            return ("text", f"Error loading page: {str(e)}")

    # Try .txt file (text pages)
    txt_path = os.path.join(pages_dir, f"{page_name}.txt")
    if os.path.exists(txt_path):
        with open(txt_path, "r") as f:
            return ("text", f.read())

    return None
