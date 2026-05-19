import React, { useState } from 'react'

export default function Login(){
  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')
  const [loading,setLoading]=useState(false)
  const [error,setError]=useState('')
  const [success,setSuccess]=useState('')

  const validate = ()=>{
    if(!email) return 'Email is required'
    if(!/^\S+@\S+\.\S+$/.test(email)) return 'Enter a valid email'
    if(password.length < 6) return 'Password must be at least 6 characters'
    return ''
  }

  const handleSubmit = (e)=>{
    e.preventDefault()
    setError(''); setSuccess('')
    const v = validate()
    if(v){ setError(v); return }
    setLoading(true)
    setTimeout(()=>{
      setLoading(false)
      if(email === 'user@example.com' && password === 'password'){
        setSuccess('Login successful — welcome back!')
      }else{
        setError('Invalid credentials (try user@example.com / password)')
      }
    }, 900)
  }

  return (
    <div className="row justify-content-center">
      <div className="col-md-6 col-lg-5">
        <div className="card shadow-sm">
          <div className="card-body p-4">
            <h4 className="card-title mb-3">Sign in</h4>
            {error && <div className="alert alert-danger">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}
            <form onSubmit={handleSubmit} noValidate>
              <div className="mb-3">
                <label className="form-label">Email</label>
                <input type="email" className="form-control" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com" />
              </div>
              <div className="mb-3">
                <label className="form-label">Password</label>
                <input type="password" className="form-control" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Enter password" />
              </div>
              <div className="d-grid">
                <button className="btn btn-primary" disabled={loading}>
                  {loading ? 'Signing in...' : 'Sign In'}
                </button>
              </div>
            </form>
            <hr/>
            <p className="small text-muted mb-0">Demo: use user@example.com / password</p>
          </div>
        </div>
      </div>
    </div>
  )
}
