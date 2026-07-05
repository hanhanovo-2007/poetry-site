<template>
  <div class="page">
    <!-- ===== 轮播区 ===== -->
    <section class="hero-section">
      <div class="carousel" @mouseenter="pauseCarousel" @mouseleave="startCarousel">
        <div
          v-for="(slide, index) in carouselSlides"
          :key="index"
          class="carousel-slide"
          :class="{ active: currentSlide === index }"
          :style="{ backgroundImage: slide.bg }"
        >
          <div class="slide-overlay"></div>
          <div class="slide-location-label">{{ slide.location }}</div>
          <div class="slide-content">
            <p class="slide-poem">{{ slide.poem }}</p>
            <p class="slide-author">—— {{ slide.author }} ——</p>
          </div>
        </div>
        <div class="carousel-dots">
          <span
            v-for="(_, index) in carouselSlides"
            :key="index"
            class="dot"
            :class="{ active: currentSlide === index }"
            @click="currentSlide = index"
          ></span>
        </div>
      </div>
      <div class="carousel-subtitle">摄影地：江西 · 望仙谷 / 婺源 / 卧龙谷</div>
    </section>

    <div class="divider"></div>

    <!-- ===== 千古名句 ===== -->
    <section class="quote-section">
      <h2 class="section-title">千古名句</h2>
      <p class="section-desc">穿越千年的文字，依然动人心弦</p>
      <div class="quote-grid">
        <div v-for="(item, index) in famousQuotes" :key="index" class="quote-card card">
          <div class="quote-badge">{{ index + 1 }}</div>
          <p class="quote-text">{{ item.quote }}</p>
          <p class="quote-source">—— {{ item.source }}</p>
          <a :href="item.link" target="_blank" class="quote-link">查看全文 &rarr;</a>
        </div>
      </div>
    </section>

    <div class="divider"></div>

    <!-- ===== 古代佳作一览 ===== -->
    <section class="masterpiece-section">
      <h2 class="section-title">古代佳作一览</h2>
      <p class="section-desc">点选任意作品，可跳转百度百科查阅详情</p>
      <div class="masterpiece-list">
        <a
          v-for="(work, index) in masterpieces"
          :key="index"
          :href="work.link"
          target="_blank"
          class="masterpiece-item card"
        >
          <span class="masterpiece-era">{{ work.era }}</span>
          <div class="masterpiece-info">
            <h3 class="masterpiece-title">{{ work.title }}</h3>
            <p class="masterpiece-author">{{ work.author }}</p>
          </div>
          <p class="masterpiece-excerpt">{{ work.excerpt }}</p>
          <span class="masterpiece-arrow">&rarr;</span>
        </a>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const currentSlide = ref(0)
let timer = null

const carouselSlides = [
  {
    poem: '欲买桂花同载酒，终不似，少年游',
    author: '刘过《唐多令》',
    location: '江西 · 望仙谷',
    bg: 'url(https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1400&q=85)'
  },
  {
    poem: '胭脂泪，相留醉，几时重。自是人生长恨水长东',
    author: '李煜《相见欢》',
    location: '江西 · 望仙谷',
    bg: 'url(https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1400&q=85)'
  },
  {
    poem: '红藕香残玉簟秋。轻解罗裳，独上兰舟',
    author: '李清照《一剪梅》',
    location: '江西 · 卧龙谷',
    bg: 'url(https://images.unsplash.com/photo-1444464666168-49d633b8672b?w=1400&q=85)'
  },
  {
    poem: '最是人间留不住，朱颜辞镜花辞树',
    author: '王国维《蝶恋花》',
    location: '江西 · 婺源',
    bg: 'url(https://images.unsplash.com/photo-1504198266287-1659872e6590?w=1400&q=85)'
  },
  {
    poem: '为天地立心，为生民立命，\n为往圣继绝学，为万世开太平',
    author: '张载《横渠四句》',
    location: '江西 · 望仙谷',
    bg: 'url(https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1400&q=85)'
  },
  {
    poem: '问君能有几多愁？恰似一江春水向东流',
    author: '李煜《虞美人》',
    location: '江西 · 婺源',
    bg: 'url(https://images.unsplash.com/photo-1528164344705-47542687000d?w=1400&q=85)'
  },
  {
    poem: '春花秋月何时了，往事知多少',
    author: '李煜《虞美人》',
    location: '江西 · 卧龙谷',
    bg: 'url(https://images.unsplash.com/photo-1518173946687-a36f968f7e89?w=1400&q=85)'
  }
]

