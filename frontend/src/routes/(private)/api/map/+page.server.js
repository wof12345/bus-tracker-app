

const VITE_OPEN_CAGE_API_KEY = import.meta.env.VITE_OPEN_CAGE_API_KEY



export const actions = {
    reverseGeoCode: async (event) => {
        const { fetch, request } = event;

        const formData = await request.formData();

        let lat = formData.get('lat')
        let lng = formData.get('lng')


        try {
            const response =
                await fetch(`https://api.opencagedata.com/geocode/v1/json?q=${lat}+${lng}&key=${VITE_OPEN_CAGE_API_KEY}`);
            const data = await response.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },

};
