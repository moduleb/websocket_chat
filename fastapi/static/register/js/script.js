// Переключение Register / Login
const loginLink = document.getElementById('login-link');

const registerLink = document.getElementById('register-link');
const formTypeMarkup = document.getElementById('form-type-markup');

const registerFormBox = document.getElementById('register');
const loginFormBox = document.getElementById('login');
const forms = document.getElementsByTagName('form');

const formSelector = document.getElementById('form-selector-wrap');
const formGreeting = document.getElementById('form-greeting');
const formDescription = document.getElementById('form-description');
const formBox = document.getElementById('form-box');

const registerPasswordField = document.getElementById('register-password-field');
const loginPasswordField = document.getElementById('login-password-field');

// Иконка глаза в пароле
const registerOpenEyeIcon = document.getElementById("register-open-eye-icon");
const registerCrossedEyeIcon = document.getElementById("register-crossed-eye-icon");
const loginOpenEyeIcon = document.getElementById("login-open-eye-icon");
const loginCrossedEyeIcon = document.getElementById("login-crossed-eye-icon");

const successMessage = document.getElementById("success-message");
const successMessageText = successMessage.querySelector("span");

const email = document.getElementById("register-email-field");
const nameField = document.getElementById("register-name-field");
const passwordField = document.getElementById("register-password-field");
const loginNameField = document.getElementById("login-name-field");
const form = document.getElementsByTagName("form")[0];
const formLogin = document.getElementsByTagName("form")[1];
const emailError = document.querySelector("#register-email-field + span.error");
const nameError = document.querySelector("#register-name-field + span.error");
const passwordError = document.querySelector("#register-password-field + span.error");

// var leftDistance = "";


// --------------- Submit Register -----------------------------------------------------

form.addEventListener("submit", async function (event) {
    var isvalid = true;

    // Валидация полей
    if (!email.validity.valid) {
        // Если поле email не валидно, отображаем сообщение об ошибке
        showEmailError();
        // Предотвращаем стандартное событие отправки формы
        event.preventDefault();
        isvalid = false;
    } else {
        emailError.textContent = "";
    }

    if (!nameField.validity.valid) {
        showNameError();
        event.preventDefault();
        isvalid = false;
    } else {
        nameError.textContent = "";
    }

    if (!passwordField.validity.valid) {
        showPasswordError();
        event.preventDefault();
        isvalid = false;
    } else {
        passwordError.textContent = "";
    }

    // Если все поля валидные - отправляем форму
    if (isvalid) {
        event.preventDefault();

        // Создаем объект для отправки
        const requestBody = {
            username: nameField.value,
            password: passwordField.value
        };

        // Добавляем telegram_id только если оно заполнено
        if (email.value.trim() !== "") {
            requestBody.telegram_id = email.value;
    }
        try {
            const response = await fetch('/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            if (response.status === 201) {
                window.location.href = '/success/register';

            } else if (response.status === 409) {
                alert('Пользователь с таким именем уже существует.');

            } else {
                const errorData = await response.json();
                alert('Ошибка: ' + (errorData.message || 'Неизвестная ошибка'));
            }
        } catch (error) {
            const errorData = await response.json();
            console.error('Ошибка при отправке запроса:', error);
            console.error('Ошибка при отправке запроса:', errorData);
            alert('Произошла ошибка при регистрации. Пожалуйста, попробуйте еще раз.');
        }
    }
});


// --------------- Submit Login --------------------------------------------------------

formLogin.addEventListener("submit", async function (event) {

    // Проверка валидности полей
    if (!loginNameField.validity.valid || !loginPasswordField.validity.valid) {
        alert("Wrong login or password");
        event.preventDefault();

    } else {
        // Если все поля валидные - отправляем форму
        event.preventDefault(); 

        try {
            const response = await fetch('/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: loginNameField.value,
                    password: loginPasswordField.value
                })
            });

            if (response.status === 200) {
                window.location.href = '/success/login';

            } else if (response.status === 401) {
                alert('Wrong login or password');

            } else {
                const errorData = await response.json();
                alert('Ошибка: ' + (errorData.message || 'Неизвестная ошибка'));
            }

        } catch (error) {
            console.error('Ошибка при отправке запроса:', error);
            alert('Произошла ошибка при авторизации. Пожалуйста, попробуйте еще раз.');
        }
    }
});


