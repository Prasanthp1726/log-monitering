import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import { addToCart } from '../features/cartSlice'
import { useNavigate } from 'react-router-dom'

const SIZES = ['S','M','L','XL','XXL']

export default function ProductCard({ product }){
  const [selectedSize, setSelectedSize] = useState('XL')
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const handleAddToCart = () => {
    dispatch(addToCart({ product, size: selectedSize }))
    navigate('/cart')
  }

  return (
    <div className="card h-100 shadow-sm">
      <div className="product-image-container">
        <img
          src={product.image}
          alt={product.title}
          className="product-image"
          onError={(e) => { e.target.onerror = null; e.target.src = 'https://via.placeholder.com/180x160?text=No+Image' }}
        />
      </div>
      <div className="card-body d-flex flex-column">
        <h6 className="card-title" style={{fontSize:14}}>{product.title}</h6>
        <p className="text-muted small mb-2">${product.price}</p>
        <div className="mb-3">
          <div className="text-muted small mb-2">Size:</div>
          <div className="btn-group btn-group-sm" role="group" aria-label="Select size">
            {SIZES.map(size => (
              <button
                key={size}
                type="button"
                className={`btn btn-outline-secondary ${selectedSize === size ? 'active bg-dark text-white' : ''}`}
                onClick={() => setSelectedSize(size)}
              >
                {size}
              </button>
            ))}
          </div>
        </div>
        <div className="mt-auto d-grid">
          <button className="btn btn-sm btn-primary" onClick={handleAddToCart}>Add to cart</button>
        </div>
      </div>
    </div>
  )
}
