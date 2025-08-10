<script setup>
import { ref } from 'vue'

const customPath = ref('')

function sanitizePath(input) {
  if (!input) return ''
  // 去掉前后空格，移除前缀斜杠，只允许字母数字-_
  const trimmed = String(input).trim().replace(/^\/+/, '')
  const normalized = trimmed.replace(/[^a-zA-Z0-9_-]/g, '-')
  return normalized
}

function gotoHash() {
  const wanted = sanitizePath(customPath.value)
  const newHash = wanted || Math.random().toString(36).slice(2, 10)
  window.location.pathname = '/' + newHash
}
</script>

<template>
  <main class="container">
    <input
      class="path-input"
      v-model="customPath"
      placeholder="自定义路径（可选）"
      @keydown.enter="gotoHash"
    />
    <button class="goto-btn" @click="gotoHash">新建笔记</button>
  </main>
</template>

<style scoped>
.container {
  max-width: 480px;
  margin: 120px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.path-input {
  width: 100%;
  max-width: 480px;
  padding: 0.9em 1.2em;
  font-size: 1.1rem;
  border-radius: 8px;
  border: 2px solid #646cff;
  box-shadow: 0 2px 8px #646cff22;
  margin-bottom: 16px;
  outline: none;
}
.path-input:focus {
  border-color: #42b883;
  box-shadow: 0 2px 10px #42b88333;
}
.goto-btn {
  padding: 1em 2.5em;
  font-size: 1.3rem;
  border-radius: 8px;
  border: none;
  background: #646cff;
  color: #fff;
  cursor: pointer;
  box-shadow: 0 2px 8px #646cff22;
  transition: background 0.2s;
}
.goto-btn:hover {
  background: #42b883;
}
</style>
