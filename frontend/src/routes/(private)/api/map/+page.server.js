const VITE_OPEN_CAGE_API_KEY = import.meta.env.VITE_OPEN_CAGE_API_KEY;
const VITE_OPEN_ROUTE_API_KEY = import.meta.env.VITE_OPEN_ROUTE_API_KEY;
const VITE_LOCATION_IQ_API_KEY = import.meta.env.VITE_LOCATION_IQ_API_KEY;

export const actions = {
    reverseGeoCode: async (event) => {
        const { fetch, request } = event;

        const formData = await request.formData();

        let lat = formData.get("lat");
        let lng = formData.get("lng");

        try {
            const response = await fetch(
                `https://api.opencagedata.com/geocode/v1/json?q=${lat}+${lng}&key=${VITE_OPEN_CAGE_API_KEY}`,
            );
            const data = await response.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },

    forwardGeoCode: async (event) => {
        const { fetch, request } = event;

        const formData = await request.formData();

        let search = formData.get("search");

        console.log(search);


        try {
            const response = await fetch(
                `https://us1.locationiq.com/v1/search.php?key=${VITE_LOCATION_IQ_API_KEY}&q=${search}&format=json`,
            );
            const data = await response.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },


    getORSRoute: async (event) => {
        const { fetch, request } = event;

        const formData = await request.formData();

        let start = JSON.parse(formData.get("start"));
        let end = JSON.parse(formData.get("end"));

        console.log(start, end);

        const url = `https://api.openrouteservice.org/v2/directions/driving-car`;
        const body = {
            coordinates: [start, end],
        };

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: VITE_OPEN_ROUTE_API_KEY,
                },
                body: JSON.stringify(body),
            });

            const data = await response.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },
};
