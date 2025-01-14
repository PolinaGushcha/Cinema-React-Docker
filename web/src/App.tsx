import { useState } from 'react'
import './App.css'
import { ITicket } from './types/index.ts'
import { Advertising } from './components/advertising/index.tsx';
import { Header } from './components/header/index.tsx';
import { TicketSelection } from './components/main/index.tsx';
import { Footer } from './components/footer/index.tsx';
import { handleApi } from './services/index.ts';

function App() {
  const [userTicket, setUserTiket] = useState<ITicket>({});
  const [changeTime, setChangeTime] = useState<boolean>(false);

  const handleCreateTicket = async (obj: ITicket) => {
    setChangeTime(!!obj.cinemas);
    if (changeTime && obj?.timeslots && userTicket.seats) {
      userTicket && handleApi(import.meta.env.VITE_RESOURCE_CHANGE_TIME + `?user_name=${encodeURIComponent(userTicket.userName || "")}&cinema_id=${userTicket.cinemasId}&film_id=${userTicket.filmId}&old_time=${encodeURIComponent(userTicket.timeslots || "")}&new_time=${encodeURIComponent(obj.timeslots || "")}`, "POST", [Number(obj.timeslotsId)])
      const ticket = { ...userTicket }
      ticket.timeslots = obj.timeslots
      ticket.timeslotsId = obj.timeslotsId
      setUserTiket(ticket);
    } else if (!userTicket) {
      setUserTiket(obj);
    } else {
      setUserTiket(prev => Object.assign(obj, prev));
      obj?.seats && handleApi(import.meta.env.VITE_RESOURCE_BOOK_SEATS + `?user_name=${encodeURIComponent(userTicket.userName || "")}&cinema_id=${userTicket.cinemasId}&film_id=${userTicket.filmId}&time=${encodeURIComponent(userTicket.timeslots || "")}`, "POST", obj.seats)
    }
  }

  const handleUnbookSeats = async () => {
    userTicket?.seats && await handleApi(import.meta.env.VITE_RESOURCE_UNBOOK_SEATS + `?user_name=${encodeURIComponent(userTicket.userName || "")}&cinema_id=${userTicket.cinemasId}&film_id=${userTicket.filmId}&time=${encodeURIComponent(userTicket.timeslots || "")}`, "POST", userTicket.seats)
    const obj = { ...userTicket }
    delete obj?.seats
    setUserTiket(obj);
  }

  return (
    <>
      <Header />
      <main>
        <Advertising />
        <TicketSelection userTicket={userTicket} changeTime={changeTime} handleCreateTicket={handleCreateTicket} />
        <Advertising />
      </main>
      <Footer userTicket={userTicket} changeTime={changeTime} setChangeTime={setChangeTime} unbookSeats={handleUnbookSeats} />
    </>
  )
}

export default App
