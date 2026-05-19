import React, { useEffect, useState } from 'react'

export default function Orders(){
  const [orders, setOrders] = useState([])

  useEffect(()=>{
    try{
      const raw = localStorage.getItem('orders')
      const parsed = raw ? JSON.parse(raw) : []
      setOrders(parsed)
    }catch(e){ setOrders([]) }
  }, [])

  if(orders.length === 0) return <div className="alert alert-info p-4">No orders yet.</div>

  return (
    <div>
      <h4 className="mb-3">Order History</h4>
      {orders.map(o=> (
        <div key={o.id} className="card mb-3">
          <div className="card-body">
            <div className="d-flex justify-content-between">
              <div>Order #{o.id}</div>
              <div>{new Date(o.date).toLocaleString()}</div>
            </div>
            <ul className="small mt-2 mb-2">
              {o.items.map(it=> (
                <li key={`${it.product.id}-${it.size}`}>{it.product.title} (Size: {it.size}) × {it.quantity} — ${(it.product.price * it.quantity).toFixed(2)}</li>
              ))}
            </ul>
            <div><strong>Total: ${o.total.toFixed(2)}</strong></div>
          </div>
        </div>
      ))}
    </div>
  )
}
