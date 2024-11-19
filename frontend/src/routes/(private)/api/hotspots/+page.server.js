import api from "$lib/api/api";

export const actions = {
    create: async (event) => {
        const { request, cookies, fetch } = event;

        const formData = await request.formData();

        let token = cookies.get("token");

        let name = formData.get('name')
        let location_name = formData.get('location_name')
        let coordinates = JSON.parse(formData.get('coordinates'))
        let description = formData.get('description')

        try {
            const res = await api.post("/hotspots/", token, fetch, { body: { name, location_name, description, coordinates } });

            let data = await res.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },
};
