document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');

    sendButton.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message !== '') {
            appendMessage('user', message);
            userInput.value = '';
            getBotResponse(message);
        }
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.textContent = message;

        messageElement.appendChild(messageContent);
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function getBotResponse(message) {
        // Simple keyword-based responses
        const dateRegex = /\b(?:\d{1,2}\/\d{1,2}\/\d{4}|\d{4}-\d{1,2}-\d{1,2})\b/g;
        const lowerCaseMessage = message.toLowerCase();
        let response = '';

        if (lowerCaseMessage.includes('hello') || lowerCaseMessage.includes('hi')) {
            response = 'Hello! Welcome to our hotel booking service. How can I assist you today?';
        } else if (lowerCaseMessage.includes('book') && lowerCaseMessage.includes('room')) {
            response = 'Sure! I can help you book a room. May I know your check-in and check-out dates?';
        } else if (lowerCaseMessage.includes('check-in') || lowerCaseMessage.includes('check-out') || lowerCaseMessage.includes('dates')) {
            const dates = message.match(dateRegex);

            if (dates && dates.length >= 2) {
                const checkInDate = moment(dates[0], 'MM/DD/YYYY');
                const checkOutDate = moment(dates[1], 'MM/DD/YYYY');

                if (checkInDate.isValid() && checkOutDate.isValid()) {
                    response = `Great! I've got your check-in date as ${checkInDate.format('MMMM D, YYYY')} and check-out date as ${checkOutDate.format('MMMM D, YYYY')}.`;
                } else {
                    response = 'Sorry, I couldn\'t parse the dates. Could you please reformat them as MM/DD/YYYY?';
                }
            } else {
                response = 'Could you please provide the check-in and check-out dates?';
            }
        } else if (lowerCaseMessage.includes('check availability')) {
            response = 'Please provide the dates you wish to stay, and I will check the availability for you.';
        } else if (lowerCaseMessage.includes('thank you') || lowerCaseMessage.includes('thanks')) {
            response = 'You\'re welcome! If you have any more questions, feel free to ask.';
        } else {
            response = 'I\'m sorry, I didn\'t understand that. Could you please rephrase or ask something else related to booking?';
        }

        // Simulate bot response delay
        setTimeout(() => {
            appendMessage('bot', response);
        }, 1000);
    }
});