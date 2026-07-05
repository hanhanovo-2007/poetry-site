import { reactive, computed } from "vue"
import api from "../api/index"

const state = reactive({
  user: null,
  showLoginModal: false,
  showRegisterModal: false,
})

export function useAuth() {
  const user = computed(() => state.user)
  const isLoggedIn = computed(() => state.user !== null)
  const showLoginModal = computed(() => state.showLoginModal)
  const showRegisterModal = computed(() => state.showRegisterModal)

  function openLogin() { state.showLoginModal = true; state.showRegisterModal = false }
  function openRegister() { state.showRegisterModal = true; state.showLoginModal = false }
  function closeModals() { state.showLoginModal = false; state.showRegisterModal = false }

  async function loadUser() {
    try {
      const res = await api.get("/profile/")
      state.user = res.data
    } catch {
      state.user = null
    }
  }

  async function login(username, password) {
    const res = await api.post("/login/", { username, password })
    state.user = res.data
    closeModals()
    return res
  }

  async function register(data) {
    const res = await api.post("/register/", data)
    state.user = res.data
    closeModals()
    return res
  }

  async function logout() {
    await api.post("/logout/")
    state.user = null
  }

  async function updateProfile(data) {
    const res = await api.put("/profile/", data)
    state.user = res.data
    return res
  }

  return {
    user, isLoggedIn, showLoginModal, showRegisterModal,
    openLogin, openRegister, closeModals,
    loadUser, login, register, logout, updateProfile,
  }
}
