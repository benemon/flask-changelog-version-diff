document.getElementById('changelogForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const url = document.getElementById('url').value;
    const version1 = document.getElementById('version1').value;
    const version2 = document.getElementById('version2').value;

    const resultContainer = document.getElementById('result');
    const releaseCountContainer = document.getElementById('releaseCount');
    const errorMessageContainer = document.getElementById('errorMessage');

    try {
        const response = await fetch('/compare_versions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, version1, version2 })
        });

        if (response.ok) {
            const data = await response.json();
            resultContainer.innerHTML = data.changes;

            // Display the release count
            releaseCountContainer.textContent = `Number of Releases: ${data.release_count}`;

            // Clear any previous error message
            errorMessageContainer.style.display = 'none';
            errorMessageContainer.innerHTML = '';

            // Apply collapsible behavior
            document.querySelectorAll(".collapsible-btn").forEach(button => {
                button.addEventListener("click", function() {
                    this.classList.toggle("active");
                    const content = this.nextElementSibling;

                    if (content.style.maxHeight) {
                        // Collapse the content
                        content.style.maxHeight = null;
                    } else {
                        // Expand the content with a short delay to improve smoothness
                        content.style.maxHeight = "0px";
                        setTimeout(() => {
                            content.style.maxHeight = content.scrollHeight + "px";
                        }, 10);  // Small delay to ensure smooth height calculation
                    }
                });
            });
        } else {
            const error = await response.json();
            errorMessageContainer.style.display = 'block';
            errorMessageContainer.innerHTML = `Error: ${error.detail}`;
            resultContainer.innerHTML = '';
            releaseCountContainer.textContent = '';
        }
    } catch (err) {
        errorMessageContainer.style.display = 'block';
        errorMessageContainer.innerHTML = `Unexpected error: ${err.message}`;
        resultContainer.innerHTML = '';
        releaseCountContainer.textContent = '';
    }
});
