import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <section className="container page">
      <h1>Admin Dashboard</h1>
      <p>Manage the bookstore from here.</p>

      <div className="admin-grid">
        <Link className="admin-card" to="/admin/books">
          <h2>Manage Books</h2>
          <p>Add, edit and delete books.</p>
        </Link>

        <Link className="admin-card" to="/admin/books/add">
          <h2>Add Book</h2>
          <p>Add a new book to the store.</p>
        </Link>

        <Link className="admin-card" to="/admin/orders">
          <h2>Manage Orders</h2>
          <p>View and update customer orders.</p>
        </Link>
      </div>
    </section>
  );
}