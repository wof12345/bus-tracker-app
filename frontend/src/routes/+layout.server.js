export const load = async (event) => {
    const user = await event.locals.verifyUser();

    return { user };
};