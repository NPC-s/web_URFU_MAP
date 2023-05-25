function saveFloor(number){
    localStorage.setItem("floor", number);
}

function setStartFloor(){
    localStorage.setItem("floor", 2);
}

function printFloor(){
    var src = document.getElementById("Floor");
    var img = getFloor();
    src.appendChild(img);
} 

function getFloor(){
    var img = document.createElement("img");    
    var floor = localStorage.getItem("floor");
    img.src = "../images/floor" + floor + ".svg";
    img.className = "map";
    return img;
}

function printFloorWithPath(path){
    debugger;
    var src = document.getElementById("Floor");
    var floor = localStorage.getItem("floor");
    var canvas = document.createElement("canvas");
    canvas.width = 1920;
    canvas.height = 1080;
    canvas.className = "map";

    var ctx = canvas.getContext("2d");
    var isFirstPointFinded = false;

    for (var point of path){
        var fields = point.fields;
        var isCurrentFloor = fields.floor == floor;

        if (isCurrentFloor && !isFirstPointFinded){
            isFirstPointFinded = true;
            ctx.moveTo(fields.relativeX, fields.relativeY);
            continue;
        }

        if (!isCurrentFloor && isFirstPointFinded) break;

        if (!isCurrentFloor) continue;
        
        ctx.lineTo(fields.relativeX, fields.relativeY);
    }

    ctx.lineWidth = 10;
    ctx.strokeStyle = "#d64c70";

    ctx.stroke();

    src.appendChild(canvas);
}

function getArray(){
    let array = [];

    var i = 5;
    while(i > 0){
        array.push({
            floor: 2,
            relativeX: getRandomNumber(0, 1000),
            relativeY: getRandomNumber(0, 1000) 
        });
        i--;
    }

    return array;
}

function getRandomNumber(min, max) {
    return Math.random() * (max - min) + min
  }