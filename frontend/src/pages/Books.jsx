import { useEffect, useState } from "react";
import BookCard from "../components/BookCard";

export default function Books() {
  const [books, setBooks] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");

  async function loadBooks() {
    const params = new URLSearchParams();

    if (search) params.append("search", search);
    if (category) params.append("category", category);

    const response = await fetch(`/api/books?${params.toString()}`);
    const data = await response.json();
    setBooks(data);
  }

  useEffect(() => {
    loadBooks();
  }, [category]);

  function submitSearch(event) {
    event.preventDefault();
    loadBooks();
  }

  const categories = [
    "Fiction",
    "Self Help",
    "Programming",
    "Finance",
    "Fantasy"
  ];

  return (
    <section className="container page">
      <h1>Books</h1>

      <form className="search-bar" onSubmit={submitSearch}>
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by title or author"
        />

        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="">All Categories</option>
          {categories.map((item) => (
            <option key={item} value={item}>{item}</option>
          ))}
        </select>

        <button className="button" type="submit">
          Search
        </button>
      </form>

      <div className="book-grid">
        {books.length === 0 ? (
          <p>No books found.</p>
        ) : (
          books.map((book) => (
            <BookCard key={book.id} book={book} />
          ))
        )}
      </div>
    </section>
  );
}