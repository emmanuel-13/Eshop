deleted = document.getElementById("delete");
var id = document.getElementById("id");
csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;

deleted.addEventListener("click", function(e){
    e.preventDefault();

    data = {
        "id": id.value,
        "csrf": csrf
    }

    $.ajax({
        url: "/auths/room_delete/",
        type: "POST",
        dataType: "json",
        data: data,
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", data['csrf'])
        },
        success: function(res){
            if (res.status === true) {
                window.location.href = "http://127.0.0.1:8000/auths/community";
            } else {
                alert(res.msg);
            }
        }
    })
})
