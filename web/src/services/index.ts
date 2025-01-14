export const handleApi = async (url: string, apiMethod: string, bodyParams?: number[]) => {
    try {
        const response = await fetch(
            url, bodyParams ?
            {
                method: apiMethod,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(bodyParams)
            }
            :
            { method: apiMethod }
        );
        const data = await response.json();
        return data
    } catch (error) {
        console.error(error)
    }
}