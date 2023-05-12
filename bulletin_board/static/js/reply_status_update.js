acceptButtons = document.getElementsByClassName("accept-reply")
rejectButtons = document.getElementsByClassName("reject-reply")
replyCards = document.getElementsByClassName("reply-card")

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
  }


for (let i = 0; i < acceptButtons.length; i++) {
    acceptButtons[i].addEventListener("click", function() {
        reply = replyCards[i]
        let xhr = new XMLHttpRequest();
        const pk = this.getAttribute("reply-pk");
        xhr.open("POST", '/api/reply_accept/' + pk + '/', true);
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function() {
            
            if (xhr.readyState === 4 && xhr.status === 200) {
                let response = JSON.parse(xhr.responseText);
                console.log(response);
                if (response.success) {
                    alert('Отклик принят! Сообщение пользователю отправлено.')
                    reply.remove()
                }
                else {
                    alert('Что-то пошло не так. Попробуйте попозже.')
                }
            }
        };

        xhr.send()

    });

    rejectButtons[i].addEventListener("click", function() { 
        reply = replyCards[i]
        let xhr = new XMLHttpRequest();
        const pk = this.getAttribute("reply-pk");
        xhr.open("POST", '/api/reply_reject/' + pk + '/', true);
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function() {
            
            if (xhr.readyState === 4 && xhr.status === 200) {
                let response = JSON.parse(xhr.responseText);
                if (response.success) {
                    alert('Отклик отклонен!')
                    reply.remove()
                }
                else {
                    alert('Что-то пошло не так. Попробуйте попозже.')
                }
            }
        };

        xhr.send()
    });

}

// for (let i = 0; i < rejectButtons.length; i++) {


// }