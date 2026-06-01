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
    const modifierByTool = {
      Calculadora: "calc",
      "Sobre o criador": "creator",
      LLM: "llm",
    };
    const modifier = modifierByTool[tool] || "llm";
    badge.className = `message__badge message__badge--${modifier}`;
    badge.textContent = `Ferramenta usada: ${tool}`;
    element.appendChild(badge);
  }

  messages.scrollTop = messages.scrollHeight;
}

// --- Modal de configurações --------------------------------------------------
// Apenas leitura: consulta /config/status para mostrar o provider e SE a chave
// está configurada no backend. A chave em si nunca trafega pelo frontend.
const CONFIG_URL =
  location.protocol === "file:"
    ? "http://localhost:8000/config/status"
    : "/config/status";

const settingsBtn = document.getElementById("settings-btn");
const settingsModal = document.getElementById("settings-modal");
const settingsClose = document.getElementById("settings-close");
const cfgProvider = document.getElementById("cfg-provider");
const cfgStatus = document.getElementById("cfg-status");

async function loadConfigStatus() {
  cfgStatus.textContent = "verificando…";
  cfgStatus.className = "status-pill";

  try {
    const response = await fetch(CONFIG_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();
    cfgProvider.textContent = data.provider;

    if (data.llm_configured) {
      cfgStatus.textContent = "Configurada";
      cfgStatus.classList.add("status-pill--ok");
    } else {
      cfgStatus.textContent = "Não configurada";
      cfgStatus.classList.add("status-pill--off");
    }
  } catch (error) {
    cfgProvider.textContent = "—";
    cfgStatus.textContent = "Erro ao consultar";
    cfgStatus.classList.add("status-pill--off");
  }
}

function openSettings() {
  settingsModal.hidden = false;
  loadConfigStatus();
}

function closeSettings() {
  settingsModal.hidden = true;
}

settingsBtn.addEventListener("click", openSettings);
settingsClose.addEventListener("click", closeSettings);

// Fecha ao clicar no fundo escuro (fora do card) ou ao apertar Esc.
settingsModal.addEventListener("click", (event) => {
  if (event.target === settingsModal) closeSettings();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !settingsModal.hidden) closeSettings();
});
