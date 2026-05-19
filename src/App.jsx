import React, { useEffect, useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { fetchProducts, fetchCategories } from './features/productsSlice'
import Layout from './components/Layout'
import Home from './pages/Home'
import Cart from './components/Cart'
import Login from './components/Login'
import About from './pages/About'
import CategoryPage from './pages/CategoryPage'
import Orders from './pages/Orders'
import Checkout from './pages/Checkout'
import OrderConfirmation from './pages/OrderConfirmation'

export default function App(){
  const dispatch = useDispatch()
  const { status } = useSelector(s=>s.products)
  const [search,setSearch] = useState('')
  const [category,setCategory] = useState('')

  useEffect(()=>{
    if(status === 'idle') dispatch(fetchProducts())
    dispatch(fetchCategories())
  }, [status, dispatch])

  return (
    <Layout search={search} setSearch={setSearch} category={category} setCategory={setCategory}>
      <Routes>
        <Route path="/" element={<Home search={search} category={category} />} />
        <Route path="/about" element={<About />} />
        <Route path="/category/:name" element={<CategoryPage />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/checkout" element={<Checkout />} />
        <Route path="/orders" element={<Orders />} />
        <Route path="/order-confirmation" element={<OrderConfirmation />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Layout>
  )
}
