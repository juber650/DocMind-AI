const API_URL = `${API_BASE_URL}/ask`;
const API_BASE_URL = "https://docmind-ai-backend.onrender.com";

const welcome = document.getElementById("welcome");
const chat = document.getElementById("chat");
const input = document.getElementById("questionInput");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const newChatBtn = document.getElementById("newChatBtn");
const uploadNavBtn = document.getElementById("uploadNavBtn");
const uploadPanel = document.getElementById("uploadPanel");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");

function addMessage(role, text, sources = []) {
  welcome.style.display = "none";

  const wrapper = document.createElement("div");
  wrapper.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "You" : "D";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  if (sources.length && role === "assistant") {
    const sourceBox = document.createElement("div");
    sourceBox.className = "sources";
    sourceBox.textContent = "Sources: " + sources.join(" · ");
    bubble.appendChild(sourceBox);
  }

  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);

  chat.appendChild(wrapper);
  chat.scrollTop = chat.scrollHeight;
}

function addTyping() {
  const wrapper = document.createElement("div");
  wrapper.className = "message assistant";
  wrapper.id = "typingMessage";

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = "D";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  const typing = document.createElement("div");
  typing.className = "typing";
  typing.innerHTML = "<span></span><span></span><span></span>";

  bubble.appendChild(typing);
  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);

  chat.appendChild(wrapper);
  chat.scrollTop = chat.scrollHeight;
}

function removeTyping() {
  document.getElementById("typingMessage")?.remove();
}

/* ==========================================
   ASK QUESTION
========================================== */

async function askQuestion(question) {
  question = question.trim();

  if (!question) return;

  addMessage("user", question);

  input.value = "";
  input.style.height = "auto";

  sendBtn.disabled = true;

  addTyping();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question: question
      })
    });

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const data = await response.json();

    removeTyping();

    const answer =
      data.answer ||
      data.response ||
      data.result ||
      "No answer returned.";

    const sources =
      data.sources ||
      data.source ||
      [];

    addMessage(
      "assistant",
      answer,
      Array.isArray(sources)
        ? sources
        : [String(sources)]
    );

  } catch (error) {
    removeTyping();

    addMessage(
      "assistant",
      "I could not connect to the FastAPI backend. Make sure the backend is running."
    );

    console.error(error);

  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

/* ==========================================
   SEND BUTTON
========================================== */

sendBtn.addEventListener("click", () => {
  askQuestion(input.value);
});

/* ==========================================
   ENTER KEY
========================================== */

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    askQuestion(input.value);
  }
});

/* ==========================================
   AUTO RESIZE TEXTAREA
========================================== */

input.addEventListener("input", () => {
  input.style.height = "auto";

  input.style.height =
    Math.min(input.scrollHeight, 130) + "px";
});

/* ==========================================
   QUICK QUESTIONS
========================================== */

document
  .querySelectorAll(".quick-card")
  .forEach(card => {
    card.addEventListener("click", () => {
      input.value = card.dataset.question;
      input.focus();
    });
  });

/* ==========================================
   RESET CHAT
========================================== */

function resetChat() {
  chat.innerHTML = "";

  welcome.style.display = "block";

  input.value = "";
  input.style.height = "auto";
}

clearBtn.addEventListener("click", resetChat);
newChatBtn.addEventListener("click", resetChat);

/* ==========================================
   UPLOAD PANEL
========================================== */

uploadNavBtn.addEventListener("click", () => {
  uploadPanel.classList.toggle("show");
});

/* ==========================================
   PDF UPLOAD
========================================== */

fileInput.addEventListener("change", async () => {
  const file = fileInput.files[0];

  if (!file) return;

  /* Check PDF */
  if (
    file.type !== "application/pdf" &&
    !file.name.toLowerCase().endsWith(".pdf")
  ) {
    fileName.textContent = "Please select a PDF file.";
    return;
  }

  /* Show filename */
  fileName.textContent = "Uploading: " + file.name;
  uploadPanel.classList.add("show");
  fileInput.disabled = true;

  try {
    /* Create FormData */
    const formData = new FormData();
    formData.append("file", file);

    /* Upload PDF to FastAPI */
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: "POST",
      body: formData
    });

    /* Get backend response */
    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail ||
        `Upload failed (${response.status})`
      );
    }

    /* Successful upload */
    fileName.textContent = "✓ " + file.name + " uploaded successfully";

    addMessage(
      "assistant",
      `Document ready! ${data.filename} has been processed. ${data.pages} pages and ${data.chunks} chunks created. You can now ask questions about this document.`
    );

    input.focus();

  } catch (error) {
    console.error("Upload error:", error);
    fileName.textContent = "Upload failed";

    addMessage(
      "assistant",
      "I could not upload the PDF. Please make sure the FastAPI backend is running and try again."
    );

  } finally {
    fileInput.disabled = false;
  }
});