import { showToaster } from "$lib/store/toaster";

export function validateApiResponse(response, toaster = true) {


    if (response?.data?.detail || response?.detail || response?.data?.error || !response) {
        if (typeof response?.data?.detail === "string")
            if (toaster) showToaster(response?.data?.detail);
            else if (toaster) showToaster("Something went wrong!");

        return false;
    }

    return true
}