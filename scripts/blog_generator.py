import os
import markdown
import yaml
import subprocess
from datetime import datetime
from pathlib import Path
from jinja2 import Template

def get_changed_posts():
    """Get list of markdown files that have been modified in the posts directory."""
    try:
        # Get modified and untracked files
        modified = subprocess.check_output(['git', 'ls-files', '-m', 'posts/'], text=True).splitlines()
        untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', 'posts/'], text=True).splitlines()

        # Combine and filter for markdown files
        changed_files = set(modified + untracked)
        return [f for f in changed_files if f.endswith('.md')]
    except subprocess.CalledProcessError:
        print("Warning: Git command failed. Processing all markdown files.")
        # Fallback: return all markdown files
        return [str(p) for p in Path('posts').glob('*.md')]

def read_markdown_file(file_path):
    """Read a markdown file and extract frontmatter and content."""
    with open(file_path, 'r') as f:
        content = f.read()

    # Split frontmatter and markdown content
    _, frontmatter, markdown_content = content.split('---', 2)
    metadata = yaml.safe_load(frontmatter)

    # Convert date format if needed
    if 'date' in metadata:
        try:
            # Try to parse various date formats
            date_obj = datetime.strptime(metadata['date'], '%B %d %Y')
            metadata['date'] = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            # If date is already in YYYY-MM-DD format, leave it as is
            pass

    return metadata, markdown_content.strip()

def convert_markdown_to_html(markdown_content):
    """Convert markdown content to HTML."""
    md = markdown.Markdown(extensions=['meta', 'fenced_code', 'codehilite', 'tables', 'attr_list', 'md_in_html'])
    return md.convert(markdown_content)

def generate_blog_post_html(metadata, html_content, prev_post=None, next_post=None):
    """Generate HTML for a single blog post."""
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-GYJRB0KS1S"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag() { dataLayer.push(arguments); }
            gtag('js', new Date());
            gtag('config', 'G-GYJRB0KS1S');
        </script>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ metadata.title }} - Atul Dhingra</title>
        <link rel="stylesheet" href="/css/style.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <!-- Add syntax highlighting CSS if needed -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="/index.html">Home</a></li>
                    <li><a href="/about.html">About Me</a></li>
                    <li><a href="/experience.html">Experience</a></li>
                    <li><a href="/publications.html">Publications</a></li>
                    <li><a href="/patents.html">Patents</a></li>
                    <li><a href="/blog.html">Blog</a></li>
                    <li><a href="/contact.html">Contact</a></li>
                </ul>
            </nav>
        </header>

        <article class="blog-post-full">
            <div class="post-header">
                <h1>{{ metadata.title }}</h1>
                <div class="post-meta">
                    <span class="date">{{ metadata.date }}</span>
                    <span class="authors">By {{ ', '.join(metadata.authors) }}</span>
                    <div class="tags">
                        {% for tag in metadata.tags %}
                        <span class="tag">{{ tag }}</span>
                        {% endfor %}
                    </div>
                </div>
            </div>
            <div class="post-content">
                {{ html_content }}
            </div>
            
            <div class="post-navigation">
                {% if prev_post %}
                <a href="/{{ prev_post.url }}" class="nav-button prev">
                    <i class="fas fa-arrow-left"></i>
                    <span>Previous<br>{{ prev_post.title }}</span>
                </a>
                {% endif %}
                
                {% if next_post %}
                <a href="/{{ next_post.url }}" class="nav-button next">
                    <span>Next<br>{{ next_post.title }}</span>
                    <i class="fas fa-arrow-right"></i>
                </a>
                {% endif %}
            </div>
        </article>

        <footer>
            <p>&copy; 2024 Atul Dhingra's Portfolio. All rights reserved.</p>
        </footer>

        <!-- Add syntax highlighting JS if needed -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
        <script>hljs.highlightAll();</script>
    </body>
    </html>
    """
    return Template(template).render(
        metadata=metadata, 
        html_content=html_content,
        prev_post=prev_post,
        next_post=next_post
    )

def get_all_posts_metadata():
    """Get metadata for all existing posts."""
    posts_metadata = []
    for md_file in Path('posts').glob('*.md'):
        metadata, _ = read_markdown_file(md_file)
        metadata['url'] = f'blog/{md_file.stem}.html'
        posts_metadata.append(metadata)
    return posts_metadata

def update_blog_listing(posts_metadata):
    """Update the main blog listing page."""
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-GYJRB0KS1S"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag() { dataLayer.push(arguments); }
            gtag('js', new Date());
            gtag('config', 'G-GYJRB0KS1S');
        </script>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Blog - Atul Dhingra</title>
        <link rel="stylesheet" href="css/style.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="about.html">About Me</a></li>
                    <li><a href="experience.html">Experience</a></li>
                    <li><a href="publications.html">Publications</a></li>
                    <li><a href="patents.html">Patents</a></li>
                    <li><a href="blog.html">Blog</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </nav>
        </header>

        <section id="blog">
            <div class="container">
                <h1>Blog</h1>
                <div class="blog-grid">
                    {% for post in posts %}
                    <article class="blog-post">
                        <div class="post-image">
                            <img src="{{ post.image }}" alt="{{ post.title }}">
                        </div>
                        <div class="post-content">
                            <h2>{{ post.title }}</h2>
                            <div class="post-meta">
                                <span class="date">{{ post.date }}</span>
                                <span class="category">{{ post.tags[0] }}</span>
                            </div>
                            <p>{{ post.excerpt }}</p>
                            <a href="{{ post.url }}" class="read-more">Read More</a>
                        </div>
                    </article>
                    {% endfor %}
                </div>
            </div>
        </section>

        <footer>
            <p>&copy; 2024 Atul Dhingra's Portfolio. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """
    return Template(template).render(posts=posts_metadata)

