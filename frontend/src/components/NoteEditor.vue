<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
const title = ref(window.location.pathname)
const content = ref('')
const hash = ref('')
// 四态 + 额外错误态：
// idle(无改动) / saving(有改动等待上传) / saved_recent(正常文本已上传5秒内) / gen_saved(生成器文本已上传) / error
const SS={
    Idle:"idle",
    SAVING:'saving',
    SAVED_RECENT:'saved_recent',
    GEN_SAVED:'gen_saved',
    ERROR:'error'
}
const saveStatus = ref(SS.Idle)
let savedRecentTimer = null
const lastSavedContent = ref('')

function getHashFromPath() {
    const m = window.location.pathname.match(/\/([^\/]+)$/)
    return m ? m[1] : ''
}

function loadNote() {
    if (!hash.value) return
    fetch(`/api/${hash.value}`)
        .then(res => res.json())
        .then(data => {
            content.value = data.content || ''
            lastSavedContent.value = content.value
            saveStatus.value = SS.Idle
            console.log('内容已加载')
        })
        .catch(e => {
            console.error('加载失败', e)
        })
}

// 监听 path 变化
function handlePathChange() {
    hash.value = getHashFromPath()
    loadNote()
}

onMounted(() => {
    handlePathChange()
    window.addEventListener('popstate', handlePathChange)
    window.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
    window.removeEventListener('popstate', handlePathChange)
    window.removeEventListener('keydown', handleKeydown)
})

// 监听 hash 变化（如通过跳转按钮）
watch(hash, () => {
    loadNote()
})

// 节流函数
function throttle(fn, delay) {
    let timer = null
    let lastArgs = null
    return function (...args) {
        lastArgs = args
        if (!timer) {
            timer = setTimeout(() => {
                fn(...lastArgs)
                timer = null
            }, delay)
        }
    }
}

// 保存内容到后端
async function saveNote() {
    if (!hash.value) return
    let payload = { content: content.value }
    saveStatus.value = 'saving'
    try {
        // 尝试 parse
        if (window.parse) {
            try {
                const gen = window.parse(content.value)
                payload.gen = gen;
                console.log("Generated Generator");
                console.log(gen);
            } catch (e) {
            }
        }
        await fetch(`/api/${hash.value}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        lastSavedContent.value = content.value
        // 生成器文本优先显示专用态；否则显示5秒“已上传”态
        if (payload.gen) {
            saveStatus.value = SS.GEN_SAVED
        } else {
            saveStatus.value = SS.SAVED_RECENT
            if (savedRecentTimer) clearTimeout(savedRecentTimer)
            savedRecentTimer = setTimeout(() => {
                // 若这段时间内没有新的改动，则回到无改动态
                if (content.value === lastSavedContent.value && saveStatus.value === 'saved_recent') {
                    saveStatus.value = SS.Idle
                }
            }, 5000)
        }

    } catch (e) {
        saveStatus.value = SS.ERROR
        console.error("保存失败", e)
    }
}

const throttledSave = throttle(saveNote, 5000)
watch(content, () => {
    saveStatus.value = SS.SAVING
    throttledSave();
})

function handleKeydown(e) {
    // Ctrl+S 或 Cmd+S 立即保存
    const isSaveHotkey = (e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S')
    if (isSaveHotkey) {
        e.preventDefault()
        saveNote()
    }
}
</script>

<template>
    <main class="container">
        <div class="save-status-fixed">
            <template v-if="saveStatus === SS.Idle">
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                    <circle cx="9" cy="9" r="8" stroke="#9aa0a6" stroke-width="2" />
                </svg>
            </template>
            <template v-else-if="saveStatus === SS.SAVING">
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                    <circle cx="9" cy="9" r="8" stroke="#646cff" stroke-width="2" />
                    <path d="M9 4v5l3 3" stroke="#646cff" stroke-width="2" fill="none" />
                </svg>
            </template>
            <template v-else-if="saveStatus === SS.SAVED_RECENT">
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                    <circle cx="9" cy="9" r="8" stroke="#42b883" stroke-width="2" />
                    <path d="M5 9l2.5 2.5L13 6" stroke="#42b883" stroke-width="2" fill="none" />
                </svg>
            </template>
            <template v-else-if="saveStatus === SS.GEN_SAVED">
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                    <circle cx="9" cy="9" r="8" stroke="#10b981" stroke-width="2" />
                    <path d="M6 9h6M9 6v6" stroke="#10b981" stroke-width="2" />
                </svg>
            </template>
            <template v-else-if="saveStatus === SS.ERROR">
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                    <circle cx="9" cy="9" r="8" stroke="#ff4d4f" stroke-width="2" />
                    <path d="M6 6l6 6M12 6l-6 6" stroke="#ff4d4f" stroke-width="2" />
                </svg>
            </template>
        </div>
        <h1>{{ title }}</h1>
        <div class="dashed-divider"></div>
        <textarea v-model="content" placeholder="请输入内容..." rows="16" class="note-textarea"></textarea>
    </main>
</template>

<style scoped>
.save-status-fixed {
    position: fixed;
    right: 16px;
    top: 16px;
    z-index: 100;
    background: #fff;
    border-radius: 50%;
    width: 22px;
    height: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px #0001;
    pointer-events: none;
    user-select: none;
}

.dashed-divider {
    width: 90vw;
    max-width: 700px;
    border-bottom: 2px dashed #bbb;
    margin: 0 auto 24px auto;
}

h1 {
    font-size: 2rem;
    margin-bottom: 1.5rem;
    color: #646cff;
}

.container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    justify-content: flex-start;
    background: #fff;
    box-sizing: border-box;
    padding: 0;
}

h1 {
    font-size: 2rem;
    margin-bottom: 1.5rem;
    color: #646cff;
}

.note-textarea {
    width: calc(100vw - 48px);
    height: calc(100vh - 120px);
    min-height: 400px;
    font-size: 1.2rem;
    padding: 1.5em;
    border: none;
    border-radius: 0;
    resize: none;
    box-sizing: border-box;
    background: transparent;
    color: #222;
    margin: 0 auto;
    box-shadow: none;
}

.note-textarea:focus {
    outline: none;
}
</style>
