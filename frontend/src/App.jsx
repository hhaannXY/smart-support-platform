import React, {useEffect, useState} from 'react'

export default function App(){
  const [tickets, setTickets] = useState([])

const API_BASE = import.meta.env.VITE_API_URL || '/api'
 
   useEffect(()=>{
     fetch(`${API_BASE}/tickets`)
       .then(r=>r.json())
       .then(setTickets)
       .catch(()=>{})
 
     const ws = new WebSocket((location.protocol === 'https:' ? 'wss://' : 'ws://') + location.hostname + ':8000/ws')
    ws.onmessage = (ev) => {
      try{
        const data = JSON.parse(ev.data)
        if(data.type === 'ticket_created'){
          setTickets(prev => [data.ticket, ...prev])
        }
      }catch(e){ }
    }
    return () => ws.close()
  },[])

const [newTicket, setNewTicket] = useState("")
 
   const handleSubmit = (event) => {
     event.preventDefault()
     if(!newTicket.trim()) return
     fetch(`${API_BASE}/tickets/submit`, {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ text: newTicket })
     })
       .then(r=>r.json())
       .then(data => {
         setTickets(prev => [data, ...prev])
         setNewTicket("")
       })
       .catch(()=>{})
   }
 
   return (
     <div style={{padding:20,fontFamily:'Arial'}}>
       <h1>Support Dashboard (Demo)</h1>
       <form onSubmit={handleSubmit} style={{marginBottom:20}}>
         <input
           value={newTicket}
           onChange={(e)=>setNewTicket(e.target.value)}
           placeholder="Введите текст заявки"
           style={{width:'60%', padding:8, marginRight:8}}
         />
         <button type="submit" style={{padding:'8px 16px'}}>Отправить</button>
       </form>
      <ul>
        {tickets.map(t=> (
          <li key={t.id}>{t.id}: {t.text} — {t.category}</li>
        ))}
      </ul>
    </div>
  )
}
