import { IFooter } from "../../types"
import "./index.css"

export const Footer: React.FC<IFooter> = ({ userTicket, changeTime, setChangeTime, unbookSeats }) => {
    return (
        (userTicket?.seats && userTicket?.timeslots && !changeTime) ?
            <footer>
                <div className="ticket">
                    <h3>Your tickets: </h3>
                    <p>Name: {userTicket.userName}</p>
                    <p>City: {userTicket.city}</p>
                    <p>Film: {userTicket.film}</p>
                    <p>Cinema: {userTicket.cinemas}</p>
                    <p>Timeslot: {userTicket.timeslots}</p>
                    <p>Seats: {userTicket.seats.map((el, id) => <span key={id}>{el} </span>)}</p>
                </div>
                <div className="deleteBook">
                    <button onClick={unbookSeats}>Unbook seats</button>
                    <button onClick={() => { setChangeTime(prev => !prev) }}>Change time</button>
                </div>
            </footer>
            :
            <></>

    )
}