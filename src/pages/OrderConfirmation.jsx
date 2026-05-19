import React from 'react'
import { Link, useLocation } from 'react-router-dom'

export default function OrderConfirmation(){
  const { state } = useLocation()
  const orderId = state?.orderId

  return (
    <div className="card shadow-sm border-0">
      <div className="card-body text-center p-5">
        <div className="mb-4 rounded-circle bg-success bg-opacity-10 d-inline-flex align-items-center justify-content-center" style={{width:80,height:80}}>
          <span className="fs-1 text-success">✓</span>
        </div>
        <h3 className="mb-3">Order Placed!</h3>
        <p className="text-muted mb-4">Thank you for your purchase. Your order has been successfully placed.</p>
        {orderId && <p className="fw-semibold">Order reference: <span className="text-primary">#{orderId}</span></p>}
        <div className="d-flex justify-content-center gap-3 mt-4">
          <Link to="/orders" className="btn btn-primary">View Orders</Link>
          <Link to="/" className="btn btn-outline-secondary">Continue Shopping</Link>
        </div>
      </div>
    </div>
  )
}
