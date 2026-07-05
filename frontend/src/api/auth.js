import api from "./index";

export function registerUser(data) {
  return api.post("/register/", data);
}

export function loginUser(data) {
  return api.post("/login/", data);
}

export function logoutUser() {
  return api.post("/logout/");
}

export function getProfile() {
  return api.get("/profile/");
}

export function updateProfile(data) {
  return api.put("/profile/", data);
}
