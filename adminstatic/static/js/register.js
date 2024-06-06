const username = document.querySelector("#InputUsername");
const feedback = document.querySelector(".Username");
const email = document.querySelector("#InputEmail");
const emailfeedback = document.querySelector(".Email");

username.addEventListener("keyup", (e) => {
    const userval = e.target.value;

    if (userval.length > 3) {
        fetch("/auths/validate/", {
            body: JSON.stringify({'username': userval}),
            method: "POST",

        }).then((res)=>res.json()).then((data)=> {
            if(data.error){
                username.classList.add("is-invalid");
                feedback.style.display = "block";
                feedback.innerHTML = `<p> ${data.error} </p>`
            } else{
                username.classList.remove("is-invalid");
                feedback.style.display = "block";
                feedback.innerHTML = `<p> ${data.success} </p>`
            }
    });
    } else {
        console.log("Failed to post data");
    }
})

email.addEventListener("keyup", (e) => {
    const myemail = e.target.value;

    if (myemail.length > 0) {
        fetch("/auths/email_validate/", {
            body: JSON.stringify({'email': myemail}), 
            method: "POST"
        }).then(res => res.json()).then(data => {
            if (data.error) {
                email.classList.add("is-invalid");
                emailfeedback.style.display = "block";    
                emailfeedback.innerHTML = `<p> ${data.error} </p>`;
            } else {
                email.classList.remove("is-invalid");
                emailfeedback.style.display = "block";
                emailfeedback.innerHTML = `<p> ${data.success} </p>`;
            }
            
        });
    }
    else{
        console.log("failed to post email")
    }
    
})