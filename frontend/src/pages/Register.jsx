import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Register({ onLogin }) {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: ""
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
    setMessage("");

    const response = await fetch("/api/register", {
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

    onLogin(data.user);
    navigate("/");
  }

  return (
    <section className="form-page">
      <form className="form-card" onSubmit={submit}>
        <h1>Create Account</h1>

        <label>Name</label>
        <input
          name="name"
          value={form.name}
          onChange={change}
          required
        />

        <label>Email</label>
        <input
          name="email"
          type="email"
          value={form.email}
          onChange={change}
          required
        />

        <label>Password</label>
        <input
          name="password"
          type="password"
          value={form.password}
          onChange={change}
          required
        />

        {message && <p className="error">{message}</p>}

        <button className="button" type="submit">
          Register
        </button>

        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </section>
  );
}