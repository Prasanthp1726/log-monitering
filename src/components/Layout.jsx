import React from 'react'
import Header from './Header'
import Footer from './Footer'

export default function Layout({ search, setSearch, category, setCategory, children }){
  return (
    <>
      <Header search={search} setSearch={setSearch} category={category} setCategory={setCategory} />
      <main className="mb-5">
        <div className="container py-4">
          {children}
        </div>
      </main>
      <Footer />
    </>
  )
}
