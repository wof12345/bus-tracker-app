import { fail, redirect } from "@sveltejs/kit";
import { showSpinner } from "$lib/store/spinner";
import { validateApiResponse } from "$components/utils/validateApiResponse.js";
import api from "$lib/api/api";

export const load = async (event) => {
  const { parent } = event;
  const { user } = await parent();

  if (validateApiResponse(user)) {
    redirect(307, "/home");
  }

  return {};
};

export const actions = {
  login: async (event) => {
    const { request, cookies, locals, fetch } = event;

    const formData = await request.formData();

    const email = formData.get("email");
    const password = formData.get("password_login");

    let token = cookies.get("token");

    try {
      const res = await api.post("/auth/login/", token, fetch, {
        body: {
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
          role: "student",
          token: data.token,
        };

      cookies.set("token", data.token, { path: "/" });

      return (
        userData || {
          error:
            typeof data.detail === "string"
              ? data.detail
              : "Something went wrong",
        }
      );
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  },
};
