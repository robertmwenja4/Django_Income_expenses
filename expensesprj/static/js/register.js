// const config = {};

// const Index = {
//     init(){
//         console.log('object');
//         $('#usernameField').on('keyup',this.changeUsername);
//     },
//     changeUsername(){
//         console.log('Username Changed');
//     }
// };
// Index.init();

const usernameField = document.querySelector("#usernameField");
const feedbackField = document.querySelector(".invalid-feedback");
const emailField = document.querySelector("#emailField");
const emailFeedbackField = document.querySelector(".emailFeedback");
const usernameSuccess = document.querySelector(".usernameSuccess");
const emailSuccess = document.querySelector(".emailSuccess");
const passwordField = document.querySelector("#passwordField");
const submitBtn = document.querySelector(".submitBtn");
// const showHidePassword = document.querySelector(".showHidePassword");
const showHidePassword = document.getElementById("showHidePassword");

const handleClickPassword = (e) => {
    console.log("Hello");
    if (showHidePassword.textContent === "SHOW") {
        passwordField.setAttribute("type","text");
        showHidePassword.textContent = "HIDE";
    }else{
        passwordField.setAttribute("type","password");
        showHidePassword.textContent = "SHOW";
    }
}

showHidePassword.addEventListener("click", handleClickPassword);

emailField.addEventListener("keyup", (e)=>{
    const emailVal = e.target.value;
    emailFeedbackField.style.display = "none";
    emailSuccess.style.display = "block";
    emailSuccess.textContent = `Checking ${emailVal}`;
    emailField.classList.remove("is-invalid")
    if(emailVal.length > 0){
        fetch("/authentication/email-validation",
            {
                body: JSON.stringify({email: emailVal}),
                method: 'POST', 
            }
        ).then((res)=> res.json())
        .then((data)=>{
            console.log(data);
            emailSuccess.style.display = "none";
            if(data.email_error){
                emailField.classList.add("is-invalid");
                emailFeedbackField.style.display = "block";
                emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
                submitBtn.disabled = true;
            }else{
                submitBtn.disabled = false;
            }
        })
    }
});
usernameField.addEventListener("keyup", (e)=>{
    const usernameVal = e.target.value;
    usernameSuccess.style.display = "block";
    usernameSuccess.textContent = `Checking ${usernameVal}`;
    feedbackField.style.display = "none";
    usernameField.classList.remove("is-invalid")
    if(usernameVal.length > 0){
        fetch("/authentication/username-validation",
            {
                body: JSON.stringify({username: usernameVal}),
                method: 'POST', 
            }
        ).then((res)=> res.json())
        .then((data)=>{
            console.log(data);
            usernameSuccess.style.display = "none";
            if(data.username_error){
                usernameField.classList.add("is-invalid");
                feedbackField.style.display = "block";
                feedbackField.innerHTML = `<p>${data.username_error}</p>`;
                submitBtn.disabled = true;
            }
            else{
                submitBtn.disabled = false;
            }
        })
    }
});