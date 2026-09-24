import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

export default function BookDetails({ user }) {
  const { id } = useParams();
  const navigate = useNavigate();

  const [book, setBook] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch(`/api/books/${id}`)
      .then((response) => response.json())
      .then((data) => setBook(data));
  }, [id]);

  async function addToCart() {
    if (!user) {
      navigate("/login");
      return;
    }

    const response = await fetch("/api/cart", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        book_id: book.id,
        quantity: Number(quantity)
      })
    });

    const data = await response.json();
    setMessage(data.message);
  }

  if (!book) {
    return <div className="loading">Loading book...</div>;
  }

  return (
    <section className="container page">
      <div className="details-card">
        <img src={book.image} alt={book.title} />

        <div>
          <p className="category">{book.category}</p>
          <h1>{book.title}</h1>
          <h3>by {book.author}</h3>
          <p className="details-description">{book.description}</p>
          <p className="price">₹{Number(book.price).toFixed(2)}</p>
          <p>Available stock: {book.stock}</p>

          {book.stock > 0 && (
            <div className="quantity-row">
              <label>Quantity:</label>
              <input
                type="number"
                min="1"
                max={book.stock}
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
              />
            </div>
          )}

          <button
            className="button"
            disabled={book.stock === 0}
            onClick={addToCart}
          >
            {book.stock === 0 ? "Out of Stock" : "Add to Cart"}
          </button>

          {message && <p className="success">{message}</p>}

          <Link className="back-link" to="/books">
            ← Back to Books
          </Link>
        </div>
      </div>
    </section>
  );
}