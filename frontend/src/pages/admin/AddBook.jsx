import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function AddBook() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    title: "",
    author: "",
    category: "",
    price: "",
    description: "",
    image: "",
    stock: ""
  });

  const [message, setMessage] = useState("");

  function change(event) {
    setForm({
      ...form,
      [event.target.name]: event.target.value
    });
  }

  async function submit(event) {
    event.preventDefault();

    const response = await fetch("/api/admin/books", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form)
    });

    const data = await response.json();

    if (!response.ok) {
      setMessage(data.message);
      return;
    }

    navigate("/admin/books");
  }

  return (
    <section className="form-page">
      <form className="form-card wide" onSubmit={submit}>
        <h1>Add Book</h1>

        <label>Title</label>
        <input name="title" value={form.title} onChange={change} required />

        <label>Author</label>
        <input name="author" value={form.author} onChange={change} required />

        <label>Category</label>
        <input name="category" value={form.category} onChange={change} required />

        <label>Price</label>
        <input
          name="price"
          type="number"
          step="0.01"
          value={form.price}
          onChange={change}
          required
        />

        <label>Stock</label>
        <input
          name="stock"
          type="number"
          min="0"
          value={form.stock}
          onChange={change}
          required
        />

        <label>Image URL</label>
        <input name="image" value={form.image} onChange={change} />

        <label>Description</label>
        <textarea
          name="description"
          rows="5"
          value={form.description}
          onChange={change}
        />

        {message && <p className="error">{message}</p>}

        <button className="button" type="submit">
          Add Book
        </button>
      </form>
    </section>
  );
}