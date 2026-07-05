<template>
  <div class="page gallery-page">
    <h1 class="page-title">诗歌苑</h1>
    <p class="page-subtitle">漫步诗林，品读百家之作</p>

    <div class="gallery-toolbar">
      <div class="search-box">
        <span class="search-icon">&#128269;</span>
        <input v-model="searchQuery" type="text" class="form-input" placeholder="搜索诗词标题或作者..." @input="debouncedSearch" />
      </div>
    </div>

    <div v-if="loading" class="loading-state">加载中...</div>

    <div v-else class="works-grid">
      <div v-for="work in filteredWorks" :key="work.id" class="work-card card">
        <div class="work-header">
          <div class="work-author" @click="viewProfile(work.author.username)">
            <div class="avatar" :style="{ background: avatarColors[work.author.id % avatarColors.length] }">
              {{ (work.author.nickname || work.author.username).charAt(0) }}
            </div>
            <div>
              <p class="author-name">{{ work.author.nickname || work.author.username }}</p>
              <p class="work-time">{{ work.created_at }}</p>
            </div>
          </div>
          <button class="work-likes-btn" :class="{ liked: likedSet.has(work.id) }" @click="handleLike(work.id)">
            &#10084; {{ work.likes }}
          </button>
        </div>

        <div v-if="work.image" class="work-image">
          <img :src="work.image" :alt="work.title" />
        </div>

        <h3 class="work-title">{{ work.title }}</h3>
        <p class="work-content">{{ work.content }}</p>

        <div class="work-footer">
          <button class="btn-comment" @click="toggleComment(work.id)">
            &#128172; 评论 ({{ work.comments_count }})
          </button>
        </div>

        <div v-if="openCommentId === work.id" class="comment-section">
          <div v-if="commentLoading(work.id)" class="loading-small">加载评论...</div>
          <div v-else class="comment-list">
            <div v-for="(c, i) in commentMap[work.id] || []" :key="i" class="comment-item">
              <span class="comment-author">{{ c.author.nickname || c.author.username }}</span>
              <span class="comment-text">{{ c.text }}</span>
            </div>
            <div v-if="!(commentMap[work.id] || []).length" class="no-comments">暂无评论</div>
          </div>
          <div class="comment-input-row">
            <input v-model="newComment" type="text" class="form-input" placeholder="写下你的评论..." />
            <button class="btn btn-primary btn-sm" @click="addComment(work.id)" :disabled="!newComment.trim()">发表</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && filteredWorks.length === 0" class="empty-state">
      <p>暂无相关作品</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import { getWorks, getComments, addComment as apiAddComment, likeWork } from "../api/poetry"
import { useAuth } from "../composables/useAuth"

const router = useRouter()
const { isLoggedIn, openLogin } = useAuth()

const searchQuery = ref("")
const openCommentId = ref(null)
const newComment = ref("")
const loading = ref(true)
const works = ref([])
const commentMap = ref({})
const loadingComments = ref({})
const likedSet = ref(new Set())
const avatarColors = ["#8B2500", "#2d5a2d", "#0f3460", "#5c3a00", "#6b3fa0", "#b8860b"]

let searchTimer = null

const filteredWorks = computed(() => {
  if (!searchQuery.value) return works.value
  const q = searchQuery.value.toLowerCase()
  return works.value.filter(
    (w) =>
      w.title.toLowerCase().includes(q) ||
      (w.author.nickname || w.author.username).toLowerCase().includes(q)
  )
})

function debouncedSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(fetchWorks, 300)
}

async function fetchWorks() {
  loading.value = true
  try {
    const res = await getWorks({ search: searchQuery.value })
    works.value = res.data
  } catch (e) {
    console.error("Failed to load works:", e)
  } finally {
    loading.value = false
  }
}

async function fetchComments(workId) {
  loadingComments.value[workId] = true
  try {
    const res = await getComments(workId)
    commentMap.value[workId] = res.data
  } catch {
    commentMap.value[workId] = []
  } finally {
    loadingComments.value[workId] = false
  }
}

function commentLoading(workId) {
  return loadingComments.value[workId]
}

