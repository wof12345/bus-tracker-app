
import api from "$lib/api/api";

export const actions = {
  register: async (event) => {
    const { request, cookies, fetch } = event;

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
          role: "commuter",
        },
      });

      let data = await res.json();
      return data;
    } catch (error) {
      console.log(error);
      return { error: error?.detail || "Something went wrong!" };
    }
  },
};
