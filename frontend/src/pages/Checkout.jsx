import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Checkout() {
  const navigate = useNavigate();
  const [message, setMessage] = useState("");

  async function placeOrder() {
    setMessage("");

    const response = await fetch("/api/orders", {
      method: "POST"
    });

    const data = await response.json();

    if (!response.ok) {
      setMessage(data.message);
      return;
    }

    navigate(`/orders/${data.order_id}`);
  }

  return (
    <section className="form-page">
      <div className="form-card">
        <h1>Checkout</h1>

        <p>
          This student project uses a simple checkout flow.
          No real payment is processed.
        </p>

        {message && <p className="error">{message}</p>}

        <button className="button" onClick={placeOrder}>
          Place Order
        </button>
      </div>
    </section>
  );
}