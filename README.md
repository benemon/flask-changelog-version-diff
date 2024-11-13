
# Changelog Diff Viewer

The **Changelog Diff Viewer** is a Flask web application that allows users to view differences between two versions in a `CHANGELOG.md` file hosted on GitHub. The app retrieves the changelog file, captures sections between the specified versions, and displays them as collapsible sections in a user-friendly format.

## Features

- Fetches `CHANGELOG.md` from a specified GitHub URL.
- Supports version headers with or without markdown links.
- Displays each version section as a collapsible block for easy navigation.
- Simple, clean UI with a calm color palette for a modern look.

## Requirements

- Python 3.8 or later
- Internet connection (to retrieve changelog content from GitHub)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/changelog-diff-viewer.git
cd changelog-diff-viewer
```

### Step 2: Set up a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

The application requires the following Python packages:
- `Flask` - for handling HTTP requests and serving the web application.
- `requests` - for fetching the `CHANGELOG.md` content from GitHub.
- `markdown2` - for converting markdown content to HTML.

## Configuration

The application has no configuration requirements beyond dependencies. Ensure the Python packages in `requirements.txt` are installed.

## Running the Application

### Step 1: Start the Flask Development Server

With the virtual environment activated (if you are using one), run the following command:

```bash
python app.py
```

This command will start the Flask development server on `http://127.0.0.1:5000`.

### Step 2: Access the Application

Open a web browser and navigate to:

```
http://127.0.0.1:5000
```

## Usage

1. **Provide the `CHANGELOG.md` URL**: Enter the raw GitHub URL of the `CHANGELOG.md` file you wish to analyze.
   - **Example**: `https://raw.githubusercontent.com/username/repo/main/CHANGELOG.md`
2. **Enter Old and New Versions**: Specify the two versions you want to compare. Ensure the version format matches what’s used in the `CHANGELOG.md` file.
3. **Submit the Form**: Click "Get Differences" to retrieve the changelog content between the specified versions.
4. **View Collapsible Sections**: Each version section will appear as a collapsible block, displaying content changes in an organized, user-friendly way.

### Example

To view changes between version `3.5.7` and `3.5.12` of a changelog, enter:
- URL: `https://raw.githubusercontent.com/username/repo/main/CHANGELOG.md`
- Old Version: `3.5.7`
- New Version: `3.5.12`

Click **Get Differences** to display the differences between these versions.

## Troubleshooting

- **Versions Not Found**: Ensure the version format entered matches what’s in the changelog. For example, if versions are encapsulated in brackets (`[v1.0.0]`), enter `v1.0.0` in the form.
- **Fetching Errors**: Ensure the GitHub URL provided is a valid raw URL (e.g., `https://raw.githubusercontent.com/...`) and the file is accessible.

## Deployment

For production deployment, consider using a WSGI server like **gunicorn** and a reverse proxy (such as **nginx** or **Apache**).

### Example Gunicorn Command

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

This command runs the application with 4 workers, binding to all interfaces on port 5000.

## File Structure

```plaintext
changelog-diff-viewer/
├── app.py                # Main Flask application file
├── requirements.txt      # Dependencies file
├── templates/
│   └── index.html        # HTML template for the application
└── static/
    ├── main.js           # JavaScript for handling UI interactions
    └── styles.css        # CSS styles for UI design
```

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss the changes.