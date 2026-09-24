import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

export default function OrderDetails() {
  const { id } = useParams();
  const [order, setOrder] = useState(null);

  useEffect(() => {
    fetch(`/api/orders/${id}`)
      .then((response) => response.json())
      .then((data) => setOrder(data));
  }, [id]);

  if (!order) {
    return <div className="loading">Loading order...</div>;
  }

  return (
    <section className="container page">
      <div className="order-header">
        <div>
          <h1>Order #{order.id}</h1>
          <p>Status: <strong>{order.status}</strong></p>
        </div>

        <h2>₹{Number(order.total_amount).toFixed(2)}</h2>
      </div>

      <div className="cart-list">
        {order.items.map((item, index) => (
          <div className="cart-item" key={index}>
            <img src={item.image} alt={item.title} />

            <div className="cart-info">
              <h3>{item.title}</h3>
              <p>{item.author}</p>
              <p>Quantity: {item.quantity}</p>
            </div>

            <strong>
              ₹{(Number(item.price) * item.quantity).toFixed(2)}
            </strong>
          </div>
        ))}
      </div>

      <Link className="back-link" to="/orders">
        ← Back to Orders
      </Link>
    </section>
  );
}