import React, { useEffect, useState } from 'react'
import logo from './logo.svg'
import './App.css'
import useSWR from 'swr'

function sqlFetcher(query: string) {
  query += ' format JSON'
  return fetch(`/db?query=${query}`).then(r => r.json())
}

function App() {
  const [count, setCount] = useState(0)
  const {data, error} = useSWR('select count(*) as count from r2', sqlFetcher)
  if (error) return <div>error</div>
  if (!data) return <div>loading</div>
  console.log('Data?', data)

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>{data.data[0].count} Rides</p>
        <p>
          <button type="button" onClick={() => setCount((count) => count + 1)}>
            count is: {count}
          </button>
        </p>
        <p>
          Edit <code>App.tsx</code> and save to test HMR updates.
        </p>
        <p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
          {' | '}
          <a
            className="App-link"
            href="https://vitejs.dev/guide/features.html"
            target="_blank"
            rel="noopener noreferrer"
          >
            Vite Docs
          </a>
        </p>
      </header>
    </div>
  )
}

export default App
