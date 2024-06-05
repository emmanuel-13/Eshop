join = document.getElementById("join");
id = document.getElementById("myroomid");
room = document.getElementById("myroomname")
csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

join.addEventListener("click", function(e){
    e.preventDefault();
    
    data = {
        "id": id.value,
        "csrf_token": csrf_token,
        "room": room.value,
    }

    $.ajax({
        type: "POST",
        url: "/auths/join/",
        dataType: "json",
        data: data,
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", data['csrf_token']);
        },
        success: function(res){
            if (res.status === true) {
                alert(res.msg);
                window.location.href = `http://127.0.0.1:8000/auths/room/${data['room']}`
            }else{
                alert("error processing request")
            }
        },
        error: function(err){
            alert(err)
        }
    })
})