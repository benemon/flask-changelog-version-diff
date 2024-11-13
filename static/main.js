document.getElementById('changelogForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const url = document.getElementById('url').value;
    const version1 = document.getElementById('version1').value;
    const version2 = document.getElementById('version2').value;

    const response = await fetch('/compare_versions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, version1, version2 })
    });

    const resultContainer = document.getElementById('result');
    if (response.ok) {
        const data = await response.json();
        resultContainer.innerHTML = data.changes;

        // Apply collapsible behavior with icon rotation
        document.querySelectorAll(".collapsible-btn").forEach(button => {
            button.addEventListener("click", function() {
                this.classList.toggle("active");  // Toggle active state for rotation
                const content = this.nextElementSibling;
                
                // Toggle display and max-height
                if (content.style.display === "block") {
                    content.style.display = "none";
                    content.style.maxHeight = null;
                } else {
                    content.style.display = "block";
                    content.style.maxHeight = content.scrollHeight + "px";
                }
            });
        });
    } else {
        const error = await response.json();
        resultContainer.innerHTML = `Error: ${error.detail}`;
    }
});