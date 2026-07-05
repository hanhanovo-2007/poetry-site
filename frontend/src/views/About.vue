<template>
  <div class="page about-page">
    <h1 class="page-title">关于我们</h1>
    <p class="page-subtitle">以诗会友，传承经典</p>

    <div class="about-layout">
      <!-- 开发者信息 -->
      <div class="about-main">
        <div class="card developer-card">
          <div class="developer-avatar">戴</div>
          <h2 class="developer-name">{{ developer.name }}</h2>
          <p class="developer-role">计算机科学与技术专业 · {{ developer.grade }}</p>

          <div class="divider"></div>

          <div class="info-list">
            <div class="about-info-row">
              <span class="about-label">姓 名</span>
              <span class="about-value">{{ developer.name }}</span>
            </div>
            <div class="about-info-row">
              <span class="about-label">学 号</span>
              <span class="about-value">{{ developer.studentId }}</span>
            </div>
            <div class="about-info-row">
              <span class="about-label">邮 箱</span>
              <span class="about-value">
                <a :href="'mailto:' + developer.email">{{ developer.email }}</a>
              </span>
            </div>
            <div class="about-info-row">
              <span class="about-label">专 业</span>
              <span class="about-value">计算机科学与技术</span>
            </div>
          </div>
        </div>

        <!-- 项目介绍 -->
        <div class="card project-card">
          <h3 class="about-section-title">&#10022; 项目介绍</h3>
          <p class="about-text">
            "诗词鉴赏交流"是一个基于 Vue 3 + Django 全栈开发的诗词兴趣交流平台。
            旨在为诗词爱好者提供一个优雅、宁静的创作与交流空间。
          </p>
          <p class="about-text">
            本站涵盖诗词创作发布、作品鉴赏、互动评论等核心功能，
            并采用中国古典美学风格设计，让用户在品诗论词的同时，
            感受千年文化的厚重与雅致。
          </p>
        </div>
      </div>

      <!-- 侧边信息 -->
      <div class="about-sidebar">
        <div class="card tech-card">
          <h3 class="about-section-title">&#10022; 技术栈</h3>
          <div class="tech-list">
            <span class="tech-tag">Vue 3</span>
            <span class="tech-tag">Vite</span>
            <span class="tech-tag">Django</span>
            <span class="tech-tag">Python</span>
            <span class="tech-tag">SQLite</span>
            <span class="tech-tag">simpleui</span>
          </div>
        </div>

        <div class="card copyright-card">
          <h3 class="about-section-title">&#10022; 版权声明</h3>
          <p class="copyright-text">
            本网站为课程设计作品，所展示的诗词内容仅供学习交流使用。
            部分经典诗词引用自中国古代文学作品，版权归原作者所有。
            原创作品版权归各自作者所有。
          </p>
          <p class="copyright-text">
            未经许可，禁止将本站内容用于任何商业用途。
          </p>
          <div class="copyright-year">
            &copy; 2026 诗词鉴赏交流. All Rights Reserved.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const developer = {
  name: '戴智祺',
  studentId: '2406102312',
  email: 'hanhanpvp2007@gmail.com',
  grade: '2024级'
}
</script>

<style scoped>
.about-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
  align-items: start;
}
.developer-card {
  text-align: center;
  padding: 40px;
  background: linear-gradient(135deg, #faf3e6 0%, #fff8f0 100%);
}
.developer-avatar {
  width: 80px; height: 80px; border-radius: 50%;
  background: var(--red-primary, #8B2500);
  color: white;
  font-size: 36px;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px;
}
.developer-name {
  font-size: 24px;
  color: var(--ink-black, #2c2c2c);
  letter-spacing: 4px;
  margin-bottom: 4px;
}
.developer-role {
  font-size: 14px;
  color: var(--text-muted, #8a7a6a);
  margin-bottom: 16px;
}
.info-list { text-align: left; }
.about-info-row {
  display: flex;
  padding: 10px 0;
  border-bottom: 1px solid var(--parchment-dark, #E8D5B0);
}
.about-info-row:last-child { border-bottom: none; }
.about-label {
  width: 60px;
  color: var(--gold, #B8860B);
  font-size: 14px;
  font-weight: bold;
}
.about-value {
  flex: 1;
  color: var(--text-primary, #2c2c2c);
  font-size: 14px;
}
.about-value a { color: var(--red-primary, #8B2500); }
.project-card, .tech-card, .copyright-card {
  padding: 24px;
  margin-bottom: 20px;
}
.about-section-title {
  font-size: 16px;
  color: var(--red-primary, #8B2500);
  letter-spacing: 2px;
  margin-bottom: 16px;
}
.about-text {
  font-size: 14px;
  color: var(--text-secondary, #5a4a3a);
  line-height: 2;
  margin-bottom: 12px;
}
.tech-list { display: flex; flex-wrap: wrap; gap: 8px; }
.tech-tag {
  padding: 4px 14px;
  background: var(--parchment-light, #FAF3E6);
  border: 1px solid var(--border-color, #D4C5A9);
  border-radius: 4px;
  font-size: 13px;
  color: var(--text-secondary, #5a4a3a);
}
.copyright-text {
  font-size: 13px;
  color: var(--text-muted, #8a7a6a);
  line-height: 1.8;
  margin-bottom: 10px;
}
.copyright-year {
  margin-top: 16px;
  font-size: 12px;
  color: var(--gold, #B8860B);
  text-align: center;
  letter-spacing: 1px;
}
@media (max-width: 768px) {
  .about-layout { grid-template-columns: 1fr; }
}
</style>