def get_series_order(metadata):
    """Get the order for series posts."""
    title = metadata.get('title', '').lower()
    try:
        # Extract part number if it exists
        if 'part' in title:
            part = int(''.join(filter(str.isdigit, title.split('part')[-1])))
            return part
        return float('inf')  # Non-series posts go last
    except (ValueError, IndexError):
        return float('inf')

def main():
    # Create necessary directories
    blog_posts_dir = Path('blog')
    blog_posts_dir.mkdir(exist_ok=True)

    # Get changed posts
    changed_posts = get_changed_posts()
    if not changed_posts:
        print("No changes detected in posts directory.")
        return

    print(f"Processing {len(changed_posts)} changed posts:")
    for post in changed_posts:
        print(f"- {post}")

    # Get all posts metadata and sort them
    all_posts_metadata = get_all_posts_metadata()
    all_posts_metadata.sort(key=lambda x: (
        datetime.strptime(x['date'], '%Y-%m-%d').strftime('%Y-%m'),
        get_series_order(x)
    ))

    # Process changed markdown files
    for md_file in changed_posts:
        # Read and process the markdown file
        metadata, markdown_content = read_markdown_file(md_file)
        html_content = convert_markdown_to_html(markdown_content)

        # Find current post index in sorted list
        current_index = next(i for i, post in enumerate(all_posts_metadata) 
                           if post['url'] == f'blog/{Path(md_file).stem}.html')
        
        # Get previous and next posts
        prev_post = all_posts_metadata[current_index - 1] if current_index > 0 else None
        next_post = all_posts_metadata[current_index + 1] if current_index < len(all_posts_metadata) - 1 else None

        # Generate the blog post HTML file
        post_filename = Path(md_file).stem + '.html'
        post_path = blog_posts_dir / post_filename

        # Write the blog post HTML
        with open(post_path, 'w') as f:
            f.write(generate_blog_post_html(metadata, html_content, prev_post, next_post))
        print(f"Generated {post_path}")

    # Update the main blog listing
    with open('blog.html', 'w') as f:
        f.write(update_blog_listing(all_posts_metadata))
    print("Updated blog listing page")

if __name__ == '__main__':
    main()