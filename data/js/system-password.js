
window.addEventListener('load', function () {
    var forms = document.getElementsByClassName('needs-validation');
    var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                var password = document.getElementById('password').value;
                var passwordUser = document.getElementById('password_user');

                if (passwordUser.checked) {
                    setCursorBusy();
                    cmd(`set-password-general=${password}`);
                } else {
                    setCursorBusy();
                    cmd(`set-password=${password}`);
                }

                setTimeout(function() {
                    smoothPageFade('index.html');
                }, 3000);                
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Adiciona ouvinte de evento de entrada para verificar a correspondência das senhas
    var passwordInput = document.getElementById('password');
    var confirmPasswordInput = document.getElementById('password_confirm');

    passwordInput.addEventListener('input', function () {
        if (passwordInput.value !== "") {
            if (passwordInput.value !== confirmPasswordInput.value) {
                confirmPasswordInput.setCustomValidity("As senhas não correspondem.");
            } else {
                confirmPasswordInput.setCustomValidity("");
            }
        }
    });

    confirmPasswordInput.addEventListener('input', function () {
        if (confirmPasswordInput.value !== "") {
            if (passwordInput.value !== confirmPasswordInput.value) {
                confirmPasswordInput.setCustomValidity("As senhas não correspondem.");
            } else {
                confirmPasswordInput.setCustomValidity("");
            }
        }
    });
}, false);

function togglePasswordVisibility(event) {
    event.preventDefault(); // Prevent form submission
    var passwordField = document.getElementById('password');
    var passwordField2 = document.getElementById('password_confirm');
    var fieldType = passwordField.getAttribute('type');
    if (fieldType === 'password') {
        passwordField.setAttribute('type', 'text');
        passwordField2.setAttribute('type', 'text');
        document.getElementById('password_visibility').innerHTML = 'visibility_off';
    } else {
        passwordField.setAttribute('type', 'password');
        passwordField2.setAttribute('type', 'password');
        document.getElementById('password_visibility').innerHTML = 'visibility';
    }
}

document.getElementById('btn_visibility').addEventListener('click', togglePasswordVisibility);