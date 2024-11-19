from flask import Flask, render_template, request, send_file, redirect, url_for, session
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Replace with a secure secret key

@app.route('/', methods=['GET'])
def index():
    return render_template('resume_form.html', resume_data=session.get('resume_data'))

@app.route('/section/<section_name>')
def get_section(section_name):
    resume_data = session.get('resume_data', {})
    return render_template(f'sections/{section_name}.html', resume_data=resume_data)

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    # Get section order
    section_order = request.form.get('section_order')
    if section_order:
        section_order = json.loads(section_order)
    else:
        section_order = ['summary', 'experience', 'leadership', 'skills', 'education', 'achievements', 'projects']
    
    # Store section order in session
    session['section_order'] = section_order
    
    # Add debug logging
    print("Form Data:", request.form)
    print("Summary Data:", request.form.getlist('summary[]'))
    
    # Clear any existing resume data from session
    session.pop('resume_data', None)
    
    # Get personal information
    personal_info = {
        'name': request.form.get('name', ''),
        'email': request.form.get('email', ''),
        'phone': request.form.get('phone', ''),
        'location': request.form.get('location', ''),
        'linkedin': request.form.get('linkedin', ''),
        'portfolio': request.form.get('portfolio', '')
    }

    # Get summary points - Updated to ensure proper capture
    summary = []
    summary_points = request.form.getlist('summary[]')
    print("Raw summary points:", summary_points)  # Debug print
    for point in summary_points:
        if point.strip():
            summary.append(point.strip())
    print("Processed summary:", summary)  # Debug print

    # Get professional experience
    experience = []
    for i in range(10):  # Increased from 5 to 10 to allow more experiences
        company = request.form.get(f'company_{i}')
        position = request.form.get(f'position_{i}')
        if company and position:  # Only add if both company and position exist
            exp = {
                'company': company,
                'position': position,
                'location': request.form.get(f'location_{i}', ''),
                'start_date': format_date(request.form.get(f'exp_start_{i}', '')),
                'end_date': format_date(request.form.get(f'exp_end_{i}', '')),
                'skills': request.form.get(f'skills_{i}', ''),
                'responsibilities': [r.strip() for r in request.form.getlist(f'responsibilities_{i}[]') if r.strip()]
            }
            print(f"Experience {i}:", exp)  # Debug log
            experience.append(exp)
    
    print("Final experience list:", experience)  # Debug log

    # Get skills (single entry)
    skills = {
        'bi_tools': request.form.get('bi_tools', ''),
        'programming': request.form.get('programming', ''),
        'cloud': request.form.get('cloud', ''),
        'certifications': request.form.get('certifications', '')
    }

    # Get education
    education = []
    for i in range(3):  # Maximum 3 education entries
        school = request.form.get(f'school_{i}')
        degree = request.form.get(f'degree_{i}')
        if school and degree:  # Only add if both school and degree exist
            edu = {
                'school': school,
                'degree': degree,
                'edu_location': request.form.get(f'edu_location_{i}', ''),
                'edu_start': format_education_date(request.form.get(f'edu_start_{i}', '')),
                'edu_end': format_education_date(request.form.get(f'edu_end_{i}', ''))
            }
            education.append(edu)

    # Get achievements
    achievements = []
    for i in range(5):  # Maximum 5 achievements
        achievement = request.form.get(f'achievements_{i}')
        if achievement and achievement.strip():
            achievements.append(achievement.strip())

    # Get leadership experience
    leadership = []
    for i in range(3):  # Assuming maximum 3 leadership entries
        title = request.form.get(f'leadership_title_{i}')
        description = request.form.get(f'leadership_description_{i}')
        if title and description:
            leadership_entry = {
                'title': title,
                'description': description
            }
            leadership.append(leadership_entry)

    # Get projects
    projects = []
    for i in range(3):  # Assuming maximum 3 projects
        title = request.form.get(f'project_title_{i}')
        description = request.form.getlist(f'project_description_{i}[]')
        if title and any(description):
            project = {
                'title': title,
                'description': [d.strip() for d in description if d.strip()]
            }
            projects.append(project)

    # Store all data in session
    resume_data = {
        'personal_info': personal_info,
        'summary': summary,
        'experience': experience,
        'leadership': leadership,
        'skills': skills,
        'education': education,
        'achievements': achievements,
        'projects': projects
    }
    
    print("Final resume_data:", resume_data)  # Debug print
    session['resume_data'] = resume_data
    
    # Pass both resume_data and section_order to the template
    return render_template('download_resume.html', 
                         resume_data=resume_data,
                         section_order=section_order)

