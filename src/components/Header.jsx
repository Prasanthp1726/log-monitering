import React from 'react'
import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import CategoryFilter from './CategoryFilter'
import SearchBox from './SearchBox'

export default function Header({ search, setSearch, category, setCategory }){
  const cartItems = useSelector(s=>s.cart.items)
  const count = Object.values(cartItems).reduce((s,i)=>s + i.quantity, 0)
  const navigate = useNavigate()

  const onCategoryChange = (val)=>{
    setCategory(val)
    if(val) navigate(`/category/${encodeURIComponent(val)}`)
    else navigate('/')
  }

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-white mb-4 shadow-sm rounded-4">
      <div className="container-fluid py-3">
        <Link className="navbar-brand fw-bold" to="/">E-Commerce</Link>
        <div className="d-flex flex-wrap align-items-center gap-2 ms-auto">
          <SearchBox value={search} onChange={setSearch} />
          <CategoryFilter selected={category} onChange={onCategoryChange} />
          <div className="d-flex flex-wrap gap-2 align-items-center">
            <NavLink to="/" className={({isActive})=> isActive? 'btn btn-outline-primary btn-sm':'btn btn-light btn-sm' }>Home</NavLink>
            <NavLink to="/about" className={({isActive})=> isActive? 'btn btn-outline-primary btn-sm':'btn btn-light btn-sm' }>About</NavLink>
            <NavLink to="/orders" className={({isActive})=> isActive? 'btn btn-outline-primary btn-sm':'btn btn-light btn-sm' }>Orders</NavLink>
            <Link to="/cart" className="btn btn-primary btn-sm">Cart ({count})</Link>
            <Link to="/login" className="btn btn-outline-secondary btn-sm">Login</Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
