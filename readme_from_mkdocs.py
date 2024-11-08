import logging
import re
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def generate_readme_content() -> str:
    en_index = Path("docs/index.md")
    if not en_index.exists():
        logging.warning(f"{en_index} doesn't exist")
        return ""
        # raise a warning and exit without doing anything
    content = en_index.read_text("utf-8")
    match_pre = re.search(r"</style>\n\n", content)
    if not match_pre:
        raise RuntimeError("Couldn't find pre section (<style>) in index.md")
    frontmatter_end = match_pre.end()
    new_content = content[frontmatter_end:]
    # Remove content between <!-- only-mkdocs --> and <!-- /only-mkdocs -->
    new_content = re.sub(
        r"<!--only-mkdocs-->.*?<!--/only-mkdocs-->",
        "",
        new_content,
        flags=re.DOTALL,
    )
    return new_content


def generate_readme() -> None:
    """
    Generate README.md content from main index.md
    """
    readme_path = Path("README.md")
    if not readme_path.exists():
        readme_path.write_text("", encoding="utf-8")
    new_content = generate_readme_content()
    readme_content = readme_path.read_text("utf-8")
    if new_content == readme_content:
        return
    readme_path.write_text(new_content, encoding="utf-8")



if __name__ == "__main__":
    generate_readme()
