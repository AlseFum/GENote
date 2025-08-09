import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

createApp(App).mount('#app')

import {parse} from "./genlang/genlang.js"
window.parse=parse;