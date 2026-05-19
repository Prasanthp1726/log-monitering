import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { clearCart } from '../features/cartSlice'
import { useNavigate } from 'react-router-dom'

export default function Checkout(){
  const items = useSelector(s=>Object.values(s.cart.items))
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const total = items.reduce((sum, item) => sum + item.product.price * item.quantity, 0)

  const handlePlaceOrder = () => {
    const order = {
      id: Date.now(),
      date: new Date().toISOString(),
      items,
      total
    }
    try {
      const raw = localStorage.getItem('orders')
      const arr = raw ? JSON.parse(raw) : []
      arr.unshift(order)
      localStorage.setItem('orders', JSON.stringify(arr))
      dispatch(clearCart())
      navigate('/order-confirmation', { state: { orderId: order.id } })
    } catch (error) {
      console.error(error)
      alert('Unable to place your order. Please try again.')
    }
  }

  if(items.length === 0) {
    return <div className="alert alert-info p-4">Your cart is empty. Add products to proceed to checkout.</div>
  }

  return (
    <div className="card shadow-sm">
      <div className="card-body">
        <h4 className="card-title">Checkout</h4>
        <div className="row">
          <div className="col-lg-8">
            <div className="list-group mb-4">
              {items.map(item => (
                <div key={`${item.product.id}-${item.size}`} className="list-group-item d-flex justify-content-between align-items-center gap-3">
                  <div className="d-flex align-items-center gap-3">
                    <img src={item.product.image} alt={item.product.title} className="cart-item-image" />
                    <div>
                      <div className="fw-semibold">{item.product.title}</div>
                      <div className="text-muted small">Size: {item.size}</div>
                      <div className="text-muted small">Quantity: {item.quantity}</div>
                    </div>
                  </div>
                  <div>${(item.product.price * item.quantity).toFixed(2)}</div>
                </div>
              ))}
            </div>
          </div>
          <div className="col-lg-4">
            <div className="p-4 bg-light rounded-3">
              <h5>Total</h5>
              <div className="fs-4 fw-bold mb-3">${total.toFixed(2)}</div>
              <button className="btn btn-success w-100" onClick={handlePlaceOrder}>Place order</button>
              <button className="btn btn-secondary w-100 mt-2" onClick={()=>navigate('/cart')}>Back to Cart</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
