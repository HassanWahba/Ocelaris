<template>
  <div class="Box">
    <div class="Box-header">
      <h3 class="Box-title">New Oracle EBS Connection</h3>
    </div>

    <div class="overflow-auto">
      <div class="Box-body overflow-auto">
        <form @submit.prevent="connect">
          <div class="form-group">
            <div class="form-group-header">
              <label for="hostname">Hostname</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder="erp.company.com" id="hostname"
                v-model="hostname" />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="hostname">Port</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder="8080" id="port" v-model="port" />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="database">SID</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" id="sid" v-model="sid" />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="username">Username</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" id="username" v-model="username" />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="password">Password</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="password" id="password" v-model="password" />
            </div>
          </div>

          <div class="form-group-body">
            <div class="form-group-header">
              <label for="db_type" class="required">Database</label>
            </div>
            <select class="form-select element-drop" id="db_type" v-model="db_type">
              <option disabled value="">Please select...</option>
              <option v-for="item in this.supported" :value="item" :key="item">{{ item }}</option>
            </select>
          </div>

        </form>
      </div>
      <div class="Box-footer">
        <button class="btn btn-primary width-full mr-1" @click="send_connection"><i class="fas fa-check-circle"></i>
          Connect </button>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "oracle",
  data() {
    return {
      hostname: '',
      port: '',
      sid: '',
      username: '',
      password: '',
      db_type: '',
      erp_type: '',
      error: null,
    }
  },
  computed: {
    ...mapGetters('connection', ['supported'])
  },
  methods: {
    ...mapActions('connection', ['connect']),
    send_connection() {
      this.connect({
        hostname: this.hostname,
        port: this.port,
        sid: this.sid,
        username: this.username,
        password: this.password,
        db_type: this.db_type,
        erp_type: this.erp_type,
      })
        .then(() => {
          this.$emit('created');
        })
        .catch(e => {
          this.error = e.message;
        });
    },
  },
};
</script>

<style scoped></style>
