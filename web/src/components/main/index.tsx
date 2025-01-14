import { useRef } from "react";
import { SelectSeats } from "../selectSeats"
import { SelectValues } from "../selectValues"
import { ITicketSelection } from "../../types";
import "./index.css"

export const TicketSelection: React.FC<ITicketSelection> = ({ userTicket, changeTime, handleCreateTicket }) => {
    const ref = useRef<HTMLInputElement>(null);

    return (
        <section className="infoContainer">
            <h3>Enter your name</h3>
            {!userTicket?.userName ?
                <>
                    <input ref={ref} type="text" id="userName" />
                    <button onClick={() => ref.current ? handleCreateTicket({ userName: ref.current.value }) : console.log("Invalid value")}>OK</button>
                </>
                :
                <>
                    <p>{userTicket.userName}</p>
                    <h3>Choose your city</h3>
                    <SelectValues valueName="city" handleCreateTicket={handleCreateTicket} url={import.meta.env.VITE_RESOURCE_GET_CITIES} />
                </>
            }
            {userTicket?.cityId && <>
                <h3>Choose a film</h3>
                <SelectValues valueName="film" handleCreateTicket={handleCreateTicket} url={import.meta.env.VITE_RESOURCE_GET_FILMS_BY_CITY + `?city_id=${userTicket.cityId}`} />
            </>}
            {userTicket?.filmId && <>
                <h3>Choose cinema</h3>
                <SelectValues valueName="cinemas" handleCreateTicket={handleCreateTicket} url={import.meta.env.VITE_RESOURCE_GET_CINEMAS_BY_FILM + `?city_id=${userTicket.cityId}&film_id=${userTicket.filmId}`} />
            </>}
            {userTicket?.cinemasId && <>
                <h3>Choose a time</h3>
                <SelectValues valueName="timeslots" handleCreateTicket={handleCreateTicket} changeTime={changeTime} url={import.meta.env.VITE_RESOURCE_GET_TIMESLOTS + `?cinema_id=${userTicket.cinemasId}&film_id=${userTicket.filmId}`} />
            </>}
            {userTicket?.timeslots && <>
                <h3>Choose seats</h3>
                <SelectSeats valueName="seats" handleCreateTicket={handleCreateTicket} userName={userTicket.userName} userSeats={userTicket?.seats} url={import.meta.env.VITE_RESOURCE_GET_SEATS + `?cinema_id=${userTicket.cinemasId}&film_id=${userTicket.filmId}&time=${userTicket.timeslots}`} />
            </>}
        </section>
    )
}