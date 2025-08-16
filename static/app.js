document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("translate-form");
  const srcEl = document.getElementById("src");
  const spinner = document.getElementById("spinner");
  const resultContainer = document.getElementById("result-container");
  const output = document.getElementById("output");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = (srcEl.value || "").trim();
    if (!text) return;

    // Show spinner, hide old result
    spinner.style.display = "inline-block";
    resultContainer.style.display = "none";
    output.textContent = "";

    try {
      const res = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });

      const data = await res.json();
      if (!res.ok) {
        output.textContent = data?.error || "Translation failed";
      } else {
        output.textContent = data?.translation || "";
      }
      resultContainer.style.display = "block";
    } catch (err) {
      output.textContent = "Error contacting server";
      resultContainer.style.display = "block";
    } finally {
      spinner.style.display = "none";
    }
  });
});
