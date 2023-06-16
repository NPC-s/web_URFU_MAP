function changeClassroomInput(id, classrooms){
    let elem = document.getElementById(id);

    for (let classroom of classrooms){
        if (classroom.name == elem.value)
            return true;
    }

    elem.value = "";
    return false;
}

function checkSubmit(id, classrooms){
    let startValue = document.getElementById("start").value;
    let endValue = document.getElementById("end").value;

    if (startValue == "" || endValue == ""){
        debugger;
        return false;
    }

    let start = document.getElementsByName("start_point")[0];
    let end = document.getElementsByName("end_point")[0];
    start.value = "";
    end.value = "";

    for (let classroom of classrooms){
        if (startValue == classroom.name)
            start.value = classroom.pk;
        
        if (endValue == classroom.name)
            end.value = classroom.pk;

        if (start.value != "" && end.value != "")
            return true;
    }
}

function setStartMap(value, classrooms){
    debugger;
    for (let classroom of classrooms){
        if (value == classroom.name){
            saveFloorAndInstitue(classroom.floor, classroom.institue);
            break;
        }
    }
}