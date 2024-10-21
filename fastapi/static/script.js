// Получаем элементы из DOM
const chatBox = document.getElementById('chat-box'); // Контейнер для отображения сообщений чата
const messageInput = document.getElementById('message-input'); // Поле ввода для сообщения
const sendButton = document.getElementById('send-button'); // Кнопка для отправки сообщения

let recipient = null; // Переменная для хранения имени получателя

// Функция для получения списка пользователей
async function fetchUsers() {
    try {
        const response = await fetch('/users'); // Запрос к серверу для получения списка пользователей
        if (!response.ok) {
            throw new Error('Сетевая ошибка: ' + response.status); // Обработка ошибок сети
        }
        const data = await response.json(); // Десериализация JSON

        // Проверьте структуру данных, чтобы убедиться, что вы получаете ожидаемый формат
        console.log(data); // Выводим весь объект данных в консоль для отладки

        const usernames = data.data.usernames; // Получаем массив имен пользователей

        // Обработка полученных имен
        console.log(usernames); // Выводим имена в консоль
        return usernames; // Возвращаем массив имен
    } catch (error) {
        console.error('Ошибка при получении пользователей:', error); // Логируем ошибку
    }
}

// Вызов функции для получения пользователей
fetchUsers().then(usernames => {
    if (usernames) {
        const usersList = document.getElementById('users'); // Получаем элемент списка пользователей
        usersList.innerHTML = ''; // Очищаем предыдущий список
        usernames.forEach(username => {
            const li = document.createElement('li'); // Создаем элемент списка
            li.textContent = username; // Устанавливаем текст элемента
            li.addEventListener('click', () => {
                recipient = username; // Устанавливаем переменную recipient на выбранное имя
                messageInput.placeholder = `Сообщение для ${recipient}`; // Изменяем текст подсказки
                console.log(`Выбран получатель: ${recipient}`); // Логируем выбранного получателя
            });
            usersList.appendChild(li); // Добавляем элемент в список
        });
    } else {
        console.log('Пользователи не найдены.'); // Сообщение, если пользователей нет
    }
});



const socket = new WebSocket('ws://127.0.0.1:8000/ws');

// Обработчик события для получения сообщений от сервера
socket.onmessage = function(event) {
    // Выводим данные в консоль для отладки
    console.log('Received message:', event.data);

    try {
        // Проверяем тип данных
        console.log('Type of event.data:', typeof event.data);

        // Если event.data является строкой, парсим его
        let messageData;
        if (typeof event.data === 'string') {
            messageData = JSON.parse(event.data);
        } else {
            messageData = event.data; // Используем напрямую, если это не строка
        }

        console.log('messageData:', messageData); // Проверяем, что данные распарсились правильно

        // Проверяем, что messageData действительно является объектом
        console.log('Type of messageData:', typeof messageData); // Выводим тип messageData
        console.log('Is messageData null?', messageData === null); // Проверяем, является ли messageData null

        if (typeof messageData === 'object' && messageData !== null) {
            // Извлекаем поля from_ и text
            const from_ = messageData.from_;
            const text = messageData.text;

            // Проверяем, что переменные определены
            console.log('Received from:', from_);
            console.log('Received text:', text);

            // Проверяем, что поля from_ и text существуют
            if (from_ !== undefined && text !== undefined) {
                // Создаем новый элемент div для отображения сообщения
                const messageElement = document.createElement('div');
                
                // Устанавливаем текст сообщения
                messageElement.textContent = `${from_}: ${text}`; // Форматируем сообщение

                // Добавляем элемент в контейнер чата
                chatBox.appendChild(messageElement);
                
                // Прокручиваем вниз, чтобы показать последнее сообщение
                chatBox.scrollTop = chatBox.scrollHeight;
            } else {
                console.error('Invalid message format: missing from_ or text', messageData);
            }
        } else {
            console.error('Parsed messageData is not an object:', messageData);
        }
    } catch (error) {
        console.error('Error parsing message:', error);
    }
};





// Обработчик события для кнопки отправки сообщения
sendButton.addEventListener('click', () => {
    const message = messageInput.value; // Получаем текст из поля ввода
    if (message) { // Проверяем, что сообщение не пустое
        // Создаем объект с сообщением и дополнительной информацией
        const jsonMessage = JSON.stringify({
            text: message, // Текст сообщения
            to: recipient // Получатель сообщения (можно изменить по необходимости)
        });
        socket.send(jsonMessage); // Отправляем JSON-объект на сервер
        messageInput.value = ''; // Очищаем поле ввода после отправки
    }
});

// Обработчик события для отправки сообщения по нажатию клавиши Enter
messageInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') { // Проверяем, была ли нажата клавиша Enter
        sendButton.click(); // Вызываем клик на кнопке отправки
    }
});

