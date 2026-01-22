// 프론트팀 작업 파일
// 은어 사전

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("slangInput");
  const btn = document.getElementById("slangSearchBtn");

  const termEl = document.getElementById("slangTerm");
  const defEl = document.getElementById("slangDefinitions");
  const exEl = document.getElementById("slangExample");
  const relEl = document.getElementById("slangRelated");

  btn.addEventListener("click", async (e) => {
    e.preventDefault();

    const term = input.value.trim();
    if (!term) return;

    const res = await fetch("/api/slangSearch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ term })
    });

    const data = await res.json();

    termEl.textContent = `은어: ${data.term}`;

    defEl.innerHTML = "";
    data.definitions.forEach(d => {
      const li = document.createElement("li");
      li.textContent = d;
      defEl.appendChild(li);
    });

    exEl.textContent = `예문: ${data.example || "없음"}`;
    relEl.textContent =
      "유의어: " +
      (data.related_terms.length ? data.related_terms.join(", ") : "없음");
  });
});