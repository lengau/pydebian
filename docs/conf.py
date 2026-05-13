project = "pydebian"
author = "pydebian contributors"

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx_design",
]

exclude_patterns = ["_build"]

html_theme = "furo"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
