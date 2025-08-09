<script setup>
import { ref } from 'vue'
import NoteEditor from './components/NoteEditor.vue'
import NoteEntry from './components/NoteEntry.vue'

const hash = ref('')
if (window.location.pathname.match(/\/([^\/]+)$/)) {
  hash.value = window.location.pathname.split('/').pop()
}
</script>


<template>
  <NoteEditor v-if="hash" />
  <NoteEntry v-else />
</template>


<style scoped>
/* 样式已移至各自组件 */
</style>
