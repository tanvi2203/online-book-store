import { Link } from "react-router-dom";

export default function BookCard({ book }) {
  return (
    <div className="book-card">
      <img
        src={book.image}
        alt={book.title}
        className="book-image"
      />

      <div className="book-card-body">
        <p className="category">{book.category}</p>
        <h3>{book.title}</h3>
        <p className="author">by {book.author}</p>
        <p className="price">₹{Number(book.price).toFixed(2)}</p>

        <Link className="button" to={`/books/${book.id}`}>
          View Details
        </Link>
      </div>
    </div>
  );
}