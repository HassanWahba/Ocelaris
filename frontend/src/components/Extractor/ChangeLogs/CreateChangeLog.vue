<template>
  <div class="Box">
    <div class="Box-header">
      <h3 class="Box-title">Create a New Change Log Table</h3>
    </div>

    <form>
      <div class="overflow-auto">
        <div class="Box-body overflow-auto">

          <div class="form-group">
            <div class="form-group-header">
              <label for="name" class="required">Change Log Name</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder='e.g. Change Log for P2P' id="name"
                v-model="name" required />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="source" class="required">Source Table</label>
            </div>
            <div class="form-group-body">
              <input class="form-control" style="width: 10%;" type="text" placeholder='' id="owner" v-model="owner"
                required />.
              <input class="form-control" style="width: 88.8%;" type="text" placeholder='' id="table" v-model="table"
                required />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="condition">Condition</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder='' id="condition" v-model="condition" />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="targetTable" class="required">Document ID Column</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder="" id="targetTable" v-model="targetTable"
                required />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="timestamp" class="required">Timestamp Column</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder="" id="timestamp" v-model="timestamp"
                required />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="attributes" class="">Other Attributes' Columns</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder="separated by a comma" id="attributes"
                v-model="attributes" required />
            </div>
          </div>

        </div>
      </div>
    </form>

    <div class="Box-footer">
      <button v-if="id == -1" class="btn btn-primary mr-1" @click="create"><i class="fas fa-check-circle"></i> Create
      </button>
      <button v-else class="btn btn-primary mr-1" @click="modify"><i class="fas fa-check-circle"></i> Modify </button>
    </div>

  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";

export default {
  name: "CreateEvent",
  props: ['id', 'name', 'owner', 'table', 'timestamp', 'attributes', 'targetTable', 'condition'],
  computed: {
    ...mapGetters("meta", ['metaNames', 'error'])
  },
  watch: {
    error(newError) {
      if (newError) {
        this.errorMessage = newError.message;
        this.$notify.error('Error Occurred While Creating: ' + this.errorMessage)
      }
    }
  },
  methods: {
    create() {
      let newLogTest = {
        id: this.id,
        name: this.name,
        owner: this.owner,
        table: this.table,
        condition: this.condition,
        event_timestamp: this.timestamp,
        event_target: this.targetTable,
        attributes: this.attributes
      }
      this.$store.dispatch('log/addLog', newLogTest)
        .then(id => {
          this.$notify.success("Change log was created successfully.");
          this.$emit('created', id);
        })
        .catch(e => {
          this.$notify.error("The creation failed: " + e);
        });
    },
    modify() {
      let newLogTest = {
        id: this.id,
        name: this.name,
        owner: this.owner,
        table: this.table,
        condition: this.condition,
        event_timestamp: this.timestamp,
        event_target: this.targetTable,
        attributes: this.attributes
      }
      this.$store.dispatch('log/updateLog', newLogTest)
        .then(id => {
          this.$notify.success("Change log was modified successfully.");
          this.$emit('change', id);
        })
        .catch(e => {
          this.$notify.error("The creation failed: " + e);
        });
    }
  },
};
</script>

<style scoped></style>