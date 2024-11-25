import api from "$lib/api/api";

export const load = async ({ cookies, fetch, url }) => {
  const token = cookies.get("token");

  const page = url.searchParams.get("page") || "1";
  const tab = url.searchParams.get("tab");

  const getBuses = async () => {
    try {
      let params = { page };

      if (tab && tab != 0) {
        params['reservation'] = tab
      }

      const request = await api.get("/vehicles/", token, fetch, params);
      const data = await request.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  const getReservations = async () => {
    try {
      let params = { page, per_page: 1000 };



      const request = await api.get("/reservations/", token, fetch, params);
      const data = await request.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  return {
    vehicles: await getBuses(),
    reservations: await getReservations(),
  };
};

export const actions = {
  create: async (event) => {
    const { request, cookies, fetch } = event;

    const formData = await request.formData();

    let token = cookies.get("token");

    let name = formData.get("name");
    let description = formData.get("description");
    let license = formData.get("license");
    let current_coordinates = JSON.parse(formData.get("coordinates"));


    try {
      const res = await api.post("/vehicles/", token, fetch, {
        body: { name, description, current_coordinates, license },
      });

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

    let _id = formData.get("_id");
    let name = formData.get("name");
    let description = formData.get("description");
    let license = formData.get("license");
    let current_coordinates = JSON.parse(formData.get("coordinates"));
    let driver = JSON.parse(formData.get("driver"));
    let helper = JSON.parse(formData.get("helper"));
    let reservation = JSON.parse(formData.get("reservation"));
    let route = JSON.parse(formData.get("route"));
    let starting_point = JSON.parse(formData.get("starting_point"));
    let time = JSON.parse(formData.get("time"));

    let preBody = {
      name,
      driver,
      description,
      current_coordinates,
      license,
      helper,
      time,
      reservation,
      route,
      starting_point,
    };

    let body = { name, description, license };
    for (let key in preBody) {
      if (preBody[key]) {
        body[key] = preBody[key];
      }
    }

    console.log(body);
    try {
      const res = await api.put(`/vehicles/${_id}`, token, fetch, {
        body: body,
      });

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

    let _id = formData.get("_id");

    try {
      const res = await api.del(`/vehicles/${_id}`, token, fetch, {});

      let data = await res.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  },
};
