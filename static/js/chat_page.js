let timeoutID;
let timeout = 150;
var send_button;

function setup() {
    send_button = document.getElementById("send_button");
    send_button.addEventListener("click", new_message);
    timeoutID = window.setTimeout(messages, timeout);
}

window.addEventListener("load", setup);

// commits new message and displays it
function new_message(){
    const author = document.getElementById("author").value
    const message = document.getElementById("message").value

    fetch("/new_message/", {    // fetch runs new_message()
            method: "post",
            headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
            body: `author=${author}&message=${message}`
        })

        .then((response) => {
            return response.messages();
        })

        .catch(() => {
            console.log("error posting messages");
        });
}

// retrieves messages
function messages(){    // runs messages()
    fetch("/messages/")

    .then((response) => {
        return response.json();
    })

    .then(results => {
        let messages = "";
        for (let result of results) {
            messages += result.author + "\n" + result.message + "\n\n";
        }
        chat_window.value = messages;
    })

    .catch(() => {
        chat_window.value = "error retrieving messages from server";
    });

}

