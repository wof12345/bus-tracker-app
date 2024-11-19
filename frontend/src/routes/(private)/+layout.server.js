import { redirect } from "@sveltejs/kit";

export const load = async (event) => {

  const { parent } = event;
  const { user } = await parent();

  if (!user) {
    redirect(307, '/')
  }

  return {
    user,

  };
};
