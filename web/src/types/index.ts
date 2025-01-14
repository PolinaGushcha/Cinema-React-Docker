export type IProps = {
    name: string
    id: string
}

export interface ITicketSelection {
    userTicket: ITicket
    changeTime: boolean
    handleCreateTicket: (obj: ITicket) => void
}

export type ITicket = {
    city?: string
    cityId?: string
    film?: string
    filmId?: string
    cinemas?: string
    cinemasId?: string
    timeslots?: string
    timeslotsId?: string
    seats?: number[]
    userName?: string
}

export type ISeats = {
    book_status: string
    seat_number: string
}

export interface ISelectValues {
    handleCreateTicket: (obj: ITicket) => void;
    url: string
    valueName: string
    changeTime?: boolean
}

export interface ISelectSeats extends ISelectValues {
    userName?: string
    userSeats?: number[]
}

export interface IFooter {
    userTicket: ITicket
    changeTime: boolean
    setChangeTime: React.Dispatch<React.SetStateAction<boolean>>
    unbookSeats: () => Promise<void>
}