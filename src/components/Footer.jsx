import React from 'react'

export default function Footer(){
  return (
    <footer className="bg-white py-5 border-top">
      <div className="container">
        <div className="row gy-4">
          <div className="col-md-4">
            <div className="footer-card p-4 h-100 rounded-4 shadow-sm">
              <h6 className="text-uppercase mb-3">New</h6>
              <ul className="list-unstyled footer-links">
                <li>Flower Program</li>
                <li>New</li>
                <li>Seasonal</li>
                <li>FAQ</li>
                <li>About Us</li>
                <li>Contact Us</li>
              </ul>
            </div>
          </div>
          <div className="col-md-4">
            <div className="footer-card p-4 h-100 rounded-4 shadow-sm">
              <h6 className="text-uppercase mb-3">All Products</h6>
              <ul className="list-unstyled footer-links">
                <li>All products</li>
                <li>Ground Arrangement</li>
                <li>Cremation Vase</li>
                <li>Monument</li>
                <li>Large Potted Silk</li>
                <li>Print Friendly Catalog</li>
              </ul>
            </div>
          </div>
          <div className="col-md-4">
            <div className="footer-card p-4 h-100 rounded-4 shadow-sm">
              <h6 className="text-uppercase mb-3">Contact Info</h6>
              <p className="mb-2 text-muted">PO BOX 1533 Marietta, GA 30061</p>
              <p className="mb-2 text-muted">(770) 428 - 8883</p>
              <p className="mb-2 text-muted">(770) 422-4720</p>
              <p className="mb-0 text-muted">879 Industrial Park Dr Marietta, GA 30062</p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
