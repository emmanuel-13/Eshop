data = {
    "topic": document.getElementById("topic"),
    "room": document.getElementById("room_name"),
    "description": document.getElementById("description_room"),
    "csrf_token": document.getElementsByName("csrfmiddlewaretoken"),
}

var sub = document.getElementById("sub");

sub.addEventListener("click", function(e){
    e.preventDefault();

    data = {
        "topic": data['topic'].value,
        "room": data['room'].value,
        "description": data['description'].value,
        "csrf_token": data['csrf_token'][0].value
    }
    

    if (data['topic'] === "" || data['room'] === "" || data['description'] === "") {
        console.log("error")
    } else {
        $.ajax({
            url: "/auths/room/",
            type: "POST",
            beforeSend: function(xhr){
                xhr.setRequestHeader("X-CSRFToken", data['csrf_token'])
            },
            dataType: "json",
            data: data,
            success: function(res){
                if (res.status === true) {
                    alert(res.msg);
                    window.location.href = `http://127.0.0.1:8000/auths/room/${data['room']}`;
                }else{
                    alert(res.msg);
                }
            },
            error: function(res){
                alert("errror, processing info")
                console.log("error processing data")
            }
        })
    }
})
