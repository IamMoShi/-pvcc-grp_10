let form = document.querySelector('#registerForm');

form.email.addEventListener('change', function() {
    validEmail(this);
});

form.password.addEventListener('change', function() {
    validPassword(this);
});

form.confirmation.addEventListener('change', function() {
    validConfirmation(this, form.password);
});

form.lastname.addEventListener('change', function() {
    noBlank(this);
});

form.firstname.addEventListener('change', function() {
    noBlank(this);
});

form.addEventListener('submit', function(e){
    e.preventDefault();
    if (validEmail(form.email)
        && validPassword(form.password)
        && validConfirmation(form.confirmation, form.password)
        && noBlank(form.lastname)
        && noBlank(form.firstname)
        ) {
        form.submit();
    }
});

const validEmail = function(inputEmail) {
    // création de la RegExp pour la validation de l'email
    let emailRegExp = new RegExp(
        '^[a-zA-Z0-9._-]+[@]{1}[a-zA-Z0-9._-]+[.]{1}[a-z]{2,10}$',
        'g'
    );
    let small = inputEmail.nextElementSibling;
    if (inputEmail.value == ''){
        inputEmail.classList.remove('input-sucess');
        inputEmail.classList.remove('input-danger');
        small.innerHTML = "";
        small.classList.remove('text-success');
        small.classList.remove('text-danger');
        return false;
    }else if (emailRegExp.test(inputEmail.value)) {
        inputEmail.classList.remove('input-danger');
        inputEmail.classList.add('input-success');
        small.innerHTML = "Adresse mail valide";
        small.classList.remove('text-danger');
        small.classList.add('text-success');
        return true;
    }else{
        inputEmail.classList.remove('input-sucess');
        inputEmail.classList.add('input-danger');
        small.innerHTML = "Adresse mail invalide";
        small.classList.remove('text-success');
        small.classList.add('text-danger');
        return false;
    }

};


const validPassword = function(inputPassword) {
    // création de la RegExp pour la validation de l'email
    // Minimum min and maximum max characters, at least one uppercase letter, 
    // one lowercase letter, one number and one special character
    const min = 8;
    const max = 16;
    let small = inputPassword.nextElementSibling;
    let password = inputPassword.value;
    let msg = "HELLO";
    let passwordValid = false;
    let startMessage = "Le mot de passe doit contenir au moins "
    if (password.length < min){
        msg = startMessage + min + " caractères";
    }else if (password.length > max){
        msg = "Le mot de passe doit contenir au plus " + max + " caractères";
    }else if (! /[A-Z]/.test(password)){
        msg = startMessage + "une majuscule";
    }else if (! /[a-z]/.test(password)){
        msg = startMessage + "une minuscule";
    }else if (! /[0-9]/.test(password)){
        msg = startMessage + "un chiffre";
    }else if (! /[@$!%*?&_-]/.test(password)){
        msg = startMessage + "un caractere des caractères spéciaux @$!%*?&_-";
    }else if (/\s/.test(password)){
        msg = "Le mot de passe ne doit pas contenir d'espace";
    }else if (!/^[a-zA-Z0-9@$!%*?&_-]+$/.test(password)){
        msg = "Le mot de passe contient un caractère interdit";
    }else {
        msg = "Mot de passe valide";
        passwordValid = true
    }
    small.innerHTML = msg;
    if (passwordValid){
        inputPassword.classList.remove('input-danger');
        inputPassword.classList.add('input-success');
        small.classList.remove('text-danger');
        small.classList.add('text-success');
    }else{
        inputPassword.classList.remove('input-success');
        inputPassword.classList.add('input-danger');
        small.classList.remove('text-success');
        small.classList.add('text-danger');
    }
    return passwordValid;
};

const validConfirmation = function(inputConfirmation, formPassword) {
    let conf = inputConfirmation.value;
    let password = formPassword.value;
    let valid = false;
    let small = inputConfirmation.nextElementSibling;
    if (conf == password){
        inputConfirmation.classList.remove('input-danger');
        inputConfirmation.classList.add('input-success');
        small.classList.remove('text-danger');
        small.classList.add('text-success');
        small.innerHTML = "";
        valid = true;
    }else{
        inputConfirmation.classList.remove('input-success');
        inputConfirmation.classList.add('input-danger');
        small.classList.remove('text-success');
        small.classList.add('text-danger');
        small.innerHTML = "Les mots de passe ne correspondent pas";
    }
    return valid;
};

const noBlank = function(input) {
    let valeur = input.value;
    let small = input.nextElementSibling;
    let valid = false;
    if (valeur == ""){
        input.classList.remove('input-success');
        small.classList.remove('text-success');
        input.classList.remove('input-danger');
        small.classList.remove('text-danger');
        small.innerHTML = "";
    }else if (!/^[A-Z][A-Za-z\é\è\ê\-]+$/.test(valeur)) {
        input.classList.remove('input-success');
        input.classList.add('input-danger');
        small.classList.remove('text-success');
        small.classList.add('text-danger');
        small.innerHTML = "Pensez à remplacer les espaces par des tirets et à mettre une majuscule";
    }else if (!/[A-Z]/.test(valeur)) {
        input.classList.remove('input-success');
        input.classList.add('input-danger');
        small.classList.remove('text-success');
        small.classList.add('text-danger');
        small.innerHTML = "Pensez à commencer par une majuscule";
    }else {
        input.classList.remove('input-danger');
        input.classList.add('input-success');
        small.classList.remove('text-danger');
        small.classList.add('text-success');
        small.innerHTML = "";
        valid = true;
    }
    return valid;
};