output = "";
id = document.getElementById("id");
send = document.getElementById("send");
mes = document.getElementById("mes");
roomnames = document.getElementById("roomnames");
csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;

send.addEventListener("click", function(e){
    e.preventDefault();
    

    if (mes.value.length < 1 ){
        alert("please enter a resonable message");
    }else{
        data = {
            "id": id.value,
            "room": roomnames.value,
            "csrf": csrf,
            "message": mes.value,
        }

        $.ajax({
            type: "POST",
            url: "/auths/create_message/",
            dataType: "json",
            data: data,
            beforeSend: function(xhr){
                xhr.setRequestHeader("X-CSRFToken", data['csrf'])
            },
            success: function(res){
                if (res.status == true) {
                    window.location.href = `http://127.0.0.1:8000/auths/room/${data['room']}`    
                }
            },
            error: function(err){
                alert("error processing information");
            }
        })
    }
});
