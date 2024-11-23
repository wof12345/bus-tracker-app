import api from "$lib/api/api";
import { redirect } from "@sveltejs/kit";

export const load = async ({ cookies, fetch, url }) => {
  const token = cookies.get("token");




  return redirect(307, '/commuter/login')
};




