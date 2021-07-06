import React, { useEffect, useState } from 'react'
import './App.css'
import useSWR from 'swr'
import * as aq from 'arquero';

function sqlFetcher(query: string) {
  query += ' format JSON'
  return fetch(`/db?query=${query}`).then(r => r.json())
}

async function aqFetcher(query: string) {
  const url = `/db?query=${query} format Arrow`
  // @ts-ignore
  const dt = await aq.loadArrow(url);
  console.log(dt)
  debugger
  return {
    data: [
      {count: 99}
    ]
  }
}

function App() {
  const [count, setCount] = useState(0)
  const {data, error} = useSWR('select birth_year, count(*) as count from r2 where birth_year > 0 group by birth_year', aqFetcher)
  if (error) return <div>error</div>
  if (!data) return <div>loading</div>
  // console.log('Data?', data)

  return (
    <div className="App">
      <header className="App-header">
        <p>{data.data[0].count} Rides</p>
        <p>
          <button type="button" onClick={() => setCount((count) => count + 1)}>
            count is: {count}
          </button>
        </p>
      </header>
    </div>
  )
}

export default App
