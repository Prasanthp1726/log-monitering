import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axios from 'axios'

export const fetchProducts = createAsyncThunk('products/fetchProducts', async () => {
  const res = await axios.get('https://fakestoreapi.com/products')
  return res.data
})

export const fetchCategories = createAsyncThunk('products/fetchCategories', async () => {
  const res = await axios.get('https://fakestoreapi.com/products/categories')
  return res.data
})

const productsSlice = createSlice({
  name: 'products',
  initialState: { items: [], status: 'idle', error: null, categories: [] },
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(fetchProducts.pending, (state) => { state.status = 'loading' })
      .addCase(fetchProducts.fulfilled, (state, action) => { state.status = 'succeeded'; state.items = action.payload })
      .addCase(fetchProducts.rejected, (state, action) => { state.status = 'failed'; state.error = action.error.message })
      .addCase(fetchCategories.fulfilled, (state, action) => { state.categories = action.payload })
  }
})

export default productsSlice.reducer
