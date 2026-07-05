<template>
  <div class="page publish-page">
    <h1 class="page-title">即兴书写</h1>
    <p class="page-subtitle">挥毫泼墨，记录心中诗意</p>

    <div v-if="!isLoggedIn" class="login-hint card">
      <p>请先登录后再发表作品</p>
      <button class="btn btn-primary" @click="openLogin">前往登录</button>
    </div>

    <div v-else class="publish-layout">
      <div class="publish-main">
        <div class="card form-card">
          <div class="form-header">
            <span class="quill-icon">&#9998;</span>
            <span>创作新诗</span>
          </div>

          <div v-if="errorMsg" class="form-error-msg">{{ errorMsg }}</div>
          <div v-if="successMsg" class="form-success-msg">{{ successMsg }}</div>

          <div class="form-group">
            <label>诗词标题</label>
            <input v-model="form.title" type="text" class="form-input" placeholder="为你的诗作拟一个雅致的标题..." />
          </div>

          <div class="form-group">
            <label>诗词正文</label>
            <textarea v-model="form.content" class="form-textarea" placeholder="在此书写你的诗词佳作…&#10;一行一句，皆是心意。"></textarea>
          </div>

          <div class="form-group">
            <label>配图上传（可选）</label>
            <div class="upload-area" @click="triggerUpload">
              <input ref="fileInput" type="file" accept="image/*" hidden @change="handleUpload" />
              <div v-if="!previewUrl" class="upload-placeholder">
                <span class="upload-icon">&#127912;</span>
                <p>点击选择图片</p>
                <p class="upload-hint">支持 JPG / PNG 格式，展示在诗歌苑</p>
              </div>
              <div v-else class="upload-preview">
                <img :src="previewUrl" alt="配图预览" />
                <button class="upload-remove" @click.stop="removeImage">&times;</button>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button class="btn btn-primary" @click="submitPoem" :disabled="submitting">
              {{ submitting ? "发表中..." : "发表诗作" }}
            </button>
            <button class="btn btn-outline" @click="resetForm">清空重写</button>
          </div>
        </div>
      </div>

      <div class="publish-side">
        <div class="card tip-card">
          <h3 class="tip-title">&#10022; 创作提示</h3>
          <ul class="tip-list">
            <li>尝试以五言或七言为体</li>
            <li>注重意境与韵律的和谐</li>
            <li>可以古体，亦可现代诗</li>
            <li>配图与诗意相得益彰</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { createWork } from "../api/poetry"
import { useAuth } from "../composables/useAuth"

const router = useRouter()
const { isLoggedIn, openLogin } = useAuth()

const form = ref({ title: "", content: "" })
const fileInput = ref(null)
const previewUrl = ref("")
const imageFile = ref(null)
const submitting = ref(false)
const errorMsg = ref("")
const successMsg = ref("")

function triggerUpload() { fileInput.value.click() }

function handleUpload(e) {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    previewUrl.value = URL.createObjectURL(file)
  }
}

function removeImage() {
  previewUrl.value = ""
  imageFile.value = null
  if (fileInput.value) fileInput.value.value = ""
}

async function submitPoem() {
  errorMsg.value = ""
  successMsg.value = ""

  if (!form.value.title.trim()) {
    errorMsg.value = "请填写诗词标题"
    return
  }
  if (!form.value.content.trim()) {
    errorMsg.value = "请填写诗词正文"
    return
  }

  submitting.value = true
  try {
    let payload
    if (imageFile.value) {
      // 有图片时用 FormData 提交
      const fd = new FormData()
      fd.append("title", form.value.title.trim())
      fd.append("content", form.value.content.trim())
      fd.append("image", imageFile.value)
      payload = fd
    } else {
      payload = {
        title: form.value.title.trim(),
        content: form.value.content.trim(),
      }
    }
    await createWork(payload)
    successMsg.value = "作品发表成功！即将跳转..."
    resetForm()
    setTimeout(() => router.push("/gallery"), 1500)
  } catch (e) {
    errorMsg.value = e.message
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  form.value = { title: "", content: "" }
  removeImage()
  errorMsg.value = ""
  successMsg.value = ""
}
</script>

<style scoped>
.login-hint { text-align: center; padding: 48px; max-width: 400px; margin: 40px auto; }
.login-hint p { margin-bottom: 16px; color: var(--text-muted, #8a7a6a); font-size: 16px; }
.publish-layout { display: grid; grid-template-columns: 1fr 280px; gap: 24px; align-items: start; }
.publish-main { min-width: 0; }
.form-card { padding: 32px; }
.form-header { display: flex; align-items: center; gap: 8px; font-size: 18px; color: var(--red-primary, #8B2500); letter-spacing: 2px; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border-color, #D4C5A9); }
.quill-icon { font-size: 22px; }
.form-error-msg { color: var(--red-primary, #8B2500); font-size: 14px; margin-bottom: 12px; padding: 8px 12px; background: #fff0ee; border-radius: 4px; }
.form-success-msg { color: #2d5a2d; font-size: 14px; margin-bottom: 12px; padding: 8px 12px; background: #eefff0; border-radius: 4px; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-size: 14px; color: var(--text-secondary, #5a4a3a); margin-bottom: 6px; letter-spacing: 1px; }
.form-input, .form-textarea { width: 100%; padding: 10px 14px; border: 1px solid var(--border-color, #D4C5A9); border-radius: var(--radius, 6px); font-family: var(--font-cn, serif); font-size: 15px; background: white; color: var(--text-primary, #2c2c2c); transition: border-color 0.2s; }
.form-input:focus, .form-textarea:focus { outline: none; border-color: var(--gold, #B8860B); }
.form-textarea { min-height: 160px; resize: vertical; line-height: 1.8; }
.upload-area { border: 2px dashed var(--border-color, #D4C5A9); border-radius: var(--radius, 6px); padding: 24px; text-align: center; cursor: pointer; transition: all 0.2s; background: var(--parchment-light, #FAF3E6); }
.upload-area:hover { border-color: var(--gold, #B8860B); }
.upload-icon { font-size: 36px; }
.upload-placeholder p { color: var(--text-muted, #8a7a6a); margin-top: 8px; }
.upload-hint { font-size: 12px; }
.upload-preview { position: relative; display: inline-block; max-width: 100%; }
.upload-preview img { max-height: 200px; border-radius: 4px; }
.upload-remove { position: absolute; top: -8px; right: -8px; width: 24px; height: 24px; border-radius: 50%; background: var(--red-primary, #8B2500); color: white; border: none; cursor: pointer; font-size: 16px; line-height: 24px; }
.form-actions { display: flex; gap: 12px; margin-top: 24px; }
.tip-card { padding: 24px; background: linear-gradient(135deg, #faf3e6 0%, #fff8f0 100%); }
.tip-title { font-size: 16px; color: var(--gold, #B8860B); letter-spacing: 2px; margin-bottom: 16px; }
.tip-list { list-style: none; padding: 0; }
.tip-list li { position: relative; padding-left: 16px; margin-bottom: 10px; color: var(--text-secondary, #5a4a3a); font-size: 14px; line-height: 1.6; }
.tip-list li::before { content: ""; position: absolute; left: 0; top: 8px; width: 6px; height: 6px; background: var(--gold, #B8860B); border-radius: 50%; }
@media (max-width: 768px) { .publish-layout { grid-template-columns: 1fr; } }
</style>
