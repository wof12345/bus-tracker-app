import api from "$lib/api/api";
import { v4 as uuidv4 } from "uuid";

export const load = async ({ cookies, fetch, url }) => {
  const token = cookies.get("token");

  const page = url.searchParams.get("page") || "1";

  const getUsers = async () => {
    try {
      let params = { page, role: 'driver' };

      const request = await api.get("/users/", token, fetch, params);
      const data = await request.json();



      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  return {
    users: await getUsers(),
  };
};


export const actions = {
  create: async (event) => {
    const { request, cookies, fetch } = event;

    const formData = await request.formData();

    let token = cookies.get("token");

    let email = formData.get('email')
    let password = formData.get('password') || uuidv4()
    let phone = formData.get('phone')
    let first_name = formData.get('first_name')
    let last_name = formData.get('last_name')
    let address = formData.get('address')
    let role = 'driver'


    try {
      const res = await api.post("/users/", token, fetch, { body: { email, password, phone, first_name, last_name, address, role } });

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
    let email = formData.get('email')
    let phone = formData.get('phone')
    let first_name = formData.get('first_name')
    let last_name = formData.get('last_name')
    let address = formData.get('address')
    let role = 'driver'


    try {
      const res = await api.put(`/users/${_id}`, token, fetch, { body: { email, phone, first_name, last_name, address, role } });

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
      const res = await api.del(`/users/${_id}`, token, fetch, {});

      let data = await res.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  },
};