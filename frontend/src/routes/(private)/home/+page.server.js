import api from "$lib/api/api";
export const load = async ({ cookies, fetch, url }) => {
  const token = cookies.get("token");


  const page = url.searchParams.get("page") || "1";
  const status = url.searchParams.get("status");


  const getPayouts = async () => {
    try {
      let params = status ? { page, status } : { page };

      const tutorPayouts = await api.get("/vehicles/", token, fetch, params);
      const data = await tutorPayouts.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  return {
    payouts: await getPayouts(),
  };
};
