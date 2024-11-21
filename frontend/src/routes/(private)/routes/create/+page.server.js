import api from "$lib/api/api";

export const load = async ({ cookies, fetch }) => {
  const token = cookies.get("token");

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

  return {
    hotspots: await getHotspots(),
  };
};

export const actions = {
  create: async (event) => {
    const { request, cookies, fetch } = event;

    const formData = await request.formData();

    let token = cookies.get("token");

    let name = formData.get("name");
    let description = formData.get("description");

    let coordinates = JSON.parse(formData.get("coordinates"));
    let lines = JSON.parse(formData.get("lines"));
    let hotspots = JSON.parse(formData.get("hotspots"));

    try {
      const res = await api.post("/routes/", token, fetch, {
        body: { name, lines, description, coordinates, hotspots },
      });

      let data = await res.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  },
};
