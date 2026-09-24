import { useEffect, useState } from "react";
import { Link, Navigate, Route, Routes } from "react-router-dom";

import Home from "./pages/Home";
import Books from "./pages/Books";
import BookDetails from "./pages/BookDetails";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import Orders from "./pages/Orders";
import OrderDetails from "./pages/OrderDetails";
import Dashboard from "./pages/admin/Dashboard";
import ManageBooks from "./pages/admin/ManageBooks";
import AddBook from "./pages/admin/AddBook";
import ManageOrders from "./pages/admin/ManageOrders";


function ProtectedRoute({ user, children, adminOnly = false }) {
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (adminOnly && user.role !== "admin") {
    return <Navigate to="/" replace />;
  }

  return children;
}


function Navbar({ user, onLogout }) {
  return (
    <nav className="navbar">
      <div className="container nav-content">
        <Link className="logo" to="/">BookStore</Link>

        <div className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/books">Books</Link>

          {user && <Link to="/cart">Cart</Link>}
          {user && <Link to="/orders">My Orders</Link>}

          {user?.role === "admin" && (
            <Link to="/admin">Admin</Link>
          )}

          {!user ? (
            <>
              <Link to="/login">Login</Link>
              <Link className="button small" to="/register">Register</Link>
            </>
          ) : (
            <>
              <span className="welcome">Hi, {user.name}</span>
              <button className="button small" onClick={onLogout}>
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}


export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  async function loadUser() {
    try {
      const response = await fetch("/api/user");
      const data = await response.json();
      setUser(data.user);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadUser();
  }, []);

  async function logout() {
    await fetch("/api/logout", {
      method: "POST"
    });
    setUser(null);
  }

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <>
      <Navbar user={user} onLogout={logout} />

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/books" element={<Books />} />
          <Route path="/books/:id" element={<BookDetails user={user} />} />

          <Route
            path="/login"
            element={<Login onLogin={setUser} />}
          />

          <Route
            path="/register"
            element={<Register onLogin={setUser} />}
          />

          <Route
            path="/cart"
            element={
              <ProtectedRoute user={user}>
                <Cart />
              </ProtectedRoute>
            }
          />

          <Route
            path="/checkout"
            element={
              <ProtectedRoute user={user}>
                <Checkout />
              </ProtectedRoute>
            }
          />

          <Route
            path="/orders"
            element={
              <ProtectedRoute user={user}>
                <Orders />
              </ProtectedRoute>
            }
          />

          <Route
            path="/orders/:id"
            element={
              <ProtectedRoute user={user}>
                <OrderDetails />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin"
            element={
              <ProtectedRoute user={user} adminOnly>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin/books"
            element={
              <ProtectedRoute user={user} adminOnly>
                <ManageBooks />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin/books/add"
            element={
              <ProtectedRoute user={user} adminOnly>
                <AddBook />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin/orders"
            element={
              <ProtectedRoute user={user} adminOnly>
                <ManageOrders />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>

      <footer className="footer">
        <div className="container">
          <p>© 2026 Online Book Store</p>
        </div>
      </footer>
    </>
  );
}
