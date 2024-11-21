import api from "$lib/api/api";

export const load = async ({ cookies, fetch, params }) => {
  const token = cookies.get("token");

  let id = params.id;

  const getHotspots = async () => {
    try {
      let params = { per_page: 1000 };

      const request = await api.get("/hotspots/", token, fetch, params);
      const data = await request.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  const getRoute = async () => {
    try {
      let params = {};

      const request = await api.get(`/routes/${id}`, token, fetch, params);
      const data = await request.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  return {
    route: await getRoute(),
    hotspots: await getHotspots(),
  };
};

export const actions = {
  update: async (event) => {
    const { request, cookies, fetch } = event;

    const formData = await request.formData();

    let token = cookies.get("token");

    let _id = formData.get("_id");
    let name = formData.get("name");
    let description = formData.get("description");

    let coordinates = JSON.parse(formData.get("coordinates"));
    let lines = JSON.parse(formData.get("lines"));
    let hotspots = JSON.parse(formData.get("hotspots"));

    try {
      const res = await api.put(`/routes/${_id}`, token, fetch, {
        body: { name, lines, description, coordinates, hotspots },
      });

      let data = await res.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  },
};
