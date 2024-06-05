leaving = document.getElementById('leave');
leaveroom = document.getElementById('leaveroom');
csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value

leaving.addEventListener("click", function(e){
    e.preventDefault();
    
    data = {
        "room": leaveroom.value,
        "id": leaveroomid.value,
        "csrf": csrf
    }

    console.log(data['room'])
    console.log(data['id'])

    $.ajax({
        type: "POST",
        url: "/auths/leave/",
        dataType: "json",
        data: data,
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", data['csrf']);
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
            alert("error ")
        }
    })
});