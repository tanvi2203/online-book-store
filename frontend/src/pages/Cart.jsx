import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function Cart() {
  const [cart, setCart] = useState({
    items: [],
    total: 0
  });

  const [message, setMessage] = useState("");

  async function loadCart() {
    const response = await fetch("/api/cart");
    const data = await response.json();

    if (response.ok) {
      setCart(data);
    }
  }

  useEffect(() => {
    loadCart();
  }, []);

  async function updateItem(id, quantity) {
    const response = await fetch(`/api/cart/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ quantity: Number(quantity) })
    });

    const data = await response.json();
    setMessage(data.message);

    if (response.ok) {
      loadCart();
    }
  }

  async function removeItem(id) {
    const response = await fetch(`/api/cart/${id}`, {
      method: "DELETE"
    });

    const data = await response.json();
    setMessage(data.message);
    loadCart();
  }

  return (
    <section className="container page">
      <h1>Your Cart</h1>

      {message && <p className="success">{message}</p>}

      {cart.items.length === 0 ? (
        <div className="empty-box">
          <p>Your cart is empty.</p>
          <Link className="button" to="/books">Browse Books</Link>
        </div>
      ) : (
        <>
          <div className="cart-list">
            {cart.items.map((item) => (
              <div className="cart-item" key={item.id}>
                <img src={item.image} alt={item.title} />

                <div className="cart-info">
                  <h3>{item.title}</h3>
                  <p>{item.author}</p>
                  <p>₹{Number(item.price).toFixed(2)}</p>

                  <input
                    type="number"
                    min="1"
                    max={item.stock}
                    value={item.quantity}
                    onChange={(e) =>
                      updateItem(item.id, e.target.value)
                    }
                  />

                  <button
                    className="danger-button"
                    onClick={() => removeItem(item.id)}
                  >
                    Remove
                  </button>
                </div>

                <strong>
                  ₹{Number(item.subtotal).toFixed(2)}
                </strong>
              </div>
            ))}
          </div>

          <div className="cart-total">
            <h2>Total: ₹{Number(cart.total).toFixed(2)}</h2>
            <Link className="button large" to="/checkout">
              Proceed to Checkout
            </Link>
          </div>
        </>
      )}
    </section>
  );
}