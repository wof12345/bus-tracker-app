import api from "$lib/api/api";
export const load = async ({ cookies, fetch }) => {
  const token = cookies.get("token");


  const getStats = async () => {
    try {
      let params = {};

      const tutorPayouts = await api.get("/statistics/buses-by-reservations", token, fetch, params);
      const data = await tutorPayouts.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  return {
    statistics: await getStats(),
  };
};
