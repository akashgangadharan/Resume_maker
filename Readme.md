# Resume Builder Pro

A professional resume builder web application built with Flask that allows users to create, customize, and download their resume in PDF format. Features include drag-and-drop section reordering, real-time preview, and professional formatting.

## Features

- Interactive form-based resume creation
- Drag and drop section reordering
- Real-time resume preview
- Professional PDF output
- Customizable sections:
  - Personal Information
  - Professional Summary
  - Professional Experience
  - Leadership Experience
  - Skills
  - Education
  - Achievements
  - Projects

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository

bash
git clone https://github.com/yourusername/resume-builder-pro.git
cd resume-builder-pro


2. Create a virtual environment (recommended)

bash
python -m venv venv


3. Activate the virtual environment
- On Windows:

bash
venv\Scripts\activate

- On macOS/Linux:
bash
source venv/bin/activate


4. Install required packages
bash
pip install flask
pip install reportlab
pip install werkzeug


## Required Fonts

The application uses Calibri font family for PDF generation. You need to place the following font files in the `static/fonts` directory:
- calibri.ttf (Regular)
- calibrib.ttf (Bold)
- calibrii.ttf (Italic)

Note: Due to licensing restrictions, you need to obtain these fonts legally through Microsoft Windows or other legitimate sources.

## Project Structure

resume-builder-pro/
├── main.py
├── static/
│ ├── css/
│ │ └── style.css
│ └── fonts/
│ ├── calibri.ttf
│ ├── calibrib.ttf
│ └── calibrii.ttf
└── templates/
├── base.html
├── download_resume.html
├── resume_form.html
└── sections/
├── personal_info.html
├── summary.html
├── experience.html
├── leadership.html
├── skills.html
├── education.html
├── achievements.html
└── projects.html


## Running the Application

1. Make sure your virtual environment is activated

2. Start the Flask application:
bash
python main.py

3. Open your web browser and navigate to:
http://localhost:5000


## Usage Instructions

1. Fill in Personal Information
   - Name, email, phone, location
   - Optional: LinkedIn and portfolio URLs

2. Add Professional Summary
   - Click "Add Summary Point" for multiple points
   - First point cannot be removed
   - Additional points can be removed using the × button

3. Add Professional Experience
   - Company name, position, location
   - Start and end dates
   - Skills used (appears in italics)
   - Multiple responsibilities (can add/remove)
   - Maximum 3 experiences allowed

4. Add Leadership Experience
   - Title and description
   - Can add multiple entries

5. Add Skills
   - BI Tools & Databases
   - Programming Languages
   - Cloud Platforms
   - Certifications

6. Add Education
   - School/University name
   - Degree/Certificate
   - Location
   - Start and end dates

7. Add Projects
   - Project title
   - Project description
   - Maximum 3 projects allowed

8. Reorder Sections
   - Drag and drop sections to reorder them
   - Changes reflect in both preview and PDF

9. Generate Resume
   - Click "Generate Resume" to see preview
   - Click "Download PDF" to download the final version

## Customization

You can customize the styling by modifying:
- `static/css/style.css` for the form interface
- `templates/download_resume.html` for the preview styling
- PDF styling in `main.py`

## Troubleshooting

Common issues and solutions:

1. **Missing Fonts Error**
   - Ensure all required Calibri font files are in the `static/fonts` directory
   - Verify font file names match exactly: calibri.ttf, calibrib.ttf, calibrii.ttf

2. **Module Not Found Errors**
   - Ensure Flask is installed: `pip install flask`
   - Ensure ReportLab is installed: `pip install reportlab`
   - Verify virtual environment is activated

3. **PDF Generation Issues**
   - Check write permissions in the directory
   - Verify all form fields are properly filled

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository.