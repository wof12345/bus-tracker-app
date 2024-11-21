import api from "$lib/api/api";

export const load = async ({ cookies, fetch, url }) => {
  const token = cookies.get("token");

  const page = url.searchParams.get("page") || "1";

  const getRoutes = async () => {
    try {
      let params = { page };

      const request = await api.get("/routes/", token, fetch, params);
      const data = await request.json();



      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  return {
    routes: await getRoutes(),
  };
};


export const actions = {

  delete: async (event) => {
    const { request, cookies, fetch } = event;

    const formData = await request.formData();

    let token = cookies.get("token");

    let _id = formData.get('_id')


    try {
      const res = await api.del(`/routes/${_id}`, token, fetch, {});

      let data = await res.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  },
};