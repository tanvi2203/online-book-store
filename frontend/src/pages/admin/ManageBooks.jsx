import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function ManageBooks() {
  const [books, setBooks] = useState([]);
  const [message, setMessage] = useState("");

  async function loadBooks() {
    const response = await fetch("/api/books");
    const data = await response.json();
    setBooks(data);
  }

  useEffect(() => {
    loadBooks();
  }, []);

  async function deleteBook(id) {
    if (!window.confirm("Delete this book?")) return;

    const response = await fetch(`/api/admin/books/${id}`, {
      method: "DELETE"
    });

    const data = await response.json();
    setMessage(data.message);

    if (response.ok) {
      loadBooks();
    }
  }

  return (
    <section className="container page">
      <div className="page-title-row">
        <h1>Manage Books</h1>
        <Link className="button" to="/admin/books/add">
          Add Book
        </Link>
      </div>

      {message && <p className="success">{message}</p>}

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Book</th>
              <th>Author</th>
              <th>Category</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {books.map((book) => (
              <tr key={book.id}>
                <td>{book.title}</td>
                <td>{book.author}</td>
                <td>{book.category}</td>
                <td>₹{Number(book.price).toFixed(2)}</td>
                <td>{book.stock}</td>
                <td>
                  <button
                    className="danger-button"
                    onClick={() => deleteBook(book.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}