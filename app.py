from flask import Flask, request, render_template, jsonify
import requests
import re
import markdown2  # For converting markdown to HTML
import logging

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

    # Capture content between the new and old versions inclusively
    main_pattern = rf"(##\s*\[?v?{re.escape(version2)}\]?\(?.*?\)?\b[\s\S]*?)(?=(##\s*\[?v?{re.escape(version1)}\]?\(?.*?\)?\b|\Z))"
    main_match = re.search(main_pattern, changelog_content, re.MULTILINE | re.DOTALL)

    if not main_match:
        return jsonify({"detail": "Specified versions not found in changelog."}), 404

    # Get all captured content between version2 and version1
    captured_content = main_match.group(0)

    # Split captured content by headers to separate each version section
    section_pattern = r"(##\s*\[?v?\d+\.\d+\.\d+\]?\(?.*?\)?\b)"
    sections = re.split(section_pattern, captured_content)

    # Initialize collapsible content and count the releases
    collapsible_content = ""
    release_count = 0

    # Process sections into collapsible elements, skipping any empty initial split
    for i in range(1, len(sections), 2):
        raw_header = sections[i]
        content = sections[i + 1] if (i + 1) < len(sections) else ""
        
        # Extract just the version number from the header
        version_match = re.search(r"\d+\.\d+\.\d+", raw_header)
        header = version_match.group(0) if version_match else raw_header.strip()

        content_html = markdown2.markdown(content)

        # Add collapsible HTML for each version section
        collapsible_content += f"""
            <div class="collapsible">
                <button class="collapsible-btn">{header}</button>
                <div class="collapsible-content">
                    {content_html}
                </div>
            </div>
        """
        
        # Increment the release count
        release_count += 1

    # Return the formatted collapsible content and release count as JSON
    return jsonify({
        "changes": collapsible_content,
        "release_count": release_count
    })


if __name__ == "__main__":
     app.run(host="0.0.0.0", port=8181)
