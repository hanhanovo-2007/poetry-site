<template>
  <div class="page profile-page">
    <div v-if="loading" class="loading-state">加载中...</div>

    <template v-else>
      <div class="profile-header">
        <div class="profile-avatar">{{ displayName.charAt(0) }}</div>
        <div class="profile-info">
          <h1 class="profile-name">{{ displayName }}</h1>
          <p class="profile-bio">{{ profileData.bio || (isOwner ? "这个人很懒，什么都没写..." : "诗歌爱好者") }}</p>
          <p class="profile-meta" v-if="profileData.created_at">注册于 {{ profileData.created_at }}</p>
        </div>
      </div>

      <div class="profile-tabs">
        <button :class="['tab-btn', { active: activeTab === 'account' }]" @click="activeTab = 'account'">
          {{ isOwner ? "我的账号" : "个人信息" }}
        </button>
        <button :class="['tab-btn', { active: activeTab === 'works' }]" @click="activeTab = 'works'">
          {{ isOwner ? "我的作品" : "Ta的作品" }}
        </button>
      </div>

      <!-- Account Tab -->
      <div v-if="activeTab === 'account'" class="tab-content">
        <div class="card account-card">
          <h3 class="card-title">{{ isOwner ? "登录信息" : (profileData.nickname || profileData.username) + " 的个人信息" }}</h3>
          <div class="info-row"><span class="info-label">账号</span><span class="info-value">{{ profileData.username }}</span></div>
          <div class="info-row"><span class="info-label">昵称</span><span class="info-value">{{ profileData.nickname || profileData.username }}</span></div>
          <div class="info-row"><span class="info-label">邮箱</span><span class="info-value">{{ profileData.email || "未设置" }}</span></div>
          <div class="info-row"><span class="info-label">简介</span><span class="info-value">{{ profileData.bio || "未设置" }}</span></div>
        </div>

        <div v-if="isOwner" class="card edit-card">
          <h3 class="card-title">编辑资料</h3>
          <p v-if="editError" class="form-error">{{ editError }}</p>
          <p v-if="editSuccess" class="form-success">{{ editSuccess }}</p>
          <div class="form-group"><label>昵称</label><input v-model="editForm.nickname" class="form-input" /></div>
          <div class="form-group"><label>个人简介</label><textarea v-model="editForm.bio" class="form-textarea" style="min-height:80px"></textarea></div>
          <div class="form-group"><label>邮箱</label><input v-model="editForm.email" type="email" class="form-input" /></div>
          <div class="form-group"><label>新密码（留空不修改）</label><input v-model="editForm.password" type="password" class="form-input" placeholder="至少6位" /></div>
          <button class="btn btn-primary" @click="saveProfile" :disabled="editLoading">{{ editLoading ? "保存中..." : "保存修改" }}</button>
        </div>
      </div>

      <!-- Works Tab -->
      <div v-if="activeTab === 'works'" class="tab-content">
        <div class="works-toolbar">
          <span class="works-count">共 {{ userWorks.length }} 篇作品</span>
          <button v-if="isOwner" class="btn btn-primary btn-sm" @click="$router.push('/publish')">&#10133; 写新诗</button>
        </div>
        <div v-if="worksLoading" class="loading-small">加载作品...</div>
        <div v-for="work in userWorks" :key="work.id" class="work-item card">
          <div class="work-item-header">
            <h3 class="work-item-title">{{ work.title }}</h3>
            <div v-if="isOwner" class="work-actions">
              <button class="action-btn edit" @click="editWork(work)">&#9998;</button>
              <button class="action-btn delete" @click="handleDelete(work.id)">&#128465;</button>
            </div>
          </div>
          <p class="work-item-content">{{ work.content }}</p>
          <div class="work-stats">
            <span>&#10084; {{ work.likes }}</span>
            <span>&#128172; {{ work.comments_count || 0 }}</span>
            <span class="work-date">{{ work.created_at }}</span>
          </div>
        </div>
        <div v-if="!worksLoading && userWorks.length === 0" class="empty-state">
          <template v-if="isOwner">暂无作品，<router-link to="/publish">开始创作</router-link></template>
          <template v-else>Ta还没有发表作品</template>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { getWorks, deleteWork as apiDeleteWork } from "../api/poetry"
import { useAuth } from "../composables/useAuth"

const route = useRoute()
const router = useRouter()
const { user: currentUser, isLoggedIn, updateProfile, loadUser } = useAuth()

const activeTab = ref("account")
const loading = ref(true)
const worksLoading = ref(false)
const editLoading = ref(false)
const editError = ref("")
const editSuccess = ref("")
const profileData = ref({})
const userWorks = ref([])

const editForm = reactive({ nickname: "", bio: "", email: "", password: "" })

const usernameParam = computed(() => route.params.username || null)
const isOwner = computed(() => {
  if (!usernameParam.value) return true
  return currentUser.value && (currentUser.value.username === usernameParam.value || currentUser.value.nickname === usernameParam.value)
})
const displayName = computed(() => profileData.value.nickname || profileData.value.username || "")

