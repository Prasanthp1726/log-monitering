import React from 'react'
import { useSelector } from 'react-redux'

export default function CategoryFilter({ selected, onChange }){
  const categories = useSelector(s=>s.products.categories)
  return (
    <select className="form-select" style={{width:180}} value={selected} onChange={e=>onChange(e.target.value)}>
      <option value="">All categories</option>
      {categories.map(c=> <option key={c} value={c}>{c}</option>)}
    </select>
  )
}
