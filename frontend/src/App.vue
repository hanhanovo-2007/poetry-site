<template>
  <div id="app">
    <header class="nav-header">
      <div class="nav-inner">
        <router-link to="/" class="nav-logo">
          <span class="logo-icon">&#33773;</span>
          <span class="logo-text">诗词鉴赏交流</span>
        </router-link>
        <nav class="nav-links">
          <router-link to="/" class="nav-link" exact-active-class="active">首页</router-link>
          <router-link to="/publish" class="nav-link" active-class="active">即兴书写</router-link>
          <router-link to="/gallery" class="nav-link" active-class="active">诗歌苑</router-link>
          <router-link to="/profile" class="nav-link" active-class="active">个人主页</router-link>
          <router-link to="/about" class="nav-link" active-class="active">关于我们</router-link>
        </nav>
        <div class="nav-right">
          <template v-if="isLoggedIn">
            <router-link to="/profile" class="nav-user-btn">
              <span class="user-avatar-sm">{{ (user.nickname || user.username).charAt(0) }}</span>
              <span class="user-name">{{ user.nickname || user.username }}</span>
            </router-link>
            <button class="nav-logout-btn" @click="handleLogout">退出</button>
          </template>
          <template v-else>
            <button class="nav-login-btn" @click="openLogin">登录</button>
            <button class="nav-register-btn" @click="openRegister">注册</button>
          </template>
        </div>
      </div>
    </header>

    <main class="main-content">
      <router-view />
    </main>

    <!-- Login Modal -->
    <div v-if="showLoginModal" class="modal-overlay" @click.self="closeModals">
      <div class="modal-card">
        <button class="modal-close" @click="closeModals">&times;</button>
        <h2 class="modal-title">登录</h2>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="loginForm.username" class="form-input" required placeholder="请输入用户名" />
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="loginForm.password" type="password" class="form-input" required placeholder="请输入密码" />
          </div>
          <p v-if="loginError" class="form-error">{{ loginError }}</p>
          <button type="submit" class="btn btn-primary btn-full" :disabled="loginLoading">
            {{ loginLoading ? "登录中..." : "登录" }}
          </button>
          <p class="modal-switch">还没有账号？<a href="#" @click.prevent="openRegister">立即注册</a></p>
        </form>
      </div>
    </div>

    <!-- Register Modal -->
    <div v-if="showRegisterModal" class="modal-overlay" @click.self="closeModals">
      <div class="modal-card">
        <button class="modal-close" @click="closeModals">&times;</button>
        <h2 class="modal-title">注册</h2>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="regForm.username" class="form-input" required placeholder="字母或数字组合" />
          </div>
          <div class="form-group">
            <label>昵称</label>
            <input v-model="regForm.nickname" class="form-input" required placeholder="你的笔名" />
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="regForm.email" type="email" class="form-input" placeholder="选填" />
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="regForm.password" type="password" class="form-input" required minlength="6" placeholder="至少6位" />
          </div>
          <p v-if="registerError" class="form-error">{{ registerError }}</p>
          <button type="submit" class="btn btn-primary btn-full" :disabled="registerLoading">
            {{ registerLoading ? "注册中..." : "注册" }}
          </button>
          <p class="modal-switch">已有账号？<a href="#" @click.prevent="openLogin">立即登录</a></p>
        </form>
      </div>
    </div>

    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-divider"></div>
        <p class="footer-text">诗以言志，文以载道</p>
        <p class="footer-copy">&copy; 2026 诗词鉴赏交流 &mdash; 以诗会友，共赏风华</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import { useAuth } from "./composables/useAuth"

const {
  user, isLoggedIn, showLoginModal, showRegisterModal,
  openLogin, openRegister, closeModals,
  loadUser, login, register, logout,
} = useAuth()

const loginForm = reactive({ username: "", password: "" })
const regForm = reactive({ username: "", nickname: "", email: "", password: "", bio: "" })
const loginError = ref("")
const registerError = ref("")
const loginLoading = ref(false)
const registerLoading = ref(false)

async function handleLogin() {
  loginError.value = ""
  loginLoading.value = true
  try {
    await login(loginForm.username, loginForm.password)
    loginForm.username = ""; loginForm.password = ""
  } catch (e) {
    loginError.value = e.message
  } finally {
    loginLoading.value = false
  }
}

async function handleRegister() {
  registerError.value = ""
  registerLoading.value = true
  try {
    await register({ ...regForm })
    regForm.username = ""; regForm.nickname = ""; regForm.email = ""; regForm.password = ""; regForm.bio = ""
  } catch (e) {
    registerError.value = e.message
  } finally {
    registerLoading.value = false
  }
}

