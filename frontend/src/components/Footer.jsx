import React from 'react';
import './Footer.css';

export default function Footer({ page, setPage, hasNext, hasPrev }) {
  return (
    <footer className="footer">
      <div className="pagination">
        <button onClick={() => setPage(page - 1)} disabled={page === 1 || !hasPrev}>
          Previous
        </button>
        <span>Page {page}</span>
        <button onClick={() => setPage(page + 1)} disabled={!hasNext}>
          Next
        </button>
      </div>
    </footer>
  );
} 