async function loadProfile() {
  loading.value = true
  try {
    if (isOwner.value) {
      if (!currentUser.value) await loadUser()
      profileData.value = currentUser.value ? { ...currentUser.value } : {}
      editForm.nickname = profileData.value.nickname || ""
      editForm.bio = profileData.value.bio || ""
      editForm.email = profileData.value.email || ""
    } else {
      // Viewing another user - fetch their info from the works list
      profileData.value = {
        username: usernameParam.value,
        nickname: usernameParam.value,
        bio: "诗歌爱好者",
      }
    }
  } catch (e) {
    console.error("Load profile error:", e)
  } finally {
    loading.value = false
  }
}

async function loadWorks() {
  worksLoading.value = true
  try {
    let params = {}
    if (isOwner.value && currentUser.value) {
      params.author = currentUser.value.id
    } else if (usernameParam.value) {
      // We need the user ID - try getting from works
      const allWorks = await getWorks({ search: usernameParam.value })
      userWorks.value = allWorks.data.filter(
        (w) => w.author.username === usernameParam.value
      )
      worksLoading.value = false
      return
    }
    const res = await getWorks(params)
    userWorks.value = res.data
  } catch (e) {
    console.error("Load works error:", e)
  } finally {
    worksLoading.value = false
  }
}

async function saveProfile() {
  editError.value = ""
  editSuccess.value = ""
  editLoading.value = true
  try {
    await updateProfile({
      nickname: editForm.nickname,
      bio: editForm.bio,
      email: editForm.email,
      password: editForm.password,
    })
    editSuccess.value = "资料已更新"
    editForm.password = ""
  } catch (e) {
    editError.value = e.message
  } finally {
    editLoading.value = false
  }
}

function editWork(work) {
  // For now, navigate to publish page
  router.push("/publish")
}

async function handleDelete(id) {
  if (!confirm("确定删除此作品？")) return
  try {
    await apiDeleteWork(id)
    userWorks.value = userWorks.value.filter((w) => w.id !== id)
  } catch (e) {
    alert(e.message)
  }
}

watch(
  () => route.params.username,
  () => { loadProfile(); loadWorks() }
)

onMounted(() => { loadProfile(); loadWorks() })
</script>

<style scoped>
.loading-state, .loading-small { text-align: center; padding: 60px; color: var(--text-muted, #8a7a6a); }
.loading-small { padding: 20px; }
.profile-header { display: flex; align-items: center; gap: 24px; padding: 32px; background: linear-gradient(135deg, #3a2a1a 0%, #2c2c2c 100%); border-radius: 8px; margin-bottom: 24px; color: white; }
.profile-avatar { width: 80px; height: 80px; border-radius: 50%; background: var(--gold, #B8860B); display: flex; align-items: center; justify-content: center; font-size: 36px; color: white; flex-shrink: 0; }
.profile-name { font-size: 24px; letter-spacing: 3px; margin-bottom: 4px; }
.profile-bio { font-size: 14px; color: rgba(255,255,255,0.7); margin-bottom: 4px; }
.profile-meta { font-size: 12px; color: rgba(255,255,255,0.5); }
.profile-tabs { display: flex; gap: 0; margin-bottom: 24px; border-bottom: 2px solid var(--border-color, #D4C5A9); }
.tab-btn { padding: 12px 32px; background: none; border: none; font-family: var(--font-cn, serif); font-size: 16px; color: var(--text-muted, #8a7a6a); cursor: pointer; letter-spacing: 2px; transition: all 0.2s; border-bottom: 2px solid transparent; margin-bottom: -2px; }
.tab-btn.active { color: var(--red-primary, #8B2500); border-bottom-color: var(--red-primary, #8B2500); }
.tab-content { max-width: 700px; }
.card-title { font-size: 18px; color: var(--ink-black, #2c2c2c); letter-spacing: 2px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border-color, #D4C5A9); }
.account-card, .edit-card { margin-bottom: 20px; padding: 24px; }
.info-row { display: flex; padding: 10px 0; border-bottom: 1px solid var(--parchment-dark, #E8D5B0); }
.info-row:last-child { border-bottom: none; }
.info-label { width: 80px; color: var(--text-muted, #8a7a6a); font-size: 14px; }
.info-value { flex: 1; color: var(--text-primary, #2c2c2c); font-size: 14px; }
.form-error { color: var(--red-primary, #8B2500); font-size: 13px; margin-bottom: 12px; }
.form-success { color: #2d5a2d; font-size: 13px; margin-bottom: 12px; }
.works-toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.works-count { font-size: 14px; color: var(--text-muted, #8a7a6a); }
.work-item { padding: 20px; margin-bottom: 16px; }
.work-item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.work-item-title { font-size: 18px; color: var(--ink-black, #2c2c2c); letter-spacing: 2px; }
.work-actions { display: flex; gap: 8px; }
.action-btn { background: none; border: 1px solid var(--border-color, #D4C5A9); border-radius: 4px; padding: 4px 10px; cursor: pointer; font-size: 14px; transition: all 0.2s; }
.action-btn.edit:hover { border-color: var(--gold, #B8860B); color: var(--gold, #B8860B); }
.action-btn.delete:hover { border-color: var(--red-primary, #8B2500); color: var(--red-primary, #8B2500); }
.work-item-content { font-size: 15px; color: var(--text-secondary, #5a4a3a); line-height: 2; margin-bottom: 12px; }
.work-stats { display: flex; gap: 20px; font-size: 13px; color: var(--text-muted, #8a7a6a); }
.work-date { margin-left: auto; }
.empty-state { text-align: center; padding: 40px; color: var(--text-muted, #8a7a6a); }
</style>