async function handleLogout() {
  try { await logout() } catch {}
}

onMounted(() => { loadUser() })
</script>

<style scoped>
.nav-header {
  background: linear-gradient(135deg, #2c2c2c 0%, #3a2a1a 100%);
  position: sticky; top: 0; z-index: 100;
  border-bottom: 2px solid var(--gold, #B8860B);
}
.nav-inner {
  max-width: var(--max-width, 1200px); margin: 0 auto;
  display: flex; align-items: center;
  height: 64px; padding: 0 20px; gap: 12px;
}
.nav-logo {
  display: flex; align-items: center; gap: 8px; text-decoration: none;
  margin-right: auto;
}
.logo-icon { font-size: 28px; color: var(--gold, #B8860B); }
.logo-text { font-size: 20px; font-weight: bold; color: var(--parchment, #F5E6CC); letter-spacing: 3px; }
.nav-links { display: flex; gap: 4px; }
.nav-link {
  color: rgba(245, 230, 204, 0.8); text-decoration: none; font-size: 15px;
  padding: 8px 18px; border-radius: 4px; transition: all 0.2s; letter-spacing: 2px;
}
.nav-link:hover { color: var(--parchment, #F5E6CC); background: rgba(184, 134, 11, 0.15); }
.nav-link.active { color: var(--gold, #B8860B); background: rgba(184, 134, 11, 0.2); }
.nav-right { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.nav-user-btn {
  display: flex; align-items: center; gap: 6px; text-decoration: none;
  color: var(--parchment, #F5E6CC); padding: 4px 10px; border-radius: 4px; transition: background 0.2s;
}
.nav-user-btn:hover { background: rgba(184, 134, 11, 0.15); }
.user-avatar-sm {
  width: 28px; height: 28px; border-radius: 50%; background: var(--gold, #B8860B);
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; color: #2c2c2c; font-weight: bold;
}
.user-name { font-size: 14px; max-width: 100px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.nav-login-btn, .nav-register-btn, .nav-logout-btn {
  background: none; border: 1px solid rgba(245, 230, 204, 0.3);
  color: var(--parchment, #F5E6CC); padding: 6px 14px; border-radius: 4px;
  font-family: var(--font-cn, serif); font-size: 13px; cursor: pointer;
  transition: all 0.2s; letter-spacing: 1px;
}
.nav-login-btn:hover, .nav-register-btn:hover { background: rgba(184, 134, 11, 0.2); border-color: var(--gold, #B8860B); }
.nav-logout-btn:hover { background: rgba(139, 37, 0, 0.3); border-color: var(--red-primary, #8B2500); }
.main-content { min-height: calc(100vh - 160px); }
.site-footer {
  background: linear-gradient(135deg, #2c2c2c 0%, #3a2a1a 100%);
  padding: 30px 20px; text-align: center;
  border-top: 2px solid var(--gold, #B8860B);
}
.footer-inner { max-width: var(--max-width, 1200px); margin: 0 auto; }
.footer-divider {
  width: 60px; height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold, #B8860B), transparent);
  margin: 0 auto 16px;
}
.footer-text { color: var(--parchment, #F5E6CC); font-size: 14px; letter-spacing: 3px; margin-bottom: 8px; }
.footer-copy { color: rgba(245, 230, 204, 0.5); font-size: 12px; letter-spacing: 1px; }

/* Modal */
.modal-overlay {
  position: fixed; inset: 0; z-index: 999;
  background: rgba(0, 0, 0, 0.55);
  display: flex; align-items: center; justify-content: center;
}
.modal-card {
  background: var(--cream, #FFF8F0); border-radius: 8px;
  padding: 36px 32px 28px; width: 380px; max-width: 90vw;
  position: relative; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
.modal-close {
  position: absolute; top: 10px; right: 14px;
  background: none; border: none; font-size: 24px;
  color: var(--text-muted, #8a7a6a); cursor: pointer;
}
.modal-title { font-size: 22px; text-align: center; letter-spacing: 3px; margin-bottom: 24px; color: var(--ink-black, #2c2c2c); }
.form-error { color: var(--red-primary, #8B2500); font-size: 13px; margin-bottom: 12px; text-align: center; }
.btn-full { width: 100%; margin-top: 8px; }
.modal-switch { text-align: center; font-size: 13px; color: var(--text-muted, #8a7a6a); margin-top: 16px; }
.modal-switch a { color: var(--red-primary, #8B2500); }
</style>

