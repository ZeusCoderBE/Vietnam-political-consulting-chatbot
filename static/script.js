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
    messageContainer.style.display = 'flex'; // Flexbox for inline elements
    messageContainer.style.alignItems = 'center'; // Center vertically

    const textSpan = document.createElement('span');
    textSpan.innerHTML = "Đang suy nghĩ"; // Initial thinking text

    const dotsSpan = document.createElement('span');
    dotsSpan.style.marginLeft = '5px'; // Space between text and dots

    const timerSpan = document.createElement('span');
    timerSpan.style.marginLeft = '10px'; // Space between dots and timer
    timerSpan.style.fontSize = '12px';
    timerSpan.style.color = 'gray';
    timerSpan.innerHTML = "00:00"; // Initialize time

    // Add elements to message container
    messageContainer.appendChild(textSpan);
    messageContainer.appendChild(dotsSpan);
    messageContainer.appendChild(timerSpan);

    // Add elements to thinking message div
    thinkingMessageDiv.appendChild(avatarDiv);
    thinkingMessageDiv.appendChild(messageContainer);
    chatOutput.appendChild(thinkingMessageDiv);
    chatOutput.scrollTop = chatOutput.scrollHeight;

    // Update thinking dots immediately and every 100ms
    let dots = 0;
    const dotsSequence = [".", "..", "..."];
    function updateDots() {
        dotsSpan.innerHTML = dotsSequence[dots % 3]; // Cycle through dots
        dots++;
    }
    updateDots(); // Initial update for dots
    const dotsInterval = setInterval(updateDots, 100); // Update every 100ms

    // Timer effect
    let secondsElapsed = 0;
    const timerInterval = setInterval(function () {
        secondsElapsed++;
        const minutes = String(Math.floor(secondsElapsed / 60)).padStart(2, '0');
        const seconds = String(secondsElapsed % 60).padStart(2, '0');
        timerSpan.innerHTML = `${minutes}:${seconds}`;
    }, 1000); // Update timer every second
}


function formatLinks(text) {
    const linkPattern = /(https?:\/\/[a-zA-Z0-9.-]+(?:\/[^\s]*)?)/g;
    let formattedText = text.replace(linkPattern, function(match) {
        return `<a href="${match}" target="_blank" style="color: #1e90ff;">${match}</a>`;
    });
    formattedText = formattedText.replace(/\n/g, "<br>");
    return formattedText;
}
function check_response(text) {
    let message = text.result;
    if (message.includes("THÊM VÀO QDRANT")) {
        message = message.replace("THÊM VÀO QDRANT", "");
        text.result = message;
        return 1;
    }
    return 0; 
}
function displayBotMessage_Link(response) {
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
    const interval = setInterval(function () {
        if (message[i] === '<') {
            let tagEnd = message.indexOf('>', i);
            if (message.slice(i, tagEnd + 1).startsWith('<a')) {
                let closingTagEnd = message.indexOf('</a>', tagEnd);
                let linkHTML = message.slice(i, closingTagEnd + 4);
                messageContainer.innerHTML += linkHTML;

                // Tạo nút "Add"
                let button = $('<button>')
                    .addClass('add-link-button')
                    .data('link', linkHTML) // Gán dữ liệu vào nút
                    .append(
                        $('<img>')
                            .attr('src', 'https://kitudb.com/wp-content/uploads/2023/08/t-2-b-logo-transparent.png')
                            .attr('alt', 'Add Icon')
                            .css({ width: '20px', height: '20px' })
                    );

                $(messageContainer).append(button);

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
    }, 2);
    $(document).on('click', '.add-link-button', function () {
        // Lấy thẻ <a> đứng trước nút và lấy giá trị href
        const linkHTML = $(this).prev('a').attr('href'); // Hoặc sử dụng `.html()` nếu cần lấy nội dung thẻ <a>
    
        // Kiểm tra nếu linkHTML không phải là undefined
        if (linkHTML) {
            // Vô hiệu hóa tất cả các nút có class "add-link-button"
            $('.add-link-button').prop('disabled', true);
    
            $.ajax({
                url: '/add_links',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ link: linkHTML }),
                success: function (response) {
                    alert('Thêm thành công ' + linkHTML);
                },
                error: function (error) {
                    console.error('Error:', error);
                    alert('Thêm thất bại: ' + linkHTML);
                },
                complete: function () {
                    // Kích hoạt lại các nút sau khi request trả về
                    $('.add-link-button').prop('disabled', false);
                }
            });
        } else {
            console.error('Không tìm thấy liên kết.');
            alert('Không tìm thấy liên kết.');
        }
    });
    
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
    }, 2);  
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
        contentType: 'application/json', 
        data: JSON.stringify({ query: query }),
        success: function(response) {
            if (check_response(response) === 1) {
                displayBotMessage_Link(response); 
            } else {
                displayBotMessage(response);  
            }
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
