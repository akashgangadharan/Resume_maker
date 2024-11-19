console.log('Script loaded!');

let educationCount = 1;

function addEducation() {
    if (educationCount < 3) {
        const container = document.getElementById('education-container');
        const newEducation = `
            <div class="education-entry card">
                <div class="card-content">
                    <div class="row">
                        <div class="col-11">
                            <div class="grid">
                                <div class="form-group">
                                    <input type="text" class="form-control" 
                                           name="school_${educationCount}" 
                                           placeholder="University/School Name">
                                </div>
                                <div class="form-group">
                                    <input type="text" class="form-control" 
                                           name="degree_${educationCount}" 
                                           placeholder="Degree/Certificate">
                                </div>
                            </div>
                            <div class="grid">
                                <div class="form-group">
                                    <input type="text" class="form-control" 
                                           name="edu_location_${educationCount}" 
                                           placeholder="Location">
                                </div>
                                <div class="form-group">
                                    <input type="month" class="form-control" 
                                           name="edu_start_${educationCount}" 
                                           placeholder="Start Date">
                                </div>
                                <div class="form-group">
                                    <input type="month" class="form-control" 
                                           name="edu_end_${educationCount}" 
                                           placeholder="End Date">
                                </div>
                            </div>
                        </div>
                        <div class="col-1">
                            <button type="button" class="remove-btn" onclick="removeEducation(this)" title="Remove Education">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', newEducation);
        educationCount++;
    } else {
        alert('Maximum 3 education entries allowed!');
    }
}

function removeEducation(button) {
    const educationEntries = document.getElementsByClassName('education-entry');
    if (educationEntries.length > 1) {
        button.closest('.education-entry').remove();
        educationCount--;
    } else {
        alert('At least one education entry is required!');
    }
}

// Add event listeners when document loads
document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers to existing remove buttons
    document.querySelectorAll('#education .remove-btn').forEach(button => {
        button.onclick = function() { removeEducation(this); };
    });
});

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded!');
    
    const addButton = document.getElementById('add-education');
    console.log('Add button:', addButton);
    
    if (addButton) {
        addButton.addEventListener('click', function() {
            console.log('Add button clicked!');
            const container = document.getElementById('education-container');
            const entries = container.getElementsByClassName('education-entry');
            const newIndex = entries.length;

            const newEntry = document.createElement('div');
            newEntry.className = 'education-entry mb-3';
            newEntry.innerHTML = `
                <div class="row">
                    <div class="col-11">
                        <input type="text" class="form-control mb-2" name="school_${newIndex}" placeholder="School/University">
                        <input type="text" class="form-control mb-2" name="degree_${newIndex}" placeholder="Degree">
                        <input type="text" class="form-control mb-2" name="edu_location_${newIndex}" placeholder="Location">
                        <input type="text" class="form-control mb-2" name="edu_duration_${newIndex}" placeholder="Duration">
                    </div>
                    <div class="col-1">
                        <button type="button" class="btn btn-danger remove-education">×</button>
                    </div>
                </div>
            `;
            container.appendChild(newEntry);

            // Add event listener to the new remove button
            const removeButton = newEntry.querySelector('.remove-education');
            removeButton.addEventListener('click', function() {
                if (document.getElementsByClassName('education-entry').length > 1) {
                    newEntry.remove();
                }
            });
        });
    }

    // Add event listeners to existing remove buttons
    document.querySelectorAll('.remove-education').forEach(button => {
        button.addEventListener('click', function() {
            if (document.querySelectorAll('.education-entry').length > 1) {
                this.closest('.education-entry').remove();
            }
        });
    });
});

// Function to reindex education entries
function reindexEducationEntries() {
    const educationEntries = document.querySelectorAll('.education-entry');
    educationEntries.forEach((entry, index) => {
        entry.querySelectorAll('input').forEach(input => {
            const name = input.getAttribute('name');
            const newName = name.replace(/\d+/, index);
            input.setAttribute('name', newName);
        });
    });
}

function createEducationEntry(index) {
    return `
        <div class="education-entry mb-3">
            <div class="row">
                <div class="col-11">
                    <div class="row">
                        <div class="col-md-6">
                            <input type="text" class="form-control" name="school_${index}" placeholder="School/University">
                        </div>
                        <div class="col-md-6">
                            <input type="text" class="form-control" name="degree_${index}" placeholder="Degree">
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-4">
                            <input type="text" class="form-control" name="edu_location_${index}" placeholder="Location">
                        </div>
                        <div class="col-md-4">
                            <input type="month" class="form-control" name="edu_start_${index}" placeholder="Start Date">
                        </div>
                        <div class="col-md-4">
                            <input type="month" class="form-control" name="edu_end_${index}" placeholder="End Date">
                        </div>
                    </div>
                </div>
                <div class="col-1">
                    <button type="button" class="btn btn-danger btn-sm remove-education">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
}

function formatEducationDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    const month = date.toLocaleString('default', { month: 'long' });
    const year = date.getFullYear();
    return `${month} ${year}`;
}

$(document).ready(function() {
    // Handle remove project
    $('.project-container').on('click', '.remove-project', function() {
        const projectEntries = $('.project-entry');
        if (projectEntries.length > 1) {  // Keep at least one project entry
            $(this).closest('.project-entry').remove();
        } else {
            alert('You must keep at least one project entry.');
        }
    });

    // Your existing add project code
    $('.add-project').click(function() {
        const projectEntries = $('.project-entry');
        const newIndex = projectEntries.length;
        
        if (newIndex < 3) {  // Limit to 3 projects
            const newProject = createProjectEntry(newIndex);
            $(this).before(newProject);
        } else {
            alert('Maximum 3 projects allowed.');
        }
    });
});

function createProjectEntry(index) {
    return `
        <div class="project-entry mb-3">
            <div class="row">
                <div class="col-11">
                    <div class="row">
                        <div class="col-md-12">
                            <input type="text" class="form-control" name="project_title_${index}" 
                                   placeholder="Project Title">
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-12">
                            <div class="project-points">
                                <textarea class="form-control" name="project_description_${index}[]" 
                                          placeholder="Project Description" rows="3"></textarea>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-1">
                    <button type="button" class="btn btn-danger btn-sm remove-project">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
} 