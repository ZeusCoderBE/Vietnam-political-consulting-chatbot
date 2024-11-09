let isTyping = false;

function displayUserMessage(query) {
    const chatOutput = document.getElementById('chat-output');
    chatOutput.innerHTML += ` 
        <div class="chat-message user">
            <div class="avatar user-avatar" style="background-image: url('https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o=');"></div>
            <div class="message">${query.replace(/\n/g, '<br>')}</div>
        </div>
    `;

    // Show thinking message with avatar when sending request
    const thinkingMessageDiv = document.createElement('div');
    thinkingMessageDiv.classList.add('chat-message', 'bot', 'thinking');

    const avatarDiv = document.createElement('div');
    avatarDiv.classList.add('avatar', 'bot-avatar');
    avatarDiv.style.backgroundImage = "url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSaWGBBfkJuhnliJK-b4EeUVGvRloaFwZcKtg&s')";

    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message');
    messageContainer.innerHTML = "Đang suy nghĩ..."; // Initial thinking text

    thinkingMessageDiv.appendChild(avatarDiv);
    thinkingMessageDiv.appendChild(messageContainer);
    chatOutput.appendChild(thinkingMessageDiv);
    chatOutput.scrollTop = chatOutput.scrollHeight;

    // Update thinking dots every 100ms
    let dots = 0;
    const dotsSequence = [".", "..", "..."];
    const dotsInterval = setInterval(function () {
        messageContainer.innerHTML = "Đang suy nghĩ" + dotsSequence[dots % 3]; // Cycle through dots
        dots++;
    }, 100);  // Update dots every 100ms
}
function formatLinks(text) {
    let formattedText = text.replace(/\n/g, "<br>");
    const linkPattern = /(https?:\/\/[^\s]+)/g;
    formattedText = formattedText.replace(linkPattern, function(match) {
        return `<a href="${match}" target="_blank" style="color: #1e90ff;">${match}</a>`;
    });

    return formattedText;
}

function displayBotMessage(response) {
    if (isTyping) return;
    const chatOutput = document.getElementById('chat-output');
    let message = response.result;
    message = formatLinks(message);
    const thinkingMessage = document.querySelector('.chat-message.bot.thinking');
    if (thinkingMessage) {
        thinkingMessage.remove();
    }
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message', 'bot');
    const avatarDiv = document.createElement('div');
    avatarDiv.classList.add('avatar', 'bot-avatar');
    avatarDiv.style.backgroundImage = "url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSaWGBBfkJuhnliJK-b4EeUVGvRloaFwZcKtg&s')";
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message');
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(messageContainer);
    chatOutput.appendChild(messageDiv);
    chatOutput.scrollTop = chatOutput.scrollHeight;
    isTyping = true; 
    let i = 0;
    const interval = setInterval(function() {
        if (message[i] === '<') {
            let tagEnd = message.indexOf('>', i);
            if (message.slice(i, tagEnd + 1).startsWith('<a')) {
                let closingTagEnd = message.indexOf('</a>', tagEnd);
                messageContainer.innerHTML += message.slice(i, closingTagEnd + 4);
                i = closingTagEnd + 4;
            } else {
                messageContainer.innerHTML += message.slice(i, tagEnd + 1);
                i = tagEnd + 1;
            }
        } else {
            messageContainer.innerHTML += message[i];
            i++;
        }
        if (i >= message.length) {
            clearInterval(interval);
            isTyping = false;
        }
    }, 5);  
}
$('#send-button').on('click', function() {
    const query = $('#user-query').val();
    if (!query || isTyping) return; 
    displayUserMessage(query);
    $('#user-query').val(''); 
    $('#send-button').prop('disabled', true);

    $.ajax({
        url: '/query',
        method: 'POST',
        data: { query: query },
        success: function(response) {
            displayBotMessage(response);
        },
        error: function(error) {
            console.error("Error:", error);
        },
        complete: function() {
            $('#send-button').prop('disabled', false);
        }
    });
});

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('collapsed');
}