const famousQuotes = [
  {
    quote: '一重山，两重山。山远天高烟水寒，相思枫叶丹',
    source: '李煜《长相思》',
    link: 'https://www.baidu.com/s?wd=李煜+长相思+一重山'
  },
  {
    quote: '多情自古伤离别，更那堪冷落清秋节',
    source: '柳永《雨霖铃》',
    link: 'https://www.baidu.com/s?wd=柳永+雨霖铃'
  },
  {
    quote: '此情无计可消除，才下眉头，却上心头',
    source: '李清照《一剪梅》',
    link: 'https://www.baidu.com/s?wd=李清照+一剪梅'
  },
  {
    quote: '剪不断，理还乱，是离愁。别是一般滋味在心头',
    source: '李煜《相见欢》',
    link: 'https://www.baidu.com/s?wd=李煜+相见欢+无言独上西楼'
  },
  {
    quote: '衣带渐宽终不悔，为伊消得人懴悴',
    source: '柳永《蝶恋花》',
    link: 'https://www.baidu.com/s?wd=柳永+蝶恋花'
  },
  {
    quote: '旧江山浑是新愁。欲买桂花同载酒，终不似，少年游',
    source: '刘过《唐多令》',
    link: 'https://www.baidu.com/s?wd=刘过+唐多令'
  },
  {
    quote: '众里寻他千百度，蓦然回首，那人却在灯火阑珊处',
    source: '辛弃疾《青玉案·元夕》',
    link: 'https://www.baidu.com/s?wd=辛弃疾+青玉案+元夕'
  },
  {
    quote: '千锤万砌出深山，烈火焚烧若等闲。粉骨碎身浑不怕，要留清白在人间',
    source: '于谦《石灰吟》',
    link: 'https://www.baidu.com/s?wd=于谦+石灰吟'
  }
]

const masterpieces = [
  {
    title: '《虞美人》', author: '李煜', era: '五代',
    excerpt: '春花秋月何时了，往事知多少。小楼昨夜又东风，故国不堪回首月明中',
    link: 'https://www.baidu.com/s?wd=李煜+虞美人+春花秋月何时了'
  },
  {
    title: '《相见欢·林花谢了春红》', author: '李煜', era: '五代',
    excerpt: '林花谢了春红，太匆匆。无奈朝来寒雨晚来风。胭脂泪，相留醉',
    link: 'https://www.baidu.com/s?wd=李煜+相见欢+林花谢了春红'
  },
  {
    title: '《长相思·一重山》', author: '李煜', era: '五代',
    excerpt: '一重山，两重山。山远天高烟水寒，相思枫叶丹。菊花开，菊花残',
    link: 'https://www.baidu.com/s?wd=李煜+长相思+一重山'
  },
  {
    title: '《声声慢》', author: '李清照', era: '宋',
    excerpt: '寻寻密密，冷冷清清，凄凄惨惨戚戚。乍暖还寒时候，最难将息',
    link: 'https://www.baidu.com/s?wd=李清照+声声慢+寻寻密密'
  },
  {
    title: '《一剪梅》', author: '李清照', era: '宋',
    excerpt: '红藕香残玉簟秋。轻解罗裳，独上兰舟。云中谁寄锦书来，雁字回时',
    link: 'https://www.baidu.com/s?wd=李清照+一剪梅+红藕香残玉簟秋'
  },
  {
    title: '《雨霖铃》', author: '柳永', era: '宋',
    excerpt: '寒蟑凄切，对长亭晚，骤雨初止。都门帐饮无绪，留恋处，兰舟催发',
    link: 'https://www.baidu.com/s?wd=柳永+雨霖铃+寒蟑凄切'
  },
  {
    title: '《蝶恋花》', author: '柳永', era: '宋',
    excerpt: '伱依危楼风细细，望极春愁，黯黯生天际。草色烟光残照里，无言谁会凭栏意',
    link: 'https://www.baidu.com/s?wd=柳永+蝶恋花+伱依危楼风细细'
  },
  {
    title: '《唐多令》', author: '刘过', era: '宋',
    excerpt: '芦叶满汀洲，寒沙带浅流。二十年重过南楼。柳下系舟犹未稳，能几日，又中秋',
    link: 'https://www.baidu.com/s?wd=刘过+唐多令+芦叶满汀洲'
  },
  {
    title: '《蝶恋花》', author: '王国维', era: '近代',
    excerpt: '阅尽天涯离别苦，不道归来，零落花如许。花底相看无一语，绿窗春与天俱莫',
    link: 'https://www.baidu.com/s?wd=王国维+蝶恋花+阅尽天涯离别苦'
  },
  {
    title: '《石灰吟》', author: '于谦', era: '明',
    excerpt: '千锤万砌出深山，烈火焚烧若等闲。粉骨碎身浑不怕，要留清白在人间',
    link: 'https://www.baidu.com/s?wd=于谦+石灰吟'
  },
  {
    title: '《青玉案·元夕》', author: '辛弃疾', era: '宋',
    excerpt: '东风夜放花千树，更吹落、星如雨。宝马雕车香满路。凤箫声动，玉壶光转',
    link: 'https://www.baidu.com/s?wd=辛弃疾+青玉案+元夕'
  },
  {
    title: '《丑奴儿·书博山道中壁》', author: '辛弃疾', era: '宋',
    excerpt: '少年不识愁滋味，爱上层楼。爱上层楼，为赋新词强说愁。而今识尽愁滋味',
    link: 'https://www.baidu.com/s?wd=辛弃疾+丑奴儿+书博山道中壁'
  }
]

