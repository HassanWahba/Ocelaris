<template>
  <div class="Box">
    <div class="Box-header">
      <h3 class="Box-title">Create a New Meta Information Table</h3>
    </div>

    <div class="overflow-auto">
      <div class="Box-body overflow-auto">
        <form>
          <div class="form-group">
            <div class="form-group-header">
              <label for="name" class="required">Meta Table Name</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder='e.g. My Awsome Table' id="table"
                v-model="name" required />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="source_table" class="required">Source Table</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text"
                placeholder='e.g. "DD02L" or "DD02L JOIN DD03M ON DD02L.id=DD03M.id" ' id="source_table"
                v-model="source_table" required />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="tables" class="required">Column contains table names</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder="e.g. TABNAME, TABLE_NAME" id="tables"
                v-model="tables" required />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="owner" class="required">Column contains table owners</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder="e.g. TABNAME, TABLE_NAME" id="owner"
                v-model="owner" required />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="condition">Condition</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text"
                placeholder='e.g. DD03M.TABCLASS = "TRANSP" OR DD02L.CreationDate LIKE "2017%"' id="condition"
                v-model="condition" />
            </div>
          </div>

        </form>
      </div>
      <div class="Box-footer">
        <button class="btn btn-primary mr-1" @click="create"><i class="fas fa-check-circle"></i> Create </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CreateMeta",
  props: ['name', 'source_table', 'condition', 'owner', 'tables', 'columns'],
  methods: {
    create() {
      if (!(this.name && this.source_table && this.tables && this.owner)) {
        this.$notify.error("Please fill all mandatory fields.");
        return
      }
      let newMetaTableTest = {
        name: this.name,
        source_table: this.source_table,
        condition: this.condition,
        owner_column: this.owner,
        tables_column: this.tables,
        attributes: this.attributes,
      }
      this.$store.dispatch('meta/addMetaTable', newMetaTableTest)
        .then(id => {
          this.$emit('created', id);
        });
    },
  },
};
</script>

<style scoped></style>