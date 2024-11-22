import { redirect } from "@sveltejs/kit";
import api from "$lib/api/api";
import { validateApiResponse } from "$components/utils/validateApiResponse.js";

export const load = async (event) => {
  const { parent } = event
  const { user } = await parent();

  if (validateApiResponse(user)) {
    redirect(307, "/home");
  }

  return {};
};

export const actions = {
  login: async (event) => {
    const { request, cookies, fetch } = event;

    const formData = await request.formData();

    const email = formData.get("email");
    const password = formData.get("password_login");


    let token = cookies.get("token");

    try {
      const res = await api.post("/auth/login/", token, fetch, {
        body: {
          email,
          password,
          role: "driver",
        },
      });

      let data = await res.json();

      let userData;

      if ("token" in data)
        userData = {
          username: email,
          role: "tutor",
          token: data.token,
        };



      cookies.set('token', data.token, { path: '/' })

      return (
        userData || {
          error:
            typeof data.detail === "string"
              ? data.detail
              : "Something went wrong",
        }
      );
    } catch (error) {

      console.log(error)
      return { error: error?.detail || "Something went wrong!" };
    }
  },
};
