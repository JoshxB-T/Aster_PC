import { apiRequest } from "./apiClient";
import { ENDPOINTS } from "./endpoints";
import { SignupRequest } from "./types";

export async function postSignup({
    username,
    email,
    password
}: SignupRequest) {
    return apiRequest(
        ENDPOINTS.POST_SIGNUP,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                email,
                password
            })
        }
    );
}