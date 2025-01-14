import { useEffect, useState } from "react"
import { handleApi } from "../../services"
import { IProps, ISelectValues } from "../../types"
import "./index.css"

export const SelectValues: React.FC<ISelectValues> = ({ valueName, handleCreateTicket, changeTime, url }) => {
    const [values, setValues] = useState<IProps[]>();
    const [disabled, setDisabled] = useState<boolean>(false);
    const [loader, setLoader] = useState<boolean>(true)

    useEffect(() => {
        (async function () { // получаем данные и вносим их в values ---> будет возможность выбрать в select options
            const apiData = await handleApi(url, "GET");
            if (valueName == "cinemas") {
                setValues([...apiData.cinemas])
            } else if (valueName == "timeslots") {
                const arrTimes = apiData.times.map((el: string, id: number) => ({ id: id.toString(), name: el }))
                setValues([...arrTimes])
            } else {
                setValues([...apiData])
            }
            setLoader(false)
        })()
    }, []);

    const createValuesObj = (targetValue: string) => {
        const array = targetValue.split(','); // targetValue = "name,id" ---> ["name", "id"]
        const obj = {
            [valueName]: array[0],
            [valueName + 'Id']: array[1],
        }
        handleCreateTicket(obj);
        setDisabled(true);
    }

    return (
        <>
            {loader ? <h4>loading...</h4> :
                <select disabled={valueName == "timeslots" ? !changeTime : disabled} onChange={(event: any) => {event.target.value != "none" && createValuesObj(event.target.value)}}>
                    <option value="none">none</option>
                    {values && values.map((el) => {
                        return (
                            <option key={el.id} value={[el.name, el.id]}>
                                {el.name}
                            </option>
                        )
                    })}
                </select>
            }
        </>
    )
}