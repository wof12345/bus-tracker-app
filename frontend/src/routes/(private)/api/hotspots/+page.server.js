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
        let primary = formData.get('primary')

        try {
            const res = await api.post("/hotspots/", token, fetch, { body: { name, location_name, description, coordinates, primary } });

            let data = await res.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },

    update: async (event) => {
        const { request, cookies, fetch } = event;

        const formData = await request.formData();

        let token = cookies.get("token");

        let name = formData.get('name')
        let id = formData.get('_id')
        let location_name = formData.get('location_name')
        let coordinates = JSON.parse(formData.get('coordinates'))
        let description = formData.get('description')
        let primary = formData.get('primary')

        try {
            const res = await api.put(`/hotspots/${id}`, token, fetch, { body: { name, location_name, description, coordinates, primary } });

            let data = await res.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },
};
