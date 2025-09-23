<script setup lang="ts">
import { ref, onBeforeUnmount } from "vue";

const videoRef = ref<HTMLVideoElement | null>(null);
const inputRef = ref<HTMLInputElement | null>(null);
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

const uploadFile = async () => {
  if (!fileBlob.value) {
    console.error("Нет файла для отправки!");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileBlob.value, "upload.png");

  console.log(fileBlob.value);
};

onBeforeUnmount(() => stopCamera());
</script>

<template>
  <main class="container main-block">
    <div class="controls">
      <button @click="toggleCamera" class="btn">
        {{ isCameraOn ? "Выключить камеру" : "Включить камеру" }}
      </button>

      <input
        ref="inputRef"
        type="file"
        accept="image/*,video/*"
        @change="handleFileChange"
        class="file-input"
      />
    </div>

    <div
      class="preview-area"
      :class="{ 'with-media': isCameraOn || previewUrl }"
    >
      <div v-if="!isCameraOn && !previewUrl" class="placeholder">
        <p>Выберите файл или включите камеру</p>
      </div>

      <video
        v-show="isCameraOn"
        ref="videoRef"
        autoplay
        playsinline
        class="preview-media"
      />
      <img
        v-if="previewUrl && fileBlob?.type.startsWith('image') && !isCameraOn"
        :src="previewUrl"
        class="preview-media"
        alt="image"
      />
      <video
        v-else-if="previewUrl && !isCameraOn"
        controls
        autoplay
        loop
        :src="previewUrl"
        class="preview-media"
      />
    </div>

    <div class="camera-actions" v-if="isCameraOn || previewUrl">
      <button v-if="isCameraOn" @click="capturePhoto" class="btn btn-green">
        Сделать фото
      </button>
      <button @click="clearPreview" class="btn btn-red">
        Удалить файл
      </button>
      <button v-if="fileBlob" @click="uploadFile" class="btn btn-blue">
        Отправить на сервер
      </button>
    </div>
  </main>
</template>

<style scoped>
.main-block {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.controls {
  max-width: 600px;
  padding: 1.5rem;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin: 0 auto;
  justify-content: center;
}

.preview-area {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  border: 2px dashed #ccc;
  border-radius: 12px;
  background: #fafafa;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  min-height: 450px;
  transition: all 0.3s ease;
}

.preview-area.with-media {
  min-height: auto;
  height: auto;
  border-style: solid;
}

.preview-media {
  max-width: 100%;
  max-height: 550px;
  object-fit: contain;
  border-radius: 12px;
}

.placeholder {
  color: #888;
  font-size: 1rem;
  text-align: center;
  padding: 2rem;
}

.camera-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn-green {
  background: #2ecc71;
  color: #fff;
}

.btn-green:hover {
  background: #27ae60;
}

.btn-red {
  background: #e74c3c;
  color: #fff;
}

.btn-red:hover {
  background: #c0392b;
}

.btn-blue {
  background: #3498db;
  color: #fff;
}

.btn-blue:hover {
  background: #2980b9;
}

.file-input {
  padding: 0.4rem;
}
</style>
