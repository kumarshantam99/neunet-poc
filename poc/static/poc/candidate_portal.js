

const configureButtons = () => {
    document.getElementById("resume-upload").onchange = () => {
        document.getElementById("candidate-resume-form").submit();
    };

    document.getElementById("add-degree").onclick = addDegreeButton;

    document.getElementById("add-experience").onclick = addExperienceButton;

    const degrees = document.querySelectorAll('[id^="remove-degree"]');
    let max = 0;
    for(var i = 0; i < degrees.length; i += 1){
        const id = degrees[i].id;
        const num = parseInt(id.substring(id.length - 1));
        if(num > max){
            max = num;
        }
    }
    removeDegreeButtons(max);

    const experiences = document.querySelectorAll('[id^="remove-experience"]');
    max = 0;
    for(var i = 0; i < experiences.length; i += 1){
        const id = experiences[i].id;
        const num = parseInt(id.substring(id.length - 1));
        if(num > max){
            max = num;
        }
    }
    removeExperienceButtons(max);

}


const addDegreeButton = () => {

    // const nodes = document.querySelectorAll("#education-section input[name=degree]");
    const nodes = document.querySelectorAll("[id^='degree-container']");

    let numDegrees = 1;

    if(nodes.length > 0){
        const last = nodes[nodes.length - 1];
        numDegrees = parseInt(last.id.substring(last.id.length-1, last.id.length)) + 1;
    }

    // console.log('adding degree: ' + numDegrees);

    const educationContainer = document.getElementById("education-section");

    const degreeContainer = document.createElement('div');
    degreeContainer.id = "degree-container" + numDegrees;

    degreeContainer.innerHTML +=             
        `<div class="form-group">
            <label class="col-md-4 control-label" for="degree` + numDegrees + `">Degree ` + numDegrees + ` Type</label>  
            <div class="col-md-4">
                <input id="degree` + numDegrees + `" type="text" name="degree" class="form-control input-md">
            </div>
        </div>

        <div class="form-group">
            <label class="col-md-4 control-label" for="field` + numDegrees + `">Field of Study</label>  
            <div class="col-md-4">
                <input id="field` + numDegrees + `" name="field` + numDegrees + `" type="text" placeholder="" class="form-control input-md">  
            </div>
        </div>

        <div class="form-group">
            <label class="col-md-4 control-label" for="remove-degree` + numDegrees + `"></label>
            <div class="col-md-4">
                <button id="remove-degree` + numDegrees + `" type="button" name="remove-degree` + numDegrees + `" class="btn btn-danger pull-right">-</button>
            </div>
        </div>`;

    educationContainer.appendChild(degreeContainer);

    removeDegreeButtons(numDegrees);
};


const addExperienceButton = () => {
    const nodes = document.querySelectorAll("[id^='experience-container']");

    let numExperience = 1;

    if(nodes.length > 0){
        const last = nodes[nodes.length - 1];
        numExperience = parseInt(last.id.substring(last.id.length-1, last.id.length)) + 1;
    }

    // console.log('adding expereince number ' + numExperience);

    const experienceContainer = document.getElementById("experience-section");

    const exp = document.createElement('div');
    exp.id = "experience-container" + numExperience;   

    exp.innerHTML += 
        `<div class="form-group">
            <label class="col-md-4 control-label" for="organization` + numExperience + `">Organization</label>  
            <div class="col-md-4">
                <input id="organization` + numExperience + `" type="text" class="form-control input-md">
            </div>
        </div>

        <div class="form-group">
            <label class="col-md-4 control-label" for="designation` + numExperience + `">Designation</label>  
            <div class="col-md-4">
                <input id="designation` + numExperience + `" type="text" class="form-control input-md">
            </div>
        </div>

        <div class="form-group">
            <label class="col-md-4 control-label" for="duration` + numExperience + `">Duration (Months)</label>  
            <div class="col-md-4">
                <input id="duration` + numExperience + `" type="text" class="form-control input-md">
            </div>
        </div>
        
        <div class="form-group">
            <label class="col-md-4 control-label" for="remove-experience` + numExperience + `"></label>
            <div class="col-md-4">
                <button id="remove-experience` + numExperience + `" type="button" name="remove-experience` + numExperience + `" class="btn btn-danger pull-right">-</button>
            </div>
        </div>`;

    experienceContainer.appendChild(exp);

    removeExperienceButtons(numExperience);
};


const removeDegreeButtons = numDegrees => {
    for(var i=1; i<=numDegrees; i += 1){
        removeDegreeButton(i);
    }
}

const removeDegreeButton = numDegrees => {
    // console.log('in remove degrees function with numDegrees:' + numDegrees);
    const element = document.getElementById("remove-degree" + numDegrees);
    if(element){
        element.onclick = () => {
            // console.log('tried to remove degree-container' + numDegrees);
            const degreeContainer = document.getElementById('degree-container' + numDegrees);
            degreeContainer.parentNode.removeChild(degreeContainer);
        }
    }
};

const removeExperienceButtons = numExperience => {
    for(var i=1; i<=numExperience; i += 1){
        removeExperienceButton(i);
    }
}

const removeExperienceButton = numExperience => {
    // console.log('in remove experience function with numExperience:' + numExperience);
    const element = document.getElementById("remove-experience" + numExperience);
    if(element){
        element.onclick = () => {
            // console.log('tried to remove experience-container' + numExperience);
            const experienceContainer = document.getElementById('experience-container' + numExperience);
            experienceContainer.parentNode.removeChild(experienceContainer);
        }
    }
};

configureButtons();
