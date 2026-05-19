import React from 'react'
import { useSelector } from 'react-redux'
import ProductCard from './ProductCard'

export default function ProductList({ search, category }){
  const { items, status } = useSelector(s=>s.products)

  const filtered = items.filter(p=>{
    if(category && p.category !== category) return false
    if(search && !p.title.toLowerCase().includes(search.toLowerCase())) return false
    return true
  })

  if(status === 'loading') return <div>Loading products...</div>

  return (
    <div className="row">
      {filtered.map(p=> (
        <div className="col-12 col-sm-6 col-md-4 col-lg-3 mb-4" key={p.id}>
          <ProductCard product={p} />
        </div>
      ))}
    </div>
  )
}
