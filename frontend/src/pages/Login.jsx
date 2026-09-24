import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Login({ onLogin }) {
  const navigate = useNavigate();

  const [form, setForm] = useState({
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

    const response = await fetch("/api/login", {
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
    navigate(data.user.role === "admin" ? "/admin" : "/");
  }

  return (
    <section className="form-page">
      <form className="form-card" onSubmit={submit}>
        <h1>Login</h1>

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
          Login
        </button>

        <p>
          Don't have an account? <Link to="/register">Register</Link>
        </p>
      </form>
    </section>
  );
}