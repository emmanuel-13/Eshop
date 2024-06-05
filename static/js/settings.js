room = document.getElementById("room");
room.addEventListener("click", room_onclick)
function room_onclick(){
    document.getElementById('overall').style.display = "block";
    document.getElementById('rooms').style.display = "block";
    document.getElementById('pro').style.display = "none";
}

// rooms = document.getElementById("roomss");
// rooms.addEventListener("click", rooms_onclick)
// function rooms_onclick(){
//     document.getElementById('carrier').style.display = "block";
//     document.getElementById('overall').style.display = "none";
//     document.getElementById('rooms').style.display = "none";
// }

product = document.getElementById("product");
product.addEventListener("click", product_onclick)
function product_onclick(){
    document.getElementById('carrier').style.display = "block";
    document.getElementById('overall').style.display = "block";
    document.getElementById('pro').style.display = "block";
    document.getElementById('rooms').style.display = "none";
}

product = document.getElementById("products");
product.addEventListener("click", products_onclick)
function products_onclick(){
    document.getElementById('carrier').style.display = "block";
    document.getElementById('overall').style.display = "none";
    document.getElementById('pro').style.display = "none";
}