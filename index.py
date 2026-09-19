import datetime
from pathlib import Path
import re
import sys
import unicodedata

INDEX_FILENAME = 'INDEX.md'

EXCLUDE_DIRS = {
    '.git',
    '.venv',
    'media',
    '.gitignore',
    '__pycache__',
    'exercises'
}

EXCLUDE_FILES = {
    INDEX_FILENAME
}

def github_slug(text: str, used_slugs: set[str]) -> str:
    """Generate a GitHub-style Markdown heading anchor."""
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text, flags=re.UNICODE)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')

    if not text:
        text = 'section'

    original = text
    counter = 1

    while text in used_slugs:
        text = f'{original}-{counter}'
        counter += 1

    used_slugs.add(text)

    return text


def remove_front_matter(lines: list[str]) -> list[str] | str:
    """Remove YAML front matter from the beginning of a Markdown file."""
    if not lines:
        return lines

    if lines[0].strip() != '---':
        return lines

    for i in range(1, len(lines)):
        if lines[i].strip() in ('---', '...'):
            return lines[i + 1]

    return lines


def extract_headings(path: Path) -> list[tuple[int, str, str]]:
    """Extract headings from a Markdown file."""
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        print(f'Could not decode {path}')
        return []

    lines = text.splitlines()
    lines = remove_front_matter(lines)

    headings = []
    used_slugs = set()

    in_fenced_code_block = False
    fence = None

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('```') or stripped.startswith('~~~'):
            current_fence = stripped[:3]

            if not in_fenced_code_block:
                in_fenced_code_block = True
                fence = current_fence
            elif current_fence == fence:
                in_fenced_code_block = False
                fence = None

            continue

        if in_fenced_code_block:
            continue

        match = re.match(r'^(#{1,6})\s+(.+?)\s*#*\s*$', line)

        if not match:
            continue

        level = len(match.group(1))
        title = match.group(2).strip()

        if not title:
            continue

        anchor = github_slug(title, used_slugs)
        headings.append((level, title, anchor))

    return headings


def get_file_title(path: Path, headings: list[tuple[int, str, str]]) -> str:
    """Determine the display title for a Markdown file."""
    for level, title, _ in headings:
        if level == 1:
            return title

    return path.stem.replace('_', '').replace('-', '').strip().title()


def find_markdown_files(root: Path) -> list[Path]:
    """Recursively find Markdown files."""
    files = []

    for path in root.rglob('*.md'):
        relative_parts = path.relative_to(root).parts

        if any(part in EXCLUDE_DIRS for part in relative_parts):
            continue

        if path.name in EXCLUDE_FILES:
            continue

        files.append(path)

    return sorted(files, key=lambda p: str(p.relative_to(root)).lower())


def build_heading_tree(headings: list[tuple[int, str, str]]) -> list[dict]:
    """Convert a flat heading list into a nested tree."""
    root = []
    stack = []

    for level, title, anchor in headings:
        node = {
            'level': level,
            'title': title,
            'anchor': anchor,
            'children': [],
        }

        while stack and stack[-1]['level'] >= level:
            stack.pop()

        if stack:
            stack[-1]['children'].append(node)
        else:
            root.append(node)

        stack.append(node)

    return root


def render_heading_tree(nodes: list[dict], relative_path: str, depth: int = 1) -> list[str]:
    """Render the heading tree as Markdown bullets."""
    lines = []

    for node in nodes:
        link = f'{relative_path}#{node['anchor']}'
        indent = '  ' * depth

        lines.append(f'{indent}- [{node['title']}]({link})')
        lines.extend(render_heading_tree(node['children'], relative_path, depth + 1))

    return lines


def generate_index(root: Path) -> str:
    """Generate the complete INDEX.md content."""
    files = find_markdown_files(root)
    lines = [
        f'*Generated: {datetime.datetime.now().date()}*'
        '',
        '# Index',
        '',
    ]

    for path in files:
        relative_path = path.relative_to(root).as_posix()
        headings = extract_headings(path)
        title = get_file_title(path, headings)
        lines.append(f'- [{title}]({relative_path})')

        if headings:
            tree = build_heading_tree(headings)
            lines.extend(render_heading_tree(tree, relative_path, depth=1))
            lines.append('')

    return '\n'.join(lines)


def main():
    """Main function."""
    if len(sys.argv) > 1:
        root = Path(sys.argv[1]).resolve()
        print(f'Root: {root}')
    else:
        root = Path.cwd().resolve()
        print(f'Root: {root}')

    if not root.is_dir():
        print(f'Not a directory: {root}')
        sys.exit(1)

    index_path = root / INDEX_FILENAME
    content = generate_index(root)
    index_path.write_text(content, encoding='utf-8')
    file_count = len(find_markdown_files(root))

    print(f'Generated {index_path} from {file_count} Markdown files.')


if __name__ == '__main__':
    main()
