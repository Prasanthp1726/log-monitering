import React from 'react'
import { useParams } from 'react-router-dom'
import ProductList from '../components/ProductList'

export default function CategoryPage(){
  const { name } = useParams()
  return (
    <div>
      <h4 className="mb-3">Category: {name}</h4>
      <ProductList search={''} category={name} />
    </div>
  )
}
