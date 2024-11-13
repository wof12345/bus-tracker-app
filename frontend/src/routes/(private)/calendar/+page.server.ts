import api from "$lib/api/api";

export const load = async ({ cookies, fetch, url }) => {
  const token = cookies.get("token");

  return {};
};

export const actions = {
  getSessions: async (event) => {
    const { request, cookies, locals, fetch } = event;

    const formData = await request.formData();

    const start_time = formData.get("start_time");
    const end_time = formData.get("end_time");

    const token = cookies.get("token");

    try {
      const res = await api.get(`/sessions/`, token, fetch, {
        start_time: start_time,
        end_time: end_time,
        limit: 1000,
      });

      const data = await res.json();

      return (
        data || {
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

  get_single_session: async (event) => {
    const { request, cookies, fetch } = event;
    const formData = await request.formData();
    const session_id = formData.get("session_id");
    const token = cookies.get("token");
    try {
      const res = await api.get(`/sessions/${session_id}`, token, fetch, {});
      const data = await res.json();
      return { session: data };
    } catch (error) {
      return { error: "Failed to fetch session data" };
    }
  },

  get_meeting_url: async (event) => {
    const { request, cookies, fetch } = event;

    const formData = await request.formData();

    const room_id = formData.get("room_id");

    const token = cookies.get("token");
    try {
      const res = await api.post(`/live-class/generate-code`, token, fetch, {
        body: { room_id: room_id },
      });
      const data = await res.json();
      return data;
    } catch (error) {
      return { error: "Failed to fetch session data" };
    }
  },

  re_schedule_session: async (event) => {
    const { request, cookies, fetch } = event;
    const formData = await request.formData();

    const session_id = formData.get("session_id");
    const order_id = formData.get("order_id");
    const start_time = formData.get("start_time");

    const body = {
      type: "Reschedule",
      description: "",
      order_id: order_id,
      refund_session_ids: [session_id],
      rescheduled_appointment_slots: [
        {
          start_time: start_time,
          session_id: session_id,
        },
      ],
    };
    const token = cookies.get("token");
    try {
      const res = await api.post(`/order-resolutions`, token, fetch, { body });
      const data = await res.json();
    } catch (error) {
      return { error: "Failed to send request" };
    }
  },
};
