import api from "$lib/api/api";

export const actions = {
    getUserInfo: async (event) => {
        const { cookies, fetch } = event;

        let token = cookies.get("token");

        try {
            const res = await api.get("/account/info", token, fetch, {});

            let data = await res.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },

    updateUserPhoto: async (event) => {
        const { request, cookies, fetch } = event;

        const formData = await request.formData();

        const file = formData.get("file");

        let token = cookies.get("token");

        try {
            const res = await api.upload(
                "/account/photo",
                token,
                fetch,
                file,
                "PATCH",
            );

            let data = await res.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },

    updateUserPassword: async (event) => {
        const { request, cookies, fetch } = event;

        const formData = await request.formData();

        const current_password = formData.get("current_password");
        const new_password = formData.get("new_password");

        let token = cookies.get("token");

        try {
            const res = await api.patch("/account/password", token, fetch, {
                body: {
                    current_password,
                    new_password,
                },
            });

            let data = await res.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },

    updateUserInfo: async (event) => {
        const { request, cookies, fetch } = event;

        const formData = await request.formData();

        const first_name = formData.get("first_name");
        const last_name = formData.get("last_name");
        const email = formData.get("email");
        let date_of_birth = formData.get("date_of_birth");
        const phone = formData.get("phone");
        const gender = formData.get("gender");
        const nationality = formData.get("nationality");
        const address = JSON.parse(formData.get("address"));

        date_of_birth = new Date(date_of_birth);

        let token = cookies.get("token");

        try {
            const res = await api.patch("/account/info", token, fetch, {
                body: {
                    first_name,
                    last_name,
                    gender,
                    phone,
                    address,
                    date_of_birth,
                    nationality,
                },
            });

            let data = await res.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },

    getTutorInfo: async (event) => {
        const { cookies, fetch } = event;

        let token = cookies.get("token");

        try {
            const res = await api.get("/account/tutor/info", token, fetch, {});

            let data = await res.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },

    updateTutorInfo: async (event) => {
        const { request, cookies, fetch } = event;
        const formData = await request.formData();
        const years_of_exp = formData.get("years_of_experience");
        const about_description = formData.get("about_description");
        const experience_description = formData.get("experience_description");
        let native_lang = formData.get("native_lang");
        const available_hr_per_week = formData.get("available_hr_per_week");
        const preferred_tutoring_type = formData.get("preferred_tutoring_type");
        const spoken_langs = JSON.parse(formData.get("spoken_langs"));
        const areas = JSON.parse(formData.get("areas"));
        const preferred_curriculum = JSON.parse(
            formData.get("preferred_curriculum"),
        );
        const preferred_school_levels = JSON.parse(
            formData.get("preferred_school_level"),
        );
        const preferred_subjects = JSON.parse(formData.get("preferred_subjects"));
        const clean_convicted = formData.get("clean_convicted");
        const online_rate = formData.get("online_rate");
        const in_person_rate = formData.get("in_person_rate");

        const tutor_id = formData.get("tutor_id");

        let token = cookies.get("token");

        let form = {
            years_of_exp,
            about_description,
            experience_description,
            native_lang,
            areas,
            available_hr_per_week,
            preferred_tutoring_type,
            spoken_langs,
            preferred_curriculum,
            preferred_subjects,
            preferred_school_levels,
            clean_convicted,
            online_rate,
            in_person_rate,
            tutor_id,
        };

        let body = {};

        for (let key in form) {
            if (form[key] !== undefined && form[key] !== null) {
                body[key] = form[key];
            }
        }

        try {
            const res = await api.patch("/account/tutor/info", token, fetch, {
                body: body,
            });

            let data = await res.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },

    getTutorApplication: async (event) => {
        const { request, cookies, fetch } = event;

        let token = cookies.get("token");

        try {
            const res = await api.get("/account/tutor/application", token, fetch, {});

            let data = await res.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },

    updateTutorApplication: async (event) => {
        const { request, cookies, fetch } = event;

        const formData = await request.formData();

        const id_files = JSON.parse(formData.get("id_files"));

        let token = cookies.get("token");

        try {
            const res = await api.post("/account/tutor/application", token, fetch, {
                body: id_files,
            });

            let data = await res.json();

            return data;
        } catch (error) {
            return { error: error?.detail || "Something went wrong!" };
        }
    },

    getTutorBankDetails: async (event) => {
        const { cookies, fetch } = event;

        let token = cookies.get("token");

        try {
            const bankDetailsRes = await api.get(
                "/account/tutor/bank-detail",
                token,
                fetch,
                {},
            );

            const bankDetails = await bankDetailsRes.json();

            return bankDetails;
        } catch (error) {
            return null;
        }
    },
};
