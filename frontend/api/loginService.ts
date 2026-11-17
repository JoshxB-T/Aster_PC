import { apiRequest } from "./apiClient";
import { ENDPOINTS } from "./endpoints";
import { LoginRequest, LoginResponse } from "./types";

export async function postLogin({
    email,
    password
}: LoginRequest): Promise<LoginResponse> {
    return apiRequest(
        ENDPOINTS.POST_LOGIN,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        }
    );
}