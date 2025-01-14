import logo from '../../assets/logo.png'
import "./index.css"

export const Header = () => {
    return (
        <header>
            <img src={logo} width={90} alt="logo" />
            <div className='cinemaName'>
                <h1>ORK cinema</h1>
                <p>The best cinema ever!</p>
            </div>
        </header>
    )
}