@app.route('/download_resume')
def download_resume():
    if 'resume_data' not in session:
        return redirect(url_for('index'))
    
    # Get section order from session with summary included in default
    section_order = session.get('section_order', ['summary', 'experience', 'leadership', 'skills', 'education', 'achievements', 'projects'])
    
    # First show the preview page
    if request.args.get('format') != 'pdf':
        return render_template('download_resume.html', 
                             resume_data=session['resume_data'],
                             section_order=section_order)
    
    # Generate PDF if format=pdf is specified
    data = session['resume_data']
    buffer = io.BytesIO()
    
    # Register Calibri fonts
    pdfmetrics.registerFont(TTFont('Calibri', 'static/fonts/calibri.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri-Bold', 'static/fonts/calibrib.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri-Italic', 'static/fonts/calibrii.ttf'))
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.3*inch,
        leftMargin=0.3*inch,
        topMargin=0.1*inch,
        bottomMargin=0.1*inch
    )
    
    styles = getSampleStyleSheet()
    
    # Style definitions with consistent formatting
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Normal'],
        fontName='Calibri-Bold',
        fontSize=16,
        leading=20,
        alignment=1,  # Center alignment
        spaceAfter=5,
        textTransform='uppercase'
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontName='Calibri',
        fontSize=11,
        leading=14,
        alignment=1,  # Center alignment
        spaceAfter=0
    )
    
    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Calibri-Bold',
        fontSize=12,
        leading=14,
        leftIndent=0,
        firstLineIndent=0,
        spaceBefore=0,
        spaceAfter=2,
        textTransform='uppercase'
    )
    
    exp_header_style = ParagraphStyle(
        'ExperienceHeader',
        parent=styles['Normal'],
        fontName='Calibri-Bold',
        fontSize=11,
        leading=14,
        leftIndent=0,
        spaceBefore=0,
        spaceAfter=2
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontName='Calibri',
        fontSize=11,
        leading=14,
        leftIndent=0,
        firstLineIndent=0,
        spaceBefore=0,
        spaceAfter=2,
        alignment=4  # 4 is for justified text
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Calibri',
        fontSize=11,
        leading=14,
        leftIndent=12,
        firstLineIndent=-12,
        spaceBefore=0,
        spaceAfter=2,
        alignment=4  # 4 is for justified text
    )

    # Create a new style for skills descriptions
    skills_description_style = ParagraphStyle(
        'SkillsDescription',
        parent=normal_style,
        alignment=4  # 4 is for justified text
    )

    # Add section spacing - reduced from 20 to 2 points
    section_spacing = Spacer(1, 2)  # Changed from 20 to 2
    
    # Build the PDF content
    story = []
    
    # Header Section with proper spacing
    story.append(Paragraph(data['personal_info']['name'].upper(), name_style))
    
    # Create contact parts list
    contact_parts = [
        data['personal_info']['location'],
        f"<link href='mailto:{data['personal_info']['email']}'>{data['personal_info']['email']}</link>",
        data['personal_info']['phone']
    ]
    if data['personal_info'].get('linkedin'):
        contact_parts.append(f"<link href='{data['personal_info']['linkedin']}'>LinkedIn</link>")
    if data['personal_info'].get('portfolio'):
        contact_parts.append(f"<link href='{data['personal_info']['portfolio']}'>Portfolio</link>")
    
    story.append(Paragraph(" • ".join(contact_parts), contact_style))
    story.append(Spacer(1, 1.5))  # Set to exactly 1.5 points between contact info and first section
    
    # Add sections according to order
    for section in section_order:
        if section == 'summary' and data.get('summary'):
            story.append(Paragraph('PROFESSIONAL SUMMARY', section_header))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
            story.append(Spacer(1, 6))
            
            for point in data['summary']:
                if point.strip():
                    story.append(Paragraph(f"\u2022 {point}", bullet_style))
            story.append(Spacer(1, 8))
        
        elif section == 'experience' and data.get('experience'):
            story.append(Paragraph('PROFESSIONAL EXPERIENCE', section_header))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
            story.append(Spacer(1, 6))
            
            for exp in data['experience']:
                # Create a table for the header to align position/company and date
                header_data = [[
                    Paragraph(f"{exp['position']} | {exp['company']} | {exp['location']}", exp_header_style),
                    Paragraph(f"{exp['start_date']} - {exp['end_date']}", ParagraphStyle(
                        'DateStyle',
                        parent=exp_header_style,
                        alignment=2,  # Right alignment
                        spaceBefore=0,
                        spaceAfter=0
                    ))
                ]]
                
                header_table = Table(
                    header_data,
                    colWidths=[doc.width * 0.70, doc.width * 0.30],  # Changed from 0.75/0.25 to 0.70/0.30
                    style=[
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                        ('ALIGN', (-1, 0), (-1, 0), 'RIGHT'),
                    ]
                )
                story.append(header_table)
                
                if exp.get('skills'):
                    story.append(Spacer(1, 2))
                    story.append(Paragraph(f'<i>Skills: {exp["skills"]}</i>', normal_style))
                
                story.append(Spacer(1, 4))
                for resp in exp['responsibilities']:
                    if resp.strip():
                        story.append(Paragraph(f"\u2022 {resp}", bullet_style))
                story.append(Spacer(1, 8))
        
        elif section == 'skills' and data.get('skills'):
            story.append(Paragraph('SKILLS', section_header))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
            story.append(Spacer(1, 6))
            
            if data['skills'].get('bi_tools'):
                story.append(Paragraph(f"<font face='Calibri-Bold'>Business Intelligence and Visualization Tools:</font> {data['skills']['bi_tools']}", skills_description_style))
            if data['skills'].get('programming'):
                story.append(Paragraph(f"<font face='Calibri-Bold'>Programming & ETL Tools:</font> {data['skills']['programming']}", skills_description_style))
            if data['skills'].get('cloud'):
                story.append(Paragraph(f"<font face='Calibri-Bold'>Cloud Platform:</font> {data['skills']['cloud']}", skills_description_style))
            if data['skills'].get('certifications'):
                story.append(Paragraph(f"<font face='Calibri-Bold'>Certifications:</font> {data['skills']['certifications']}", skills_description_style))
            story.append(Spacer(1, 8))
            
        elif section == 'education' and data.get('education'):
            story.append(Paragraph('EDUCATION', section_header))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
            story.append(Spacer(1, 6))
            
            for edu in data['education']:
                # Create a table for the header to align school and date
                header_data = [[
                    Paragraph(f"{edu['school']} | {edu['edu_location']}", exp_header_style),
                    Paragraph(f"{edu['edu_start']} - {edu['edu_end']}", ParagraphStyle(
                        'DateStyle',
                        parent=exp_header_style,
                        alignment=2  # Right alignment
                    ))
                ]]
                header_table = Table(
                    header_data, 
                    colWidths=[doc.width * 0.65, doc.width * 0.35],
                    style=[
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                        ('ALIGN', (-1, -1), (-1, -1), 'RIGHT'),
                    ]
                )
                story.append(header_table)
                story.append(Spacer(1, 2))  # Add small space before degree
                story.append(Paragraph(edu['degree'], normal_style))
                story.append(Spacer(1, 6))  # Space between education entries
            
            story.append(section_spacing)
        
        elif section == 'achievements' and data.get('achievements'):
            # Add achievements section
            story.append(Paragraph('ACHIEVEMENTS', section_header))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
            story.append(Spacer(1, 2))
            for achievement in data['achievements']:
                story.append(Paragraph(f"\u2022 {achievement}", bullet_style))
            story.append(section_spacing)
            
        elif section == 'projects' and data.get('projects'):
            # Add projects section
            story.append(Paragraph('PROJECTS', section_header))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
            story.append(Spacer(1, 2))
            for project in data['projects']:
                story.append(Paragraph(project['title'], exp_header_style))
                for desc in project['description']:
                    story.append(Paragraph(f"\u2022 {desc}", bullet_style))
            story.append(section_spacing)
        
        elif section == 'leadership' and data.get('leadership'):
            story.append(Paragraph('LEADERSHIP EXPERIENCE', section_header))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
            story.append(Spacer(1, 6))
            
            for lead in data['leadership']:
                # Add title directly like in projects section
                story.append(Paragraph(lead['title'], ParagraphStyle(
                    'LeadershipTitle',
                    parent=exp_header_style,
                    leftIndent=0,  # Ensure no indentation
                    firstLineIndent=0  # Ensure no first line indent
                )))
                # Add description with bullet point
                story.append(Paragraph(f"\u2022 {lead['description']}", bullet_style))
                story.append(Spacer(1, 6))
            
            story.append(section_spacing)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    current_date = datetime.now().strftime("%Y%m%d")
    return send_file(
        buffer,
        download_name=f'resume_{current_date}.pdf',
        mimetype='application/pdf'
    )

@app.route('/edit_resume')
def edit_resume():
    if 'resume_data' not in session:
        return redirect(url_for('index'))
    
    data = session['resume_data']
    return render_template('index.html', resume_data=data)

def format_education_date(date_string):
    if not date_string:
        return ''
    try:
        # Parse the date string from the month input (YYYY-MM format)
        date = datetime.strptime(date_string, '%Y-%m')
        return date.strftime('%B %Y')  # Format as "Month YYYY"
    except (ValueError, TypeError):
        return date_string

def format_date(date_string):
    if not date_string:
        return ''
    try:
        date = datetime.strptime(date_string, '%Y-%m')
        return date.strftime('%B %Y')
    except:
        return date_string

if __name__ == '__main__':
    app.run(debug=True)
