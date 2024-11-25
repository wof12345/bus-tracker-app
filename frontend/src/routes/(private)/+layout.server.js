import { redirect } from "@sveltejs/kit";

export const load = async (event) => {

  const { parent } = event;
  const { user } = await parent();

  console.log(user);

  if (!user) {
    redirect(307, '/commuter/login')
  }

  return {
    user,

  };
};
