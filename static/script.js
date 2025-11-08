
const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector("#send-btn");
const micBtn = document.querySelector("#mic-btn");
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", className);
  const icon = className === "outgoing" 
    ? "" 
    : '<span class="material-symbols-outlined">smart_toy</span>';
  chatLi.innerHTML = `${icon}<p></p>`;
  chatLi.querySelector("p").textContent = message;
  return chatLi;
};

const handleChat = async () => {
  const userMessage = chatInput.value.trim();
  if (!userMessage) return;

  chatInput.value = "";
  chatInput.style.height = `${inputInitHeight}px`;
  chatbox.appendChild(createChatLi(userMessage, "outgoing"));
  chatbox.scrollTo(0, chatbox.scrollHeight);

  const thinkingLi = createChatLi("Mocca está pensando... ☕", "incoming");
  chatbox.appendChild(thinkingLi);
  chatbox.scrollTo(0, chatbox.scrollHeight);

  const user_id = localStorage.getItem("user_id") || Math.random().toString(36).substr(2, 9);
  localStorage.setItem("user_id", user_id);

  setTimeout(async () => {
    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage, user_id })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const data = await response.json();
      chatbox.removeChild(thinkingLi);
      chatbox.appendChild(createChatLi(data.reply || "Ups... algo pasó.", "incoming"));
    } catch (error) {
      chatbox.removeChild(thinkingLi);
      chatbox.appendChild(createChatLi("Lo siento, hubo un problema. ¿Podrías intentarlo de nuevo?", "incoming"));
    }
    chatbox.scrollTo(0, chatbox.scrollHeight);
  }, 1500);
};

chatInput.addEventListener("input", () => {
  chatInput.style.height = `${inputInitHeight}px`;
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();
    handleChat();
  }
});

sendChatBtn?.addEventListener("click", handleChat);
closeBtn?.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler?.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));

function selectBox(boxType) {
  document.body.classList.add('show-chatbot');
  const messages = {
    cafe: "Me interesa la Caja Origen Café",
    chocolate: "Me interesa la Caja Origen Chocolate",
    dual: "Me interesa la Caja Experiencia Dual"
  };
  chatInput.value = messages[boxType] || 'Quisiera saber más sobre sus cajas';
  setTimeout(handleChat, 300);
}

let recognition = null;

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'es-ES';

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript.trim();
    if (transcript) {
      chatInput.value = transcript;
      micBtn?.classList.remove("listening");
      handleChat();
    }
  };

  recognition.onerror = () => {
    micBtn?.classList.remove("listening");
    chatbox.appendChild(createChatLi("Lo siento, no pude entenderte. ¿Puedes intentarlo de nuevo?", "incoming"));
    chatbox.scrollTo(0, chatbox.scrollHeight);
  };

  recognition.onend = () => {
    micBtn?.classList.remove("listening");
  };
} else {
  micBtn?.remove(); 
}

micBtn?.addEventListener("click", () => {
  if (!recognition) return;
  chatInput.value = "";
  micBtn.classList.add("listening");
  recognition.start();
});