deleted = document.getElementById("del");
show = document.getElementById("show").innerHTML;

deleted.addEventListener("click", function(e){
    e.preventDefault();

    alert("welcome")

    // $.ajax({
    //     type: "POST",
    //     url: "/delete_todo/",
    //     dataType: "json",
    //     data: {
    //         "pk": pk,
    //     },
    //     beforeSend: function(xhr) {
    //         xhr.setRequestHeader("X-CSRFToken", csrf);
    //     },
    //     success: function(res){
    //         if (res.success) {
    //             alert(res.success);
    //         } else {
    //             alert("Failed to create")
    //         }
    //     }
    // })
})