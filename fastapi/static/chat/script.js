// Получаем элементы из DOM
const chatBox = document.getElementById('chat-box'); // Контейнер для отображения сообщений чата
const messageInput = document.getElementById('message-input'); // Поле ввода для сообщения
const sendButton = document.getElementById('send-button'); // Кнопка для отправки сообщения
const myUsername = document.getElementById('my_username'); 
let my_username = "" // Переменная для хранение собственного имени
let recipient = null; // Переменная для хранения имени получателя


// ----------------- Работа со списком пользователей -----------------------------------

// Функция для получения списка пользователей
async function fetchUsers() {
    try {
        const response = await fetch('/api/users/'); // Запрос к серверу для получения списка пользователей
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
        const usersList = document.getElementById('user-list'); // Получаем элемент списка пользователей
        usersList.innerHTML = ''; // Очищаем предыдущий список
        usernames.forEach(username => {
            const li = document.createElement('li'); // Создаем элемент списка
            li.textContent = username; // Устанавливаем текст элемента

            li.addEventListener('click', async () => { // Объявляем обработчик как асинхронный
                // Убираем выделение у всех элементов списка
                const allItems = usersList.getElementsByTagName('li');
                for (const item of allItems) {
                    item.classList.remove('active'); // Удаляем класс выделения
                }

                // Устанавливаем переменную recipient на выбранное имя
                recipient = username; 
                messageInput.placeholder = `Сообщение для ${recipient}`; // Изменяем текст подсказки
                console.log(`Выбран получатель: ${recipient}`); // Логируем выбранного получателя
                
                // Получаем историю сообщений
                const messages = await fetchMessagesHistory(recipient);
                
                // Очищаем чат
                chatBox.innerHTML = ''; // Очищаем содержимое chatBox

                // Отображаем сообщения
                for (const msg of messages) { // Используем for...of для итерации по массиву
                    displayMessage(msg.from_, msg.text);
                }

                // Выделяем текущий элемент
                li.classList.add('active'); // Добавляем класс выделения
            });

            usersList.appendChild(li); // Добавляем элемент в список
        });
    } else {
        console.log('Пользователи не найдены.'); // Сообщение, если пользователей нет
    }
});


// ----------------- Получение истории сообщений ---------------------------------------

async function fetchMessagesHistory(recipient) {
    try {
        // Формируем URL с параметром recipient
        const response = await fetch(`/api/messages/?recipient=${encodeURIComponent(recipient)}`);

        if (!response.ok) {
            throw new Error('Сетевая ошибка: ' + response.status); // Обработка ошибок сети
        }
        const data = await response.json(); // Десериализация JSON

        my_username = data.data.username
        const messages = data.data.messages

        console.log(messages); // Выводим сообщения в консоль

        return messages; // Возвращаем массив сообщений
    } catch (error) {
        console.error('Ошибка при получении истории сообщений:', error); // Логируем ошибку
        return []; // Возвращаем пустой массив в случае ошибки
    }
}


// ----------------- Отображение сообщений  --------------------------------------------

// Функция для отображения сообщения в чате
function displayMessage(from_, text) {
    // Создаем новый элемент div для отображения сообщения
    const messageElement = document.createElement('div');
    
    // Устанавливаем стиль для выравнивания сообщения
    if (from_ === my_username) {
        messageElement.style.textAlign = 'right'; // Выравнивание влево для сообщений от my_username
        from_ = "You"
    } else {
        messageElement.style.textAlign = 'left'; // Выравнивание вправо для остальных сообщений
    }

    // Создаем элемент для имени отправителя
    const nameElement = document.createElement('span');
    nameElement.textContent = from_; // Устанавливаем текст имени
    nameElement.style.color = '#007bff'; // Устанавливаем цвет имени
    nameElement.style.fontSize = 'small'; // Устанавливаем размер шрифта
    nameElement.style.display = 'block'; // Делаем имя блочным элементом, чтобы оно было на отдельной строке

    // Создаем элемент для текста сообщения
    const textElement = document.createElement('div'); // Изменяем на div
    textElement.textContent = text; // Устанавливаем текст сообщения
    textElement.style.marginTop = '-6px'; // Устанавливаем верхний отступ для текста сообщения (можно настроить по желанию)

    // Добавляем элементы имени и текста в сообщение
    messageElement.appendChild(nameElement);
    messageElement.appendChild(textElement);

    // Добавляем элемент в контейнер чата
    chatBox.appendChild(messageElement);
    
    // Прокручиваем вниз, чтобы показать последнее сообщение
    chatBox.scrollTop = chatBox.scrollHeight;
}


// ----------------- Получение сообщения по websocket ----------------------------------

// const socket = new WebSocket('ws://127.0.0.1:80/ws');
const socket = new WebSocket(`${window.location.protocol.replace('http', 'ws').replace('https', 'wss')}//${window.location.host}/ws`);

// const socket = new WebSocket('/ws');

// Обработчик события onmessage для сокета
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
                if(from_ === recipient){ // показываем сообщение только если активна вкладка с отправителем
                // Вызываем функцию для отображения сообщения
                displayMessage(from_, text);
                }
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


// ----------------- Отправка сообщения по websocket -----------------------------------

// Обработчик события для кнопки отправки сообщения
sendButton.addEventListener('click', () => {
    const message = messageInput.value; // Получаем текст из поля ввода
    if (message && recipient) { // Проверяем, что сообщение не пустое
        // Создаем объект с сообщением и дополнительной информацией
        const jsonMessage = JSON.stringify({
            text: message, // Текст сообщения
            to: recipient // Получатель сообщения (можно изменить по необходимости)
        });
        socket.send(jsonMessage); // Отправляем JSON-объект на сервер
        messageInput.value = ''; // Очищаем поле ввода после отправки

        displayMessage(my_username, message)
    }
});

// Обработчик события для отправки сообщения по нажатию клавиши Enter
messageInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') { // Проверяем, была ли нажата клавиша Enter
        sendButton.click(); // Вызываем клик на кнопке отправки
    }
});

