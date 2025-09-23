<script setup lang="ts">
import { ref, onBeforeUnmount } from "vue";

const videoRef = ref<HTMLVideoElement | null>(null);
const previewUrl = ref<string | null>(null);
const fileBlob = ref<Blob | null>(null);
let stream: MediaStream | null = null;
const isCameraOn = ref(false);

const toggleCamera = async () => {
  if (isCameraOn.value) {
    stopCamera();
    return;
  }

  clearPreview();

  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    if (videoRef.value) {
      videoRef.value.srcObject = stream;
      await videoRef.value.play();
      isCameraOn.value = true;
    }
  } catch (err) {
    console.error("Ошибка доступа к камере:", err);
    isCameraOn.value = false;
  }
};

const stopCamera = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
  }
  if (videoRef.value) videoRef.value.srcObject = null;
  isCameraOn.value = false;
};

const capturePhoto = () => {
  if (!videoRef.value) return;
  const canvas = document.createElement("canvas");
  canvas.width = videoRef.value.videoWidth;
  canvas.height = videoRef.value.videoHeight;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  ctx.drawImage(videoRef.value, 0, 0, canvas.width, canvas.height);
  canvas.toBlob(blob => {
    if (blob) {
      fileBlob.value = blob;
      previewUrl.value = URL.createObjectURL(blob);
      stopCamera();
    }
  }, "image/png");
};

const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (!input.files || !input.files[0]) return;

  const file = input.files[0];
  stopCamera();
  clearPreview();

  fileBlob.value = file;
  previewUrl.value = URL.createObjectURL(file);
};

const clearPreview = () => {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
  previewUrl.value = null;
  fileBlob.value = null;
  stopCamera();
};

onBeforeUnmount(() => stopCamera());
</script>

<template>
  <main class="main-block">
    <button @click="toggleCamera" class="btn">
      {{ isCameraOn ? "Выключить камеру" : "Включить камеру" }}
    </button>

    <video
      ref="videoRef"
      autoplay
      playsinline
      v-show="isCameraOn"
      class="camera-video">
    </video>

    <div v-if="isCameraOn" class="camera-actions">
      <button @click="capturePhoto" class="btn btn-green">Сделать фото</button>
    </div>

    <input type="file" accept="image/*,video/*" @change="handleFileChange" class="file-input" />

    <div v-if="previewUrl" class="preview">
      <p>Предпросмотр:</p>
      <img v-if="fileBlob && fileBlob.type.startsWith('image')" :src="previewUrl" />
      <video v-else controls autoplay loop :src="previewUrl"></video>
    </div>

    <button v-if="previewUrl || isCameraOn" @click="clearPreview" class="btn btn-red">Удалить</button>
  </main>
</template>

<style scoped>
.main-block {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 500px;
  margin: 0 auto;
  padding: 1rem;
}

video, img {
  max-width: 100%;
  border: 2px solid #ddd;
  border-radius: 8px;
  background: #000;
}

.preview {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.file-input {
  margin-top: 0.5rem;
}

.btn-green {
  background: #2ecc71;
}

.btn-green:hover {
  background: #27ae60;
}

.btn-red {
  background: #b65959;
}

.btn-red:hover {
  background: #b65959;
}
</style>
