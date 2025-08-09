<script setup>
function gotoHash() {
  const newHash = Math.random().toString(36).slice(2, 10)
  window.location.pathname = '/' + newHash
}
</script>

<template>
  <main class="container">
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
