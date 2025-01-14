import kate from '../../assets//Kate.jpg'
import kim from '../../assets/Kim.webp'
import beer from '../../assets/beer.png'
import "./index.css"

export const Advertising = () => {
    return (
        <section className="advertising">
            <figure className="sign">
                <img src={beer} width={200} alt="img" />
                <figcaption>Ain't no soft drink</figcaption>
            </figure>
            <figure className="sign">
                <img src={kate} width={200} alt="img" />
                <figcaption>Katyusha is 20 meters away from you and really wants to...</figcaption>
            </figure>
            <figure className="sign">
                <img src={kim} width={200} alt="img" />
                <figcaption>Kim Kardashian was treated for gout with this tool</figcaption>
            </figure>
        </section>
    )
}