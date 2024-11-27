import api from "$lib/api/api";

export const load = async ({ cookies, fetch, url }) => {
  const token = cookies.get("token");

  const page = url.searchParams.get("page") || "1";
  const tab = url.searchParams.get("tab");

  const getBuses = async () => {
    try {
      let params = { page, per_page: 1000 };

      if (tab && tab != 0) {
        params["reservation"] = tab;
      }

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
