export const actions = {
    logout: async (event) => {
        const { cookies } = event;

        try {
            cookies.delete("token", { path: "/" });

            return { message: "Logged out", status: 200 };
        } catch (error) {
            console.log(error);
            return { error: error?.detail || "Something went wrong!" };
        }
    },
};
