import React from 'react'

export default function SearchBox({ value, onChange }){
  return (
    <input className="form-control" style={{minWidth:200}} placeholder="Search products..." value={value} onChange={e=>onChange(e.target.value)} />
  )
}
