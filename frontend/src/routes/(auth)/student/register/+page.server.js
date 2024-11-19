

import { fail, redirect } from "@sveltejs/kit";
import { showSpinner } from "$lib/store/spinner";
import api from "$lib/api/api";
import { v4 as uuidv4 } from "uuid";

export const actions = {
  register: async (event) => {
    const { request, cookies, locals, fetch } = event;

    const formData = await request.formData();

    const first_name = formData.get("first_name");
    const last_name = formData.get("last_name");
    const email = formData.get("email");
    const password = formData.get("password");

    let token = cookies.get("token");

    try {
      const res = await api.post("/auth/register/", token, fetch, {
        body: {
          first_name,
          last_name,
          email,
          password,
          role: "student",
        },
      });

      let data = await res.json();

      let userData;

      if ("token" in data)
        userData = {
          username: email,
          role: role,
          token: data.token,
        };

      return data;
    } catch (error) {
      console.log(error);
      return { error: error?.detail || "Something went wrong!" };
    }
  },
};
