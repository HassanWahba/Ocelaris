<template>
  <div class="height-full d-flex flex-items-center flex-justify-center">
    <div class="blankslate card border-0 shadow p-3 bg-light" v-if="!isConnected">
      <div class="text-center info-container">
        <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" fill="black"
          class="bi bi-database-fill-add mb-3" viewBox="0 0 16 16">
          <path
            d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Zm.5-5v1h1a.5.5 0 0 1 0 1h-1v1a.5.5 0 0 1-1 0v-1h-1a.5.5 0 0 1 0-1h1v-1a.5.5 0 0 1 1 0ZM8 1c-1.573 0-3.022.289-4.096.777C2.875 2.245 2 2.993 2 4s.875 1.755 1.904 2.223C4.978 6.711 6.427 7 8 7s3.022-.289 4.096-.777C13.125 5.755 14 5.007 14 4s-.875-1.755-1.904-2.223C11.022 1.289 9.573 1 8 1Z" />
          <path
            d="M2 7v-.839c.457.432 1.004.751 1.49.972C4.722 7.693 6.318 8 8 8s3.278-.307 4.51-.867c.486-.22 1.033-.54 1.49-.972V7c0 .424-.155.802-.411 1.133a4.51 4.51 0 0 0-4.815 1.843A12.31 12.31 0 0 1 8 10c-1.573 0-3.022-.289-4.096-.777C2.875 8.755 2 8.007 2 7Zm6.257 3.998L8 11c-1.682 0-3.278-.307-4.51-.867-.486-.22-1.033-.54-1.49-.972V10c0 1.007.875 1.755 1.904 2.223C4.978 12.711 6.427 13 8 13h.027a4.552 4.552 0 0 1 .23-2.002Zm-.002 3L8 14c-1.682 0-3.278-.307-4.51-.867-.486-.22-1.033-.54-1.49-.972V13c0 1.007.875 1.755 1.904 2.223C4.978 15.711 6.427 16 8 16c.536 0 1.058-.034 1.555-.097a4.507 4.507 0 0 1-1.3-1.905Z" />
        </svg>
        <h3 class="mb-1">Choose an ERP System...</h3>
      </div>
    </div>
    <div class="card border-0 shadow p-3 bg-light" v-else>
      <div class="text-center info-container">
        <h3 class="mb-3">You are connected to an ERP System.</h3>
        <p v-if="connectionDetails" class="mb-3">
          <strong>Hostname:</strong> {{ connectionDetails.hostname }}<br>
          <strong>Port:</strong> {{ connectionDetails.port }}<br>
          <strong>Database:</strong> {{ connectionDetails.sid }}<br>
          <strong>Username:</strong> {{ connectionDetails.username }}
        </p>
        <button @click="disconnect" class="btn btn-danger">
          <i class="far fa-trash-alt"></i> Disconnect
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConnectionInfo',
  computed: {
    connectionDetails() {
      return this.$store.state.connection.details;
    },
    isConnected() {
      return this.$store.state.connection.status === 'connected';
    }
  },
  methods: {
    disconnect() {
      this.$store.dispatch('connection/disconnect');
      this.$emit('disconnected');
    }
  }
};
</script>

<style scoped>
.height-full {
  height: 100vh;
  justify-content: center;
  align-items: center;
  display: flex;
}

.blankslate,
.card {
  width: 100%;
  max-width: 400px;
}


.btn-danger:hover {
  background-color: #ff3b30;
  opacity: 0.8;
}

.bi-database-fill-add {
  color: #007bff;
}

.info-container {
  display: flex;
  justify-content: center;
  flex-direction: column;
  height: calc(70vh - 60px);
  align-items: center;
}
</style>
