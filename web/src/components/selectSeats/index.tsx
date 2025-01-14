import { useEffect, useState } from "react"
import { handleApi } from "../../services"
import { ISeats, ISelectSeats } from "../../types"
import "./index.css"

export const SelectSeats: React.FC<ISelectSeats> = ({ handleCreateTicket, url, userSeats }) => {
    const [values, setValues] = useState<ISeats[]>()
    const [loader, setLoader] = useState<boolean>(true)
    const [errorVal, setErrorVal] = useState<boolean>(false)

    useEffect(() => {
        (async function () {
            const apiData = await handleApi(url, "GET")
            apiData.seats.length = 50
            setValues(apiData.seats)
            setLoader(false)
        })()
    }, [])

    const getBookedSeats = () => {
        const seats = [...document.getElementsByClassName('seatNumber')] as HTMLInputElement[]
        const result = seats.filter((el) => el.checked).map((el) => +el.name)
        if (result.length < 1) {
            setErrorVal(true)
            setTimeout(() => setErrorVal(false), 3000)
        } else {
            handleCreateTicket({ "seats": result })
        }
    }

    return (
        <>
            <aside>
                {loader ? <h4>loading...</h4> :
                    <>
                        {
                            values && values.map((el, id) => {
                                return (
                                    <div key={id} className="seat">
                                        <label style={el.book_status != "available" ? {color: "red"} : {}} htmlFor={el.seat_number}>{el.seat_number}</label>
                                        <input disabled={!!userSeats || el.book_status != "available"} type="checkbox" className="seatNumber" name={el.seat_number} id={el.seat_number} />
                                    </div>
                                )
                            })
                        }
                    </>
                }
            </aside>
            <button disabled={!!userSeats} onClick={getBookedSeats}>Submit</button>
            {errorVal && <p className="errorMessage">Choose at least one seat</p>}
        </>
    )
}