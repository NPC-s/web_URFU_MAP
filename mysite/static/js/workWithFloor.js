function saveFloorAndInstitue(floor, institue){
    debugger;
    localStorage.setItem("floor", floor);
    localStorage.setItem("institue", institue);
}

function setStartFloor(){
    localStorage.setItem("floor", 2);
    localStorage.setItem("institue", "RI")
}

function getFloor(){
    return localStorage.getItem("floor");
}

function getInstitue(){
    return localStorage.getItem("institue");
}

function printPath(path){
    debugger;
    var src = document.getElementById("Floor");
    var floor = getFloor();
    var institue = getInstitue();
    var canvas = document.createElement("canvas");
    canvas.width = 1920;
    canvas.height = 1080;
    canvas.className = "map";

    var ctx = canvas.getContext("2d");
    var isFirstPointFinded = false;

    for (var point of path){
        var isCurrentPoint = point.floor == floor && point.institue == institue;

        if (isCurrentPoint && !isFirstPointFinded){
            isFirstPointFinded = true;
            ctx.moveTo(point.x, point.y);
            continue;
        }

        if (!isCurrentPoint && isFirstPointFinded) break;

        if (!isCurrentPoint) continue;
        
        ctx.lineTo(point.x, point.y);
    }

    ctx.lineWidth = 10;
    ctx.strokeStyle = "#d64c70";

    ctx.stroke();

    src.appendChild(canvas);
}

function getRandomNumber(min, max) {
    return Math.random() * (max - min) + min
}

function changeButtonsColor(startPoint, lastPoint){
    debugger;
    let floor = getFloor();
    let buttons = document.getElementsByName("button");

    for (let button of buttons){
        if (button.id == lastPoint.floor)
            button.style.background = '#f2505b';

        if (button.id == startPoint.floor)
            button.style.background = '#55e08d';

        if (button.id == floor)
            button.style.background = '#8cadde';
    }
}