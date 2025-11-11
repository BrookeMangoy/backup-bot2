// --- INICIO: CÓDIGO ORIGINAL DEL CHATBOT ---
const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector("#send-btn");
const micBtn = document.querySelector("#mic-btn");

// Hago una comprobación: si chatInput no existe (p.ej. en otra página), no dará error
const inputInitHeight = chatInput ? chatInput.scrollHeight : 0;

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
  // Comprobación de seguridad
  if (!chatInput) return; 
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

// Uso el operador 'optional chaining' (?) por si chatInput no existe
chatInput?.addEventListener("input", () => {
  chatInput.style.height = `${inputInitHeight}px`;
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput?.addEventListener("keydown", (e) => {
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
  // Comprobación de seguridad
  if (chatInput) {
    chatInput.value = messages[boxType] || 'Quisiera saber más sobre sus cajas';
  }
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
// --- FIN: CÓDIGO ORIGINAL DEL CHATBOT ---


// --- INICIO: NUEVA LÓGICA DE VISTAS (SPA) Y DASHBOARD ---
document.addEventListener('DOMContentLoaded', () => {

    // 1. Lógica de cambio de vistas
    const navLinks = document.querySelectorAll('.main-nav a[data-view], .logo-link[data-view]');
    const views = document.querySelectorAll('.view');

    if (navLinks.length > 0 && views.length > 0) {
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault(); // Previene el salto del href="#"
                
                const targetViewId = link.getAttribute('data-view');
                const targetView = document.getElementById(targetViewId);
                
                if (targetView) {
                    // Oculta todas las vistas
                    views.forEach(view => view.classList.remove('active'));
                    
                    // Muestra la vista objetivo
                    targetView.classList.add('active');

                    // Si el enlace también pide hacer scroll (ej. #cajas)
                    const shouldScroll = link.getAttribute('data-scroll') === 'true';
                    const href = link.getAttribute('href');
                    if (shouldScroll && href && href.startsWith('#')) {
                        const scrollTargetElement = document.getElementById(href.substring(1));
                        if (scrollTargetElement) {
                            scrollTargetElement.scrollIntoView({ behavior: 'smooth' });
                        }
                    } else {
                        // Si solo cambiamos de vista, vamos al tope de la página
                        window.scrollTo(0, 0);
                    }
                }
            });
        });
    }

    // 2. Lógica del dashboard de productos
    // AHORA BUSCA #productos-view, que es el ID de la vista
    const productDashboard = document.querySelector('#productos-view'); 
    
    if (productDashboard) {
        
        const sidebar = productDashboard.querySelector('.product-sidebar');
        const productGrid = productDashboard.querySelector('.product-grid');
        const productCards = productDashboard.querySelectorAll('.product-card-dash');

        // Manejador para los botones de cantidad (+/-)
        if (productGrid) {
            productGrid.addEventListener('click', (e) => {
                const target = e.target;
                
                if (target.classList.contains('plus')) {
                    const quantityValueElement = target.previousElementSibling;
                    let currentValue = parseInt(quantityValueElement.textContent, 10);
                    quantityValueElement.textContent = currentValue + 1;
                } else if (target.classList.contains('minus')) {
                    const quantityValueElement = target.nextElementSibling;
                    let currentValue = parseInt(quantityValueElement.textContent, 10);
                    if (currentValue > 0) {
                        quantityValueElement.textContent = currentValue - 1;
                    }
                }
            });
        }

        // Manejador para el filtro de categorías
        if (sidebar && productCards.length > 0) {
            sidebar.addEventListener('click', (e) => {
                e.preventDefault();
                const target = e.target;

                if (target.tagName === 'A') {
                    const category = target.getAttribute('data-category');
                    
                    sidebar.querySelectorAll('.category-link').forEach(a => a.classList.remove('active'));
                    target.classList.add('active');

                    productCards.forEach(card => {
                        const cardCategory = card.getAttribute('data-category');
                        if (category === 'todos' || cardCategory === category) {
                            card.style.display = 'block'; // Mostrar
                        } else {
                            card.style.display = 'none'; // Ocultar
                        }
                    });
                }
            });
        }

        // 3. Manejador para el botón "Comprar Ahora" y el formulario
        const comprarBtn = productDashboard.querySelector('#comprar-ahora-btn');
        const checkoutFormContainer = productDashboard.querySelector('#checkout-form-container');
        const orderListDiv = productDashboard.querySelector('#order-summary-list');
        const orderTotalDiv = productDashboard.querySelector('#order-summary-total');

        if (comprarBtn && checkoutFormContainer && orderListDiv && orderTotalDiv) {
            
            comprarBtn.addEventListener('click', () => {
                // 1. Limpiar el resumen anterior
                orderListDiv.innerHTML = '';
                let grandTotal = 0.0;
                let itemsSelected = 0;

                // 2. Recorrer todas las tarjetas de producto
                productCards.forEach(card => {
                    const quantityElement = card.querySelector('.quantity-value');
                    const quantity = parseInt(quantityElement.textContent, 10);

                    // Si se ha seleccionado al menos 1
                    if (quantity > 0) {
                        itemsSelected++;
                        
                        // Obtener datos del producto
                        const name = card.querySelector('h4').textContent;
                        const priceString = card.querySelector('.price').textContent;
                        // Limpiar precio (quitar $ y convertir a número)
                        const unitPrice = parseFloat(priceString.replace('$', ''));
                        
                        const lineTotal = unitPrice * quantity;
                        grandTotal += lineTotal;

                        // 3. Crear la línea del resumen con el formato solicitado
                        const itemDiv = document.createElement('div');
                        itemDiv.classList.add('summary-item');
                        
                        itemDiv.innerHTML = `
                            <span class="summary-item-name">${name} x ${quantity}</span>
                            <span class="summary-item-dots"></span>
                            <span class="summary-item-price">$${lineTotal.toFixed(2)}</span>
                        `;
                        orderListDiv.appendChild(itemDiv);
                    }
                });

                // 4. Mostrar el total
                if (itemsSelected > 0) {
                    orderTotalDiv.innerHTML = `
                        <span>TOTAL</span>
                        <span>$${grandTotal.toFixed(2)}</span>
                    `;
                } else {
                    // Si no hay productos, mostrar un mensaje
                    orderListDiv.innerHTML = '<p style="text-align:center; color: var(--coffee-medium);">No has seleccionado ningún producto.</p>';
                    orderTotalDiv.innerHTML = '';
                }

                // 5. Mostrar/Ocultar el formulario
                checkoutFormContainer.classList.toggle('active');

                // 6. Hacer scroll para que el formulario sea visible
                if (checkoutFormContainer.classList.contains('active')) {
                    checkoutFormContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            });
        }

        // 4. Manejador para el envío final del formulario (CON MODAL)
        const customerForm = productDashboard.querySelector('#customer-checkout-form');
        const confirmationModal = document.getElementById('confirmation-modal');
        const orderNumberSpan = document.getElementById('order-number');
        const modalCloseBtn = document.getElementById('modal-close-btn');

        if (customerForm && confirmationModal && orderNumberSpan && modalCloseBtn) {
            
            customerForm.addEventListener('submit', (e) => {
                e.preventDefault(); // Previene que el formulario recargue la página
                
                // 1. Validar que los campos requeridos estén llenos
                if (!customerForm.checkValidity()) {
                    customerForm.reportValidity(); // Muestra los avisos de "campo requerido"
                    return;
                }

                // 2. Generar número de pedido aleatorio (5 dígitos)
                const randomOrderNum = Math.floor(10000 + Math.random() * 90000);
                orderNumberSpan.textContent = `#${randomOrderNum}`;

                // 3. Mostrar el modal de confirmación
                confirmationModal.classList.add('active');

                // 4. Ocultar el formulario de checkout que se deslizó
                checkoutFormContainer.classList.remove('active');

                // 5. Resetear el formulario (borrar los datos del cliente)
                customerForm.reset();

                // 6. Resetear las cantidades de los productos a 0
                productCards.forEach(card => {
                    const quantityElement = card.querySelector('.quantity-value');
                    if (quantityElement) {
                        quantityElement.textContent = '0';
                    }
                });
            });

            // 7. Añadir listener al botón de cerrar el modal ("Entendido")
            modalCloseBtn.addEventListener('click', () => {
                confirmationModal.classList.remove('active');
            });
        }
    } // Cierre del if (productDashboard)
}); // Cierre del 'DOMContentLoaded'
// --- FIN: NUEVA LÓGICA ---