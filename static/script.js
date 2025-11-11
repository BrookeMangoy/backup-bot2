// static/script.js

document.addEventListener("DOMContentLoaded", () => {
    // --- NAVEGACIÓN ENTRE VISTAS (HOMEPAGE / PRODUCTOS) ---
    const navLinks = document.querySelectorAll(".main-nav a[data-view], .logo-link[data-view]");
    const views = document.querySelectorAll(".view");

    navLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const targetViewId = link.getAttribute("data-view");
            const targetView = document.getElementById(targetViewId);

            // Quitar 'active' de todas las vistas
            views.forEach(view => view.classList.remove("active"));
            
            // Añadir 'active' a la vista objetivo
            if (targetView) {
                targetView.classList.add("active");
            }

            // Si es un link de scroll en la homepage
            if (link.getAttribute("data-scroll") === "true" && targetViewId === "homepage-view") {
                const targetSectionId = link.getAttribute("href");
                const targetSection = document.querySelector(targetSectionId);
                if (targetSection) {
                    targetSection.scrollIntoView({ behavior: "smooth" });
                }
            }
        });
    });

    // --- LÓGICA DEL CHATBOT ---
    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const closeBtn = document.querySelector(".chatbot .close-btn");
    const chatbox = document.querySelector(".chatbot .chatbox");
    const chatInput = document.querySelector(".chatbot .chat-input textarea");
    const sendChatBtn = document.querySelector(".chatbot .chat-input button[type='button']");
    const micBtn = document.getElementById("mic-btn");

    let userMessage = null;
    const API_URL = "http://localhost:8000/api/chat";
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'es-ES';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    let isListening = false;
    const createChatLi = (message, className) => {
        const chatLi = document.createElement("li");
        chatLi.classList.add("chat", `${className}`);
        let chatContent = className === "outgoing" 
            ? `<p>${message}</p>` 
            : `<span class="material-symbols-outlined">coffee</span><p>${message}</p>`;
        chatLi.innerHTML = chatContent;
        return chatLi;
    }

    const generateResponse = (incomingChatLi) => {
        const messageElement = incomingChatLi.querySelector("p");
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: userMessage,
                user_id: "web-user-123" 
            })
        }

        fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
            messageElement.textContent = data.reply;
        }).catch(() => {
            messageElement.classList.add("error");
            messageElement.textContent = "Lo siento, hubo un problema. ¿Podrías intentarlo de nuevo?";
        }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
    }

    const handleChat = () => {
        userMessage = chatInput.value.trim();
        if (!userMessage) return;

        chatInput.value = "";
        chatInput.style.height = "auto";

        chatbox.appendChild(createChatLi(userMessage, "outgoing"));
        chatbox.scrollTo(0, chatbox.scrollHeight);
        
        setTimeout(() => {
            const incomingChatLi = createChatLi("Escribiendo...", "incoming");
            chatbox.appendChild(incomingChatLi);
            chatbox.scrollTo(0, chatbox.scrollHeight);
            generateResponse(incomingChatLi);
        }, 600);
    }

    chatInput.addEventListener("input", () => {
        chatInput.style.height = "auto";
        chatInput.style.height = `${chatInput.scrollHeight}px`;
    });

    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleChat();
        }
    });

    sendChatBtn.addEventListener("click", handleChat);
    closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
    chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));

    micBtn.addEventListener('click', () => {
        if (isListening) {
            recognition.stop();
            isListening = false;
            micBtn.classList.remove('listening');
        } else {
            recognition.start();
            isListening = true;
            micBtn.classList.add('listening');
        }
    });

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        chatInput.value = transcript;
        isListening = false;
        micBtn.classList.remove('listening');
        handleChat();
    };

    recognition.onerror = (event) => {
        console.error("Error en reconocimiento de voz:", event.error);
        isListening = false;
        micBtn.classList.remove('listening');
        alert("Error en el micrófono: " + event.error);
    };

    recognition.onend = () => {
        isListening = false;
        micBtn.classList.remove('listening');
    };

    // --- LÓGICA DE LA PÁGINA DE PRODUCTOS ---
    const categoryLinks = document.querySelectorAll(".category-link");
    const productCards = document.querySelectorAll(".product-card-dash");
    const quantitySelectors = document.querySelectorAll(".quantity-selector");
    
    // Filtro de categorías
    categoryLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const category = link.getAttribute("data-category");

            categoryLinks.forEach(l => l.classList.remove("active"));
            link.classList.add("active");

            productCards.forEach(card => {
                if (category === "todos" || card.getAttribute("data-category") === category) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });
    });

    // Selectores de cantidad (+ / -)
    quantitySelectors.forEach(selector => {
        const minusBtn = selector.querySelector(".minus");
        const plusBtn = selector.querySelector(".plus");
        const valueSpan = selector.querySelector(".quantity-value");

        minusBtn.addEventListener("click", () => {
            let value = parseInt(valueSpan.textContent);
            if (value > 0) {
                value--;
                valueSpan.textContent = value;
            }
        });

        plusBtn.addEventListener("click", () => {
            let value = parseInt(valueSpan.textContent);
            value++;
            valueSpan.textContent = value;
        });
    });

    // --- LÓGICA DE CHECKOUT (FORMULARIO DE COMPRA) ---
    const comprarAhoraBtn = document.getElementById("comprar-ahora-btn");
    const checkoutFormContainer = document.getElementById("checkout-form-container");
    const orderSummaryList = document.getElementById("order-summary-list");
    const orderSummaryTotal = document.getElementById("order-summary-total");
    
    comprarAhoraBtn.addEventListener("click", () => {
        let totalAmount = 0;
        let totalQuantity = 0; // <--- ARREGLO 2: Variable para contar productos
        orderSummaryList.innerHTML = ""; // Limpiar resumen

        productCards.forEach(card => {
            const quantity = parseInt(card.querySelector(".quantity-value").textContent);
            
            totalQuantity += quantity; // <--- ARREGLO 2: Sumar cantidad total

            if (quantity > 0) {
                const name = card.querySelector("h4").textContent;
                
                // --- INICIO ARREGLO 1 (Error NaN) ---
                const priceString = card.querySelector(".price").textContent;
                // Limpiar el string del precio (quitar S/, $, y espacios)
                const cleanedPriceString = priceString.replace('S/', '').replace('$', '').trim();
                const price = parseFloat(cleanedPriceString); // Convertir el string limpio
                // --- FIN ARREGLO 1 ---

                if (!isNaN(price)) { // Verificar que el precio sea un número
                    totalAmount += price * quantity;

                    // Crear item en el resumen
                    const summaryItem = document.createElement("div");
                    summaryItem.classList.add("summary-item");
                    summaryItem.innerHTML = `
                        <span class="summary-item-name">${quantity}x ${name}</span>
                        <span class="summary-item-dots"></span>
                        <span class="summary-item-price">S/ ${(price * quantity).toFixed(2)}</span>
                    `;
                    orderSummaryList.appendChild(summaryItem);
                } else {
                    console.error("Error: El precio no es un número para el producto:", name);
                }
            }
        });

        // --- INICIO ARREGLO 2 (Evitar compra vacía) ---
        if (totalQuantity === 0) {
            alert("Tu carrito de compras está vacío. Añade productos antes de comprar.");
            checkoutFormContainer.classList.remove("active"); // Ocultar formulario si estaba abierto
            return; // No continuar
        }
        // --- FIN ARREGLO 2 ---

        // Mostrar total
        orderSummaryTotal.innerHTML = `
            <span>Total</span>
            <span>S/ ${totalAmount.toFixed(2)}</span>
        `;
        
        // Mostrar el formulario
        checkoutFormContainer.classList.add("active");
        comprarAhoraBtn.textContent = "Actualizar Compra";
    });


    // --- LÓGICA DE ENVÍO DE FORMULARIO Y MODAL ---
    const checkoutForm = document.getElementById("customer-checkout-form");
    const modal = document.getElementById("confirmation-modal");
    const modalCloseBtn = document.getElementById("modal-close-btn");
    const orderNumberEl = document.getElementById("order-number");

    checkoutForm.addEventListener("submit", (e) => {
        e.preventDefault();
        
        // Generar un número de orden falso
        const orderNumber = Math.floor(Math.random() * 90000) + 10000;
        orderNumberEl.textContent = `#${orderNumber}`;
        
        // Mostrar el modal
        modal.classList.add("active");
    });

    modalCloseBtn.addEventListener("click", () => {
        modal.classList.remove("active");
        
        // Resetear todo
        checkoutForm.reset();
        checkoutFormContainer.classList.remove("active");
        comprarAhoraBtn.textContent = "Comprar Ahora";
        
        // Resetear cantidades a 0
        quantitySelectors.forEach(selector => {
            const valueSpan = selector.querySelector(".quantity-value");
            valueSpan.textContent = "0";
        });
    });
});