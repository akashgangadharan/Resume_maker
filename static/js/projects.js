$(document).ready(function() {
    // Add Project
    $("#add-project-btn").click(function() {
        var projectCount = $(".project-entry").length;
        if (projectCount < 3) {
            var newProject = `
                <div class="project-entry mb-3">
                    <div class="row">
                        <div class="col-11">
                            <input type="text" class="form-control mb-2" 
                                   name="project_title_${projectCount}" 
                                   placeholder="Project Title">
                            <textarea class="form-control" 
                                      name="project_description_${projectCount}[]" 
                                      placeholder="Project Description" 
                                      rows="3"></textarea>
                        </div>
                        <div class="col-1">
                            <button type="button" class="btn btn-danger btn-sm delete-project">×</button>
                        </div>
                    </div>
                </div>
            `;
            $(this).before(newProject);
        } else {
            alert("Maximum 3 projects allowed!");
        }
    });

    // Delete Project
    $(document).on("click", ".delete-project", function() {
        if ($(".project-entry").length > 1) {
            $(this).closest(".project-entry").remove();
        } else {
            alert("At least one project is required!");
        }
    });
}); 