document.addEventListener('DOMContentLoaded', function() {
    // Add summary point
    document.getElementById('add-summary-point').addEventListener('click', function() {
        const summaryPoint = document.createElement('div');
        summaryPoint.className = 'summary-point';
        summaryPoint.innerHTML = `
            <textarea name="summary[]" placeholder="Enter a summary point"></textarea>
            <button type="button" class="remove-point">Remove</button>
        `;
        document.querySelector('.summary-points').appendChild(summaryPoint);
    });

    // Remove summary point
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-point')) {
            // Check if this is not the last summary point
            const summaryPoints = document.querySelectorAll('.summary-point');
            if (summaryPoints.length > 1) {
                e.target.closest('.summary-point').remove();
            } else {
                // If it's the last point, just clear the textarea
                e.target.closest('.summary-point').querySelector('textarea').value = '';
            }
        }
    });

    // Add experience entry
    document.querySelector('.add-experience').addEventListener('click', function() {
        const hiddenEntry = document.querySelector('.experience-entry[style="display:none"]');
        if (hiddenEntry) {
            hiddenEntry.style.display = '';
        }
    });

    // Add project
    document.querySelector('.add-project').addEventListener('click', function() {
        const template = `
            <div class="project-entry">
                <input type="text" name="project_name[]" placeholder="Project Name">
                <input type="text" name="project_tech[]" placeholder="Technologies Used">
                <textarea name="project_description[]" placeholder="Project Description"></textarea>
                <input type="url" name="project_link[]" placeholder="Project Link (optional)">
                <button type="button" class="remove-project">Remove Project</button>
            </div>
        `;
        document.querySelector('.projects-container').insertAdjacentHTML('beforeend', template);
    });

    // Add achievement
    document.querySelector('.add-achievement').addEventListener('click', function() {
        const template = `
            <div class="achievement-entry">
                <textarea name="achievements[]" placeholder="Enter achievement"></textarea>
                <button type="button" class="remove-achievement">Remove</button>
            </div>
        `;
        document.querySelector('.achievements-container').insertAdjacentHTML('beforeend', template);
    });

    // Add education
    document.querySelector('.add-education').addEventListener('click', function() {
        const hiddenEntry = document.querySelector('.education-entry[style="display:none"]');
        if (hiddenEntry) {
            hiddenEntry.style.display = '';
        }
    });

    // Remove buttons functionality
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-project')) {
            e.target.closest('.project-entry').remove();
        }
        if (e.target.classList.contains('remove-achievement')) {
            e.target.closest('.achievement-entry').remove();
        }
    });

    // Add description point
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('add-description')) {
            const expId = e.target.getAttribute('data-exp-id');
            const descriptionPoint = document.createElement('div');
            descriptionPoint.className = 'description-point';
            descriptionPoint.innerHTML = `
                <textarea name="exp_description_${expId}[]" placeholder="Description point"></textarea>
                <button type="button" class="remove-description">Remove</button>
            `;
            // Insert before the add button
            e.target.parentElement.insertBefore(descriptionPoint, e.target);
        }
    });

    // Remove description point
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-description')) {
            const descriptionPoints = e.target.closest('.description-points').querySelectorAll('.description-point');
            if (descriptionPoints.length > 1) {
                e.target.closest('.description-point').remove();
            } else {
                // If it's the last point, just clear the textarea
                e.target.closest('.description-point').querySelector('textarea').value = '';
            }
        }
    });
}); 