const chatBox = document.getElementById("chatbot-box");
const chatMessages = document.getElementById("chat-messages");
const imageInput = document.getElementById("imageInput");

/* ================= TOGGLE CHAT ================= */
function toggleChat() {
    chatBox.classList.toggle("show");
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


/* ================= ADD MESSAGE ================= */
function addMessage(content, sender = "bot", isImage = false) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender);

    if (isImage) {
        const img = document.createElement("img");
        img.src = content;
        img.style.maxWidth = "100%";
        img.style.borderRadius = "8px";
        msg.appendChild(img);
    } else {
        if (sender === "bot") {
            msg.innerHTML = content;
        } else {
            msg.innerText = content;
        }
    }

    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/* ================= SEND MESSAGE ================= */
async function sendMessage() {
    const file = imageInput.files[0];

    if (!file) {
        alert("Vui lòng chọn ảnh!");
        return;
    }

    const imageURL = URL.createObjectURL(file);
    addMessage(imageURL, "user", true);

    const loading = document.createElement("div");
    loading.classList.add("message", "bot");
    loading.innerText = "🤖 Đang xử lý...";
    chatMessages.appendChild(loading);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch("http://127.0.0.1:8000/chat-support/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            }
        });

        if (!response.ok) {
            throw new Error("API lỗi!");
        }

        const data = await response.json();
        loading.remove();

        addMessage(data.reply || "Không có phản hồi từ AI", "bot");

    } catch (error) {
        loading.remove();
        addMessage("❌ Không thể kết nối tới server!", "bot");
        console.error(error);
    }

    imageInput.value = "";
}
