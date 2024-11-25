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

  };
};


export const actions = {
  process: async (event) => {
    const { request, cookies, fetch } = event;

    const formData = await request.formData();

    let token = cookies.get("token");

    let file = formData.get('file')


    try {
      const res = await api.upload("/license-detection/extract-license-plates", token, fetch, file, 'POST');

      let data = await res.json();

      return data;
    } catch (error) {

      console.log(error);
      return { error: error?.detail || "Something went wrong!" };
    }
  },
}