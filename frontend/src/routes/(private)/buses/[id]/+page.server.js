import api from "$lib/api/api";

export const load = async ({ cookies, fetch, params }) => {
  const token = cookies.get("token");

  let id = params.id;

  const getRoutes = async () => {
    try {
      let params = { per_page: 1000 };

      const request = await api.get("/routes/", token, fetch, params);
      const data = await request.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  const getReservations = async () => {
    try {
      let params = { per_page: 1000 };

      const request = await api.get("/reservations/", token, fetch, params);
      const data = await request.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  const getHotspots = async () => {
    try {
      let params = { per_page: 1000 };

      const request = await api.get("/hotspots/", token, fetch, params);
      const data = await request.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  const getDrivers = async () => {
    try {
      let params = { per_page: 1000, role: 'driver' };

      const request = await api.get("/users/", token, fetch, params);
      const data = await request.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  const getHelpers = async () => {
    try {
      let params = { per_page: 1000, role: 'helper' };

      const request = await api.get("/users/", token, fetch, params);
      const data = await request.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  const getVehicle = async () => {
    try {
      let params = {};

      const request = await api.get(`/vehicles/${id}`, token, fetch, params);
      const data = await request.json();

      return data;
    } catch (error) {
      return { error: error?.detail || "Something went wrong!" };
    }
  };

  return {
    vehicle: await getVehicle(),
    routes: await getRoutes(),
    hotspots: await getHotspots(),
    reservations: await getReservations(),
    drivers: await getDrivers(),
    helpers: await getHelpers(),
  };
};


