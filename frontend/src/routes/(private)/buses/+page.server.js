import api from "$lib/api/api";

export const load = async ({ cookies, fetch, url }) => {
  const token = cookies.get("token");

  const page = url.searchParams.get("page") || "1";

  const getBuses = async () => {
    try {
      let params = { page };

      const request = await api.get("/vehicles/", token, fetch, params);
      const data = await request.json();



      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  return {
    vehicles: await getBuses(),
  };
};


export const actions = {
  create: async (event) => {
    const { request, cookies, fetch } = event;

    const formData = await request.formData();

    let token = cookies.get("token");

    let name = formData.get('name')
    let description = formData.get('description')
    let license = formData.get('license')
    let current_coordinates = JSON.parse(formData.get('coordinates'))
    let driver = formData.get('driver')

    try {
      const res = await api.post("/vehicles/", token, fetch, { body: { name, driver, description, current_coordinates, license } });

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

    let _id = formData.get('_id')
    let name = formData.get('name')
    let description = formData.get('description')
    let license = formData.get('license')
    let current_coordinates = JSON.parse(formData.get('coordinates'))
    let driver = formData.get('driver')

    try {
      const res = await api.put(`/vehicles/${_id}`, token, fetch, { body: { name, driver, description, current_coordinates, license } });

      let data = await res.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  },

  delete: async (event) => {
    const { request, cookies, fetch } = event;

    const formData = await request.formData();

    let token = cookies.get("token");

    let _id = formData.get('_id')


    try {
      const res = await api.del(`/vehicles/${_id}`, token, fetch, {});

      let data = await res.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  },
};