import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { addToCart, removeFromCart, decrement, clearCart } from '../features/cartSlice'
import { useNavigate } from 'react-router-dom'

export default function Cart(){
  const items = useSelector(s=>s.cart.items)
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const entries = Object.values(items)
  const total = entries.reduce((s,e)=> s + e.product.price * e.quantity, 0)

  if(entries.length === 0) return <div className="p-4 alert alert-info">Your cart is empty</div>

  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">Your Cart</h5>
        <ul className="list-group mb-3">
          {entries.map(e=> (
            <li key={e.key} className="list-group-item d-flex justify-content-between align-items-center gap-3">
              <div className="d-flex align-items-center gap-3">
                <img src={e.product.image} alt={e.product.title} className="cart-item-image" />
                <div>
                  <strong style={{fontSize:14}}>{e.product.title}</strong>
                  <div className="small text-muted">Size: {e.size}</div>
                  <div className="small text-muted">${e.product.price} × {e.quantity}</div>
                </div>
              </div>
              <div className="d-flex align-items-center gap-2">
                <div className="input-group input-group-sm" style={{width:120}}>
                  <button className="btn btn-outline-secondary" onClick={()=>dispatch(decrement(e.key))} type="button">-</button>
                  <input type="text" readOnly className="form-control text-center" value={e.quantity} />
                  <button className="btn btn-outline-secondary" onClick={()=>dispatch(addToCart({ product: e.product, size: e.size }))} type="button">+</button>
                </div>
                <button className="btn btn-outline-danger btn-sm" onClick={()=>dispatch(removeFromCart(e.key))}>Remove</button>
              </div>
            </li>
          ))}
        </ul>
        <div className="d-flex justify-content-between align-items-center">
          <strong>Total:</strong>
          <div>${total.toFixed(2)}</div>
        </div>
        <div className="mt-3 d-flex gap-2 flex-wrap">
          <button className="btn btn-success" onClick={()=>navigate('/checkout')}>Proceed to Checkout</button>
          <button className="btn btn-outline-danger" onClick={()=>dispatch(clearCart())}>Clear</button>
        </div>
      </div>
    </div>
  )
}