// --------------- Отображение ошибок в полях ------------------------------------------

function showEmailError() {
  // Если поле пустое...
  // if (email.validity.valueMissing) {
  //   emailError.textContent = "You need to enter Telegram ID.";
  //   }

  // Если поле содержит не email-адрес...
  if (email.validity.typeMismatch) {
    emailError.textContent = "Entered value needs to be digits.";

    // Если содержимое слишком короткое...
  } else if (email.validity.tooShort) {
    emailError.textContent = `Telegram ID should be ${email.minLength} digits; you entered ${email.value.length}.`;
  }
  // Задаём стилизацию
  emailError.className = "error active";
}

function showNameError() {
  // Если поле пустое...
  if (nameField.validity.valueMissing) {
    nameError.textContent = "You need to enter an user name.";

    // Если содержимое слишком короткое...
  } else if (nameField.validity.tooShort) {
    nameError.textContent = `User name should be at least ${nameField.minLength} characters; you entered ${nameField.value.length}.`;

    // Если содержит недопустимые символы...
  } else if (nameField.validity.patternMismatch) {
    nameError.textContent = "User name can only contain English letters and numbers.";
  }
  // Задаём стилизацию
  nameError.className = "error active";
}

function showPasswordError() {
  // Если поле пустое...
  if (passwordField.validity.valueMissing) {
    passwordError.textContent = "You need to enter an password.";

    // Если содержимое слишком короткое...
  } else if (passwordField.validity.tooShort) {
    passwordError.textContent = `Password should be at least ${passwordField.minLength} characters; you entered ${passwordField.value.length}.`;

    // Если содержит недопустимые символы...
  } else if (passwordField.validity.patternMismatch) {
    passwordError.textContent = "Password must contain uppercase and lowercase letters and digits";
  }
  // Задаём стилизацию
  nameError.className = "error active";
}


// --------------- Переключение видимости пароля ---------------------------------------

function showPassword() {
  loginPasswordField.type = "text";
  loginCrossedEyeIcon.style.display = "none";
  loginOpenEyeIcon.style.display = "block";

  registerPasswordField.type = "text";
  registerOpenEyeIcon.style.display = "block";
  registerCrossedEyeIcon.style.display = "none";
}

function hidePassword() {
  loginPasswordField.type = "password";
  loginCrossedEyeIcon.style.display = "block";
  loginOpenEyeIcon.style.display = "none";

  registerPasswordField.type = "password";
  registerOpenEyeIcon.style.display = "none";
  registerCrossedEyeIcon.style.display = "block";
}


// --------------- Переключение Register / Login ---------------------------------------

// Добавляем обработчик события на клик по ссылке Login
loginLink.addEventListener('click', function (e) {
  e.preventDefault();

  // form selector
  loginLink.style.color = "#FFF";
  registerLink.style.color = "#9E896A";

  formTypeMarkup.style.left = "12px"

  // form visibility
  loginFormBox.classList.remove("hidden");
  registerFormBox.classList.add("hidden");

  reset()
});

// Добавляем обработчик события на клик по ссылке Register
registerLink.addEventListener('click', function (e) {
  e.preventDefault();

  // form selector
  registerLink.style.color = "#FFF";
  loginLink.style.color = "#9E896A";
  leftDistance = (formSelector.offsetWidth - 159) + "px";
  formTypeMarkup.style.left = leftDistance;

  // form visibility
  loginFormBox.classList.add("hidden");
  registerFormBox.classList.remove("hidden");

  reset()
});

/*
Сбрасывает содержимое форм, ошибки валидации, и видимость пароля 
  при переключении типа формы (login, register)
*/
function reset() {
  for (var i = 0; i < forms.length; i++) {
    forms[i].reset()
  }
  emailError.textContent = ""; // Сбросить содержимое сообщения
  // emailError.className = "error"; // Сбросить визуальное состояние сообщения 
  nameError.textContent = "";
  // nameFieldError.className = "error";
  passwordError.textContent = "";
  hidePassword()
}

