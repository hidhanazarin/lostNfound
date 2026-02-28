const API = "http://127.0.0.1:8000";

async function addItem() {
  const formData = new FormData();

  formData.append("type", document.getElementById("type").value);
  formData.append("title", document.getElementById("title").value);
  formData.append("location", document.getElementById("location").value);
  formData.append("contact", document.getElementById("contact").value);
  formData.append("description", document.getElementById("description").value);
  formData.append("category", document.getElementById("category").value);

  const fileInput = document.getElementById("image");
  if (fileInput.files.length > 0) {
    formData.append("image", fileInput.files[0]);
  }

  await fetch(`${API}/add-item`, {
    method: "POST",
    body: formData,
  });

  fetchItems();
}

async function fetchItems() {
  const res = await fetch(`${API}/items`);
  const items = await res.json();

  const container = document.getElementById("items");
  container.innerHTML = "";

  items.forEach((item) => {
    container.innerHTML += `
      <div class="card">
        <h3>${item.title} (${item.type})</h3>
        <p>${item.description}</p>
        <p><strong>Category:</strong> ${item.category}</p>
        ${item.image_url ? `<img src="${item.image_url}" alt="Item Image" style="max-width: 200px;">` : ""}
        <button onclick="claimItem('${item.id}')">Claim</button>
      </div>
    `;
  });
}

async function claimItem(id) {
  await fetch(`${API}/delete-item/${id}`, { method: "DELETE" });
  fetchItems();
}

fetchItems();
