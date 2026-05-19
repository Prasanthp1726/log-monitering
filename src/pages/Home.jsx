import React from 'react'
import ProductList from '../components/ProductList'

export default function Home({ search, category }){
  return (
    <>
      <section className="bg-white rounded-4 shadow-sm p-4 mb-4">
        <div className="row align-items-center">
          <div className="col-md-7">
            <h2>Shop the latest products</h2>
            <p className="text-muted">Browse our curated store and discover top categories, deals, and featured items in a modern, responsive e-commerce interface.</p>
          </div>
          <div className="col-md-5 text-md-end">
            <div className="badge bg-primary text-white p-3 rounded-4">Fast shopping experience</div>
          </div>
        </div>
      </section>
      <ProductList search={search} category={category} />
    </>
  )
}