function nextSlide() {
  currentSlide.value = (currentSlide.value + 1) % carouselSlides.length
}

function pauseCarousel() { clearInterval(timer) }
function startCarousel() { timer = setInterval(nextSlide, 5000) }

onMounted(() => startCarousel())
onUnmounted(() => clearInterval(timer))
</script>

<style scoped>
.hero-section { margin-bottom: 40px; }
.carousel {
  position: relative; width: 100%; height: 460px;
  border-radius: 8px; overflow: hidden; cursor: pointer;
}
.carousel-slide {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  opacity: 0; transition: opacity 1.0s ease;
  background-size: cover !important; background-position: center !important;
}
.carousel-slide.active { opacity: 1; }
.slide-overlay {
  position: absolute; inset: 0;
  background: rgba(0, 0, 0, 0.40);
}
.slide-location-label {
  position: absolute; top: 20px; right: 24px;
  z-index: 3;
  font-size: 12px; color: rgba(255,255,255,0.6);
  letter-spacing: 2px;
  padding: 4px 12px;
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 3px;
  backdrop-filter: blur(4px);
  background: rgba(0,0,0,0.2);
}
.slide-content {
  position: relative; z-index: 2; text-align: center;
  padding: 40px; max-width: 820px;
}
.slide-poem {
  font-size: 30px; color: var(--parchment, #F5E6CC);
  line-height: 2; letter-spacing: 4px;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.6);
  margin-bottom: 20px;
  white-space: pre-line;
}
.slide-author {
  font-size: 16px; color: var(--gold, #B8860B); letter-spacing: 3px;
}
.carousel-dots {
  position: absolute; bottom: 24px; left: 50%;
  transform: translateX(-50%); display: flex; gap: 10px; z-index: 3;
}
.dot {
  width: 10px; height: 10px; border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  cursor: pointer; transition: all 0.3s;
}
.dot.active {
  background: var(--gold, #B8860B);
  width: 28px; border-radius: 5px;
}
.carousel-subtitle {
  text-align: center;
  font-size: 12px; color: var(--text-muted, #8a7a6a);
  letter-spacing: 2px; margin-top: 12px;
}
.section-title {
  font-size: 28px; color: var(--ink-black, #2c2c2c);
  text-align: center; letter-spacing: 5px; margin-bottom: 8px;
}
.section-desc {
  font-size: 14px; color: var(--text-muted, #8a7a6a);
  text-align: center; letter-spacing: 2px; margin-bottom: 32px;
}
.quote-section { margin-bottom: 40px; }
.quote-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
.quote-card {
  position: relative; padding: 28px 24px 24px;
  background: linear-gradient(135deg, #faf3e6 0%, #fff8f0 100%);
}
.quote-badge {
  position: absolute; top: -10px; left: 20px;
  width: 32px; height: 32px; border-radius: 50%;
  background: var(--red-primary, #8B2500); color: white;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: bold;
}
.quote-text {
  font-size: 20px; color: var(--text-primary, #2c2c2c);
  line-height: 2; margin-bottom: 12px; letter-spacing: 1px;
}
.quote-source { font-size: 14px; color: var(--gold, #B8860B); margin-bottom: 12px; }
.quote-link { font-size: 13px; color: var(--red-primary, #8B2500); }
.quote-link:hover { color: var(--red-light, #C41A1A); }
.masterpiece-section { margin-bottom: 40px; }
.masterpiece-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 16px;
}
.masterpiece-item {
  display: flex; align-items: center; gap: 16px;
  padding: 18px 20px; background: white; cursor: pointer;
  transition: all 0.2s;
}
.masterpiece-item:hover {
  background: var(--parchment-light, #FAF3E6);
  border-color: var(--gold, #B8860B);
}
.masterpiece-era {
  font-size: 12px; color: white;
  background: var(--red-primary, #8B2500);
  padding: 2px 10px; border-radius: 3px; white-space: nowrap;
}
.masterpiece-info { flex: 0 0 auto; }
.masterpiece-title {
  font-size: 18px; color: var(--ink-black, #2c2c2c); letter-spacing: 2px;
}
.masterpiece-author { font-size: 12px; color: var(--text-muted, #8a7a6a); }
.masterpiece-excerpt {
  flex: 1; font-size: 14px; color: var(--text-secondary, #5a4a3a);
  line-height: 1.6; overflow: hidden;
  text-overflow: ellipsis; white-space: nowrap;
}
.masterpiece-arrow {
  color: var(--border-color, #D4C5A9);
  font-size: 20px; transition: transform 0.2s;
}
.masterpiece-item:hover .masterpiece-arrow {
  transform: translateX(4px); color: var(--gold, #B8860B);
}
@media (max-width: 768px) {
  .carousel { height: 320px; }
  .slide-poem { font-size: 22px; }
  .quote-grid, .masterpiece-list { grid-template-columns: 1fr; }
}
</style>
