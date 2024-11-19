import api from "$lib/api/api";
export const load = async ({ cookies, fetch, url, params }) => {
  const token = cookies.get("token");


  const page = url.searchParams.get("page") || "1";



  const getHotspots = async () => {
    try {
      let params = { page };

      const request = await api.get("/hotspots/", token, fetch, params);
      const data = await request.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  return {
    hotspots: await getHotspots(),
  };
};
