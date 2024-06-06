
mybtn = document.getElementById("mybtn");
id_name = document.getElementById("id_name");
product_id = document.getElementById("product_id");
id_content = document.getElementById("id_content")
csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

mybtn.addEventListener("click", function(e){
    e.preventDefault();
    
    data = {
        "id_name": id_name,
        "id_content": id_content.value,
        "csrf_token": csrf_token,
        "product_id": product_id.value,
    }
    console.log(data);

    $.ajax({
        type: "POST",
        url: "/product_review/",
        dataType: "json",
        data: data,
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", data['csrf_token']);
        },
        success: function(res){
            console.log(res.status)
        },
        error: function(err){
            alert("error processing data")
        }
    })
})