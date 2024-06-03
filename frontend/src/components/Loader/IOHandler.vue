<template>
  <div>
    <div class="Subhead">
      <div class="Subhead-heading">{{ display }}</div>
      <div class="Subhead-description"></div>
    </div>
    <div v-if="hasInput.includes(display)">
      <div class="mb-3">
        <div class="form-group form-group-header">
          <label for="switch-text">Import {{ display }} File</label>
        </div>
        <input type="file" id="file" ref="file" @change="handleFileUpload()" />
      </div>
      <button class="btn btn-primary" @click="submitFile">Import</button>
      <button v-if="file" class="btn btn-danger" @click="clearFile">Delete File</button>
      <hr />
    </div>
    <div class="form-group">
      <div class="form-group-header">
        <label for="switch-text">Export {{ display }} File</label>
      </div>

      <div class="form-group">
        <div v-if="hasInput.includes(display) & display !== 'Database'" class="form-group-body">
          <select class="form-select element-drop" style="width: 200pt;" id="selectedOption" v-model="selectedOption">
            <option disbaled value="">Please Select ...</option>
            <option v-for="item in filtered" :value="item.id">{{ item.meta.name }}</option>
          </select>
          <button class="btn" @click.prevent="addOption"><i class="fas fa-check-circle"></i></button>
          <a @click="handleExport" class="btn btn-primary">Export</a>
        </div>
        <div v-else-if="display == 'Database'" class="form-group-body">
          <a @click="getOCDMSnapshot" class="btn btn-primary">Object Centric Data Model Snapshot</a>
        </div>
        <div v-else-if="display == 'OCEL'" class="form-group-body">
          <select class="form-select element-drop" style="width: 200pt;" id="selectedOption" v-model="selectedOption">
            <option disbaled value="">Please Select ...</option>
            <option v-for="item in filtered" :value="item.id">{{ item.meta.name }}</option>
          </select>
          <br> <br>
          <a @click="getSQLiteOCEL" class="btn btn-primary">Export SQLite</a>
        </div>
        <div v-else class="form-group-body">
          <a @click="getDBSnapshot" class="btn btn-primary">Export</a>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "IOHandler",
  props: {
    display: {
      type: String,
      default: 'OCEL'
    }
  },
  data() {
    return {
      file: null,
      hasInput: ['Event', 'Object', 'Process', 'Database'],
      selectedOption: '',
      options: []
    };
  },
  computed: {
    ...mapState("events", ['events']),
    ...mapState("objects", ['objects']),
    ...mapState("processes", ['processes']),
    ...mapState("io", ['error']),
    filtered() {
      let list = [];
      switch (this.display) {
        case "Event":
          list = this.events;
          break;
        case "Object":
          list = this.objects;
          break;
        case "Process":
          list = this.processes;
          break;
        case "OCEL":
          list = this.processes;
          break;
      }
      return list;
    }
  },
  methods: {
    ...mapActions("io", ["exportDBSnapshot", "importDBSnapshot", "exportSQLiteOCEL"]),
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
      let formData = new FormData();
      formData.append('file', this.file);
      this.$api.post('api/processes/import-db-snapshot', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
      })
        .then(() => {
          this.$notify.success('File upload was successful.');
        })
        .catch(err => {
          this.$notify.error('File upload failed: ' + err.response.data);
        });
    },
    clearFile() {
      this.$refs.file.value = '';
      this.file = null;
    },
    submitFile() {
      if (!this.file) {
        return;
      }

      let formData = new FormData();
      formData.append('file', this.file);

      this.$api
        .post(`api/import-${this.display.toLowerCase()}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
        })
        .then(() => {
          this.clearFile();
          this.$notify.success(`Import of ${this.display} was successful.`);
          this.$emit('imported');
        })
        .catch(err => {
          this.$notify.error(`Import of ${this.display} failed: ` + err.response.data);
        });
    },
    handleExport() {
      let subLink = ''
      switch (this.display) {
        case "Process":
          subLink = 'processes'
          break;
        case "Object":
          subLink = 'objects'
          break;
        case "Event":
          subLink = 'events'
          break;
      }
      this.$api
        .get(`api/${subLink}/export`, { responseType: 'blob' })
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', `${this.display}.sqlite3`);
          document.body.appendChild(link);
          link.click();
        })
        .catch(err => {
          this.$notify.error(`Export of ${this.display} failed: ` + err.response.data);
        });
    },
    async getSQLiteOCEL() {
      if (!this.selectedOption) {
        this.$notify.error('Please select a process.');
        return;
      }
      const data = await this.exportSQLiteOCEL(this.selectedOption)
      const url = window.URL.createObjectURL(new Blob([data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${this.display}.sqlite3`);
      document.body.appendChild(link);
      link.click();
      console.log(url)
    },
    async getOCDMSnapshot() {
      try {
        const data = await this.exportDBSnapshot();
        const url = window.URL.createObjectURL(new Blob([data], { type: 'application/octet-stream' }));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${this.display}.db`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        console.log(url);
      } catch (error) {
        console.error('Error exporting database:', error);
      }
    },
  },
};
</script>

<style scoped></style>