async function toggleComment(workId) {
  if (openCommentId.value === workId) {
    openCommentId.value = null
    return
  }
  openCommentId.value = workId
  if (!commentMap.value[workId]) {
    await fetchComments(workId)
  }
}

async function addComment(workId) {
  if (!isLoggedIn.value) {
    openLogin()
    return
  }
  if (!newComment.value.trim()) return
  try {
    await apiAddComment(workId, { text: newComment.value })
    newComment.value = ""
    await fetchComments(workId)
    const work = works.value.find((w) => w.id === workId)
    if (work) work.comments_count++
  } catch (e) {
    alert(e.message)
  }
}

async function handleLike(workId) {
  if (likedSet.value.has(workId)) return
  try {
    const res = await likeWork(workId)
    likedSet.value.add(workId)
    const work = works.value.find((w) => w.id === workId)
    if (work) work.likes = res.data.likes
  } catch (e) {
    alert(e.message)
  }
}

function viewProfile(username) {
  router.push("/profile/" + encodeURIComponent(username))
}

onMounted(fetchWorks)
</script>

<style scoped>
.gallery-toolbar { margin-bottom: 24px; }
.search-box {
  display: flex; align-items: center;
  background: white; border: 1px solid var(--border-color, #D4C5A9);
  border-radius: var(--radius, 6px); padding: 0 14px; max-width: 400px;
}
.search-icon { font-size: 16px; color: var(--text-muted, #8a7a6a); margin-right: 8px; }
.search-box .form-input { border: none; padding-left: 0; }
.loading-state, .loading-small { text-align: center; padding: 40px; color: var(--text-muted, #8a7a6a); font-size: 14px; }
.loading-small { padding: 12px; font-size: 12px; }
.works-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; }
.work-card { padding: 0; overflow: hidden; }
.work-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-bottom: 1px solid var(--border-color, #D4C5A9); }
.work-author { display: flex; align-items: center; gap: 10px; cursor: pointer; }
.avatar { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; }
.author-name { font-size: 14px; color: var(--ink-black, #2c2c2c); font-weight: bold; }
.work-time { font-size: 12px; color: var(--text-muted, #8a7a6a); }
.work-likes-btn { background: none; border: none; font-size: 13px; color: var(--text-muted, #8a7a6a); cursor: pointer; transition: color 0.2s; font-family: var(--font-cn, serif); }
.work-likes-btn:hover { color: var(--red-primary, #8B2500); }
.work-likes-btn.liked { color: var(--red-primary, #8B2500); }
.work-image img { width: 100%; max-height: 240px; object-fit: cover; }
.work-title { font-size: 20px; color: var(--ink-black, #2c2c2c); padding: 12px 20px 4px; letter-spacing: 2px; }
.work-content { font-size: 15px; color: var(--text-secondary, #5a4a3a); padding: 0 20px 12px; line-height: 2; white-space: pre-wrap; }
.work-footer { padding: 12px 20px; border-top: 1px solid var(--border-color, #D4C5A9); }
.btn-comment { background: none; border: none; color: var(--text-muted, #8a7a6a); cursor: pointer; font-size: 13px; font-family: var(--font-cn, serif); transition: color 0.2s; }
.btn-comment:hover { color: var(--gold, #B8860B); }
.comment-section { padding: 12px 20px 16px; background: var(--parchment-light, #FAF3E6); border-top: 1px solid var(--border-color, #D4C5A9); }
.comment-list { margin-bottom: 12px; max-height: 200px; overflow-y: auto; }
.comment-item { padding: 6px 0; font-size: 14px; }
.comment-author { color: var(--red-primary, #8B2500); margin-right: 8px; font-weight: bold; }
.comment-text { color: var(--text-secondary, #5a4a3a); }
.no-comments { font-size: 13px; color: var(--text-muted, #8a7a6a); padding: 8px 0; }
.comment-input-row { display: flex; gap: 8px; }
.comment-input-row .form-input { flex: 1; }
.empty-state { text-align: center; padding: 60px; color: var(--text-muted, #8a7a6a); }
@media (max-width: 768px) { .works-grid { grid-template-columns: 1fr; } }
</style>

