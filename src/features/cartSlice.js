import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  items: {} // key -> { product, size, quantity, key }
}

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    addToCart: (state, action) => {
      const { product, size } = action.payload
      const key = `${product.id}-${size}`
      const entry = state.items[key]
      if(entry){ entry.quantity += 1 }
      else{ state.items[key] = { product, size, quantity: 1, key } }
    },
    removeFromCart: (state, action) => {
      const key = action.payload
      delete state.items[key]
    },
    decrement: (state, action) => {
      const key = action.payload
      const entry = state.items[key]
      if(!entry) return
      if(entry.quantity > 1) entry.quantity -= 1
      else delete state.items[key]
    },
    clearCart: (state)=>{ state.items = {} }
  }
})

export const { addToCart, removeFromCart, decrement, clearCart } = cartSlice.actions
export default cartSlice.reducer
