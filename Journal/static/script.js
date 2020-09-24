function darkfunc () {
    document.querySelector("body").classList.toggle("nightmode");
}

function thumbnail() {
    const x = document.getElementById("file-input").value;
    document.getElementById("preview").src = x;
}

function pwcheck(form) {
    password = form.password.value
    confirmation = form.confirmation.value

    var decimal=  /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$/;

    if(password.match(decimal) && password == confirmation)
    {
        return true;
    }
    else
    {
        alert("Weak Passwords or Passwords No Match");
        return false;
    }
}

$('#txtModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
  })