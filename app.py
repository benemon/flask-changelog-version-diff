from flask import Flask, request, render_template, jsonify
from packaging import version  # Add this import for version comparison
from markupsafe import escape  # Import escape to handle embedded HTML in markdown
import requests
import re
import markdown  # For converting markdown to HTML
import logging
import bleach

app = Flask(__name__)

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compare_versions", methods=["POST"])
def compare_versions():
    data = request.json
    url = data.get("url")
    version1 = data.get("version1")
    version2 = data.get("version2")

    # Check if the URL is a raw GitHub link
    if not url.startswith("https://raw.githubusercontent.com/"):
        return jsonify({
            "detail": "Please provide a raw GitHub link (e.g., https://raw.githubusercontent.com/username/repo/main/CHANGELOG.md)."
        }), 400

    # Fetch the CHANGELOG.md file content
    try:
        response = requests.get(url)
        response.raise_for_status()
        changelog_content = response.text
    except requests.exceptions.RequestException:
        return jsonify({"detail": "Failed to fetch the changelog file."}), 400

    # Flexible pattern to capture all content between the specified versions
    main_pattern = rf"(#{{1,6}}\s*\[?v?{re.escape(version2)}\]?\(?.*?\)?\b[\s\S]*?)(?=(#{{1,6}}\s*\[?v?{re.escape(version1)}\]?\(?.*?\)?\b|\Z))"
    main_match = re.search(main_pattern, changelog_content, re.MULTILINE | re.DOTALL)

    if not main_match:
        return jsonify({"detail": "Specified versions not found in changelog."}), 404

    # Get all captured content between version2 and version1
    captured_content = main_match.group(0)

    # Split captured content by headers to separate each version section
    section_pattern = r"(#{1,6}\s*\[?v?\d+\.\d+\.\d+[-\w.]*\]?\(?.*?\)?\b)"
    sections = re.split(section_pattern, captured_content)

    # Initialize list to store section details
    collapsible_sections = []

    # Convert specified versions to `version.Version` objects for comparison
    version1_normalized = re.sub(r"-(\w+)\.(\d+)", r"\1\2", version1)
    version2_normalized = re.sub(r"-(\w+)\.(\d+)", r"\1\2", version2)
    min_version = version.parse(version1_normalized)
    max_version = version.parse(version2_normalized)

    # Define allowed tags and attributes
    allowed_tags = [
        "p", "a", "ul", "ol", "li", "strong", "em", "code", "pre", "blockquote",
        "h1", "h2", "h3", "h4", "h5", "h6", "table", "thead", "tbody", "tr", "th", "td"
    ]
    allowed_attributes = {"a": ["href", "title"], "img": ["src", "alt", "title"]}

    # Process sections into collapsible elements
    for i in range(1, len(sections), 2):
        raw_header = sections[i]
        content = sections[i + 1] if (i + 1) < len(sections) else ""
        
        version_match = re.search(r"\d+\.\d+\.\d+[-\w.]*", raw_header)
        if not version_match:
            continue

        display_version = version_match.group(0)
        normalized_version = re.sub(r"-(\w+)\.(\d+)", r"\1\2", display_version)
        
        try:
            section_version = version.parse(normalized_version)
        except version.InvalidVersion:
            continue

        if section_version < min_version or section_version > max_version:
            continue

        # Convert markdown to HTML and sanitize embedded HTML
        content_html = markdown.markdown(content, extras=["extra"])
        content_html = bleach.clean(content_html, tags=allowed_tags, attributes=allowed_attributes)

        # Append the section data to collapsible_sections
        collapsible_sections.append({
            "version": section_version,
            "header": display_version,
            "content_html": content_html
        })

    # Sort sections by version in descending order
    collapsible_sections.sort(key=lambda x: x["version"], reverse=True)

    # Generate HTML content for each sorted section
    collapsible_content = ""
    for section in collapsible_sections:
        collapsible_content += f"""
            <div class="collapsible">
                <button class="collapsible-btn">{section['header']}</button>
                <div class="collapsible-content">
                    {section['content_html']}
                </div>
            </div>
        """

    # Return the formatted collapsible content and release count as JSON
    return jsonify({
        "changes": collapsible_content,
        "release_count": len(collapsible_sections),
        "changelog_url": url
    })

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=8181)
