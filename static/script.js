const toggleBtn = document.getElementById("toggleTheme");
const body = document.body;

// Carregar tema salvo
if (localStorage.getItem("theme") === "dark") {
  body.classList.add("dark-mode");
  toggleBtn.textContent = "☀️ Modo Claro";
}

// Alternar tema
toggleBtn.addEventListener("click", () => {
  body.classList.toggle("dark-mode");

  if (body.classList.contains("dark-mode")) {
    toggleBtn.textContent = "☀️ Modo Claro";
    localStorage.setItem("theme", "dark");
  } else {
    toggleBtn.textContent = "🌙 Modo Escuro";
    localStorage.setItem("theme", "light");
  }
});
