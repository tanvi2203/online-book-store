import { Link } from "react-router-dom";

export default function Home() {
  return (
    <section className="hero">
      <div className="container hero-content">
        <div>
          <p className="hero-label">ONLINE BOOK STORE</p>
          <h1>Find your next favorite book.</h1>
          <p>
            Browse books, discover new authors, add books to your cart
            and place your order online.
          </p>

          <Link className="button large" to="/books">
            Browse Books
          </Link>
        </div>
      </div>
    </section>
  );
}