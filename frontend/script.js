// Se o frontend for aberto direto do arquivo (file://), aponta para o backend
// local. Se for servido pelo próprio FastAPI, usa caminho relativo.
const API_URL =
  location.protocol === "file:" ? "http://localhost:8000/chat" : "/chat";

const form = document.getElementById("chat-form");
const input = document.getElementById("message");
const messages = document.getElementById("messages");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  const pending = addMessage("Pensando...", "bot");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();
    updateBotMessage(pending, data.answer, data.tool);
  } catch (error) {
    updateBotMessage(
      pending,
      "Não consegui falar com o servidor. Verifique se o backend está rodando.",
      null
    );
  }
});

// Cria uma bolha de mensagem e a adiciona ao chat. Retorna o elemento criado.
function addMessage(text, role) {
  const wrapper = document.createElement("div");
  wrapper.className = `message message--${role}`;

  const content = document.createElement("p");
  content.className = "message__text";
  content.textContent = text;

  wrapper.appendChild(content);
  messages.appendChild(wrapper);
  messages.scrollTop = messages.scrollHeight;

  return wrapper;
}

// Atualiza a bolha do bot com a resposta e o selo da ferramenta usada.
function updateBotMessage(element, text, tool) {
  element.querySelector(".message__text").textContent = text;

  if (tool) {
    const badge = document.createElement("span");
    const modifier = tool === "Calculadora" ? "calc" : "llm";
    badge.className = `message__badge message__badge--${modifier}`;
    badge.textContent = `Ferramenta usada: ${tool}`;
    element.appendChild(badge);
  }

  messages.scrollTop = messages.scrollHeight;
}
