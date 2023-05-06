const replyButton = document.getElementById('reply-button')

let cancelReplyButton = document.getElementById('cancel-reply-button');

replyButton.addEventListener('click', function() {
    let replyForm = document.getElementById('reply-form');

    replyForm.style.display = 'block';
    // cancelReplyButton = document.getElementById('cancel-reply-button')

});

cancelReplyButton.addEventListener('click', function() {
    let replyForm = document.getElementById('reply-form');
    replyForm.style.display = 'none';
});