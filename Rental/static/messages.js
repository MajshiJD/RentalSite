document.addEventListener('DOMContentLoaded', function () {
    var messages = document.querySelector('.messages');

    if (messages) {
        var messageList = messages.querySelectorAll('li');

        messageList.forEach(function (message) {
            setTimeout(function () {
                message.classList.add('hidden');
            }, 3000); // Adjust the timeout (milliseconds) based on your preference
        });
    }
});