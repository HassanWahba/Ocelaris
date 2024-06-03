<template>
  <div class="overflow-auto">
    <div class="Box-body overflow-auto">
      <form>
        <div class="form-group">
          <div class="form-group-header">
            <label for="sql-text">Create Object Mapper: SQL Query</label>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="name" class="required">Object Mapper Name</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder='Purchase Order' id="name" v-model="name"
                required />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="object_id" class="required">ID Column</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder='PO_ID' id="object_id" v-model="object_id"
                required />
            </div>
          </div>

          <div class="form-group" v-for="(attribute, index) in attributes" :key="index">
            <div class="form-group-body">
              <label :for="'attribute_column'">Attribute Column</label>
              <input class="form-control" style="width: 40%;" type="text" :id="'attribute_column_' + index"
                v-model="attribute.attribute_column" />
              <label :for="'attribute_column'">Timestamp Column</label>
              <input class="form-control" type="text" style="width: 40%;" :id="'timestamp_column_' + index"
                v-model="attribute.timestamp_column" />
            </div>
          </div>

          <div class="form-group">
            <button type="button" class="btn btn-secondary" @click.prevent="addAttribute">Add Attribute</button>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="from" class="required">From</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder='PO.PO_HEADERS_ALL' id="from"
                v-model="from" required />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="condition" class="">Condition</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder='' id="condition" v-model="condition"
                required />
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-header">
              <label for="selected-objs">Selected Object Mappers</label>
            </div>
            <div class="form-group-body" v-for="(object, index) in objects" :key="index">
              <button class="btn btn-danger" @click.prevent="removeObject(object)"><i
                  class="far fa-trash-alt"></i></button>
              <label type="text" :id="'object_' + index"> {{ object.name }} </label>
            </div>
          </div>

          <div class="form-group">
            <div class="form-group-body">
              <select class="form-select element-drop" style="width: 200pt;" id="selectedOption"
                v-model="selectedOption">
                <option disbaled value="">Choose Object Mappers</option>
                <option v-for="item in allObjects" :value="item">{{ item.name }}</option>
              </select>
              <button class="btn" @click.prevent="addObject"><i class="fas fa-check-circle"></i></button>
            </div>
          </div>

        </div>
      </form>

      <div class="Box-footer">
        <button v-if="id == -1" class="btn btn-primary mr-1" @click="createFromSQL"><i class="fas fa-check-circle"></i>
          Create </button>
        <button v-else class="btn btn-primary mr-1" @click="changeFromSQL"><i class="fas fa-check-circle"></i> Modify
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "CreateSQLObject",
  props: {
    id: String,
    name: String,
    from: String,
    condition: String,
    object_id: String,
    p_objects: {
      type: Array,
      default: []
    },
    attributes: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      errorMessage: '',
      selectedOption: '',
      objects: JSON.parse(JSON.stringify(this.p_objects))
    };
  },
  computed: {
    ...mapGetters('objects', ['objectNames']),
    allObjects() {
      return this.objectNames.filter(obj => !this.objects.some(object => object.id === obj.id) && obj.id !== this.id);
    }
  },
  methods: {
    createFromSQL() {
      this.$store.dispatch("objects/addSQLObject", {
        attributes: this.attributes,
        object_id: this.object_id,
        from_tables: this.from,
        condition: this.condition,
        name: this.name,
        objects: this.objects.map(object => object.id)
      }).then(id => {
        this.$emit('created', id);
        this.$notify.success("Object mapper was changed successfully.");
      });
    },
    addAttribute() {
      this.attributes.push({ attribute_column: '', timestamp_column: '' });
      this.$emit('updated');
    },
    checkAttribute() {
      this.attributes = this.attributes.filter(attribute => attribute.attribute_column.trim() !== '');
    },
    changeFromSQL() {
      if (this.name.trim() === '') {
        this.$notify.error('Please insert a name for the new object mapper.')
        return
      }
      this.$store.dispatch("objects/updateSQLObject", {
        id: this.id,
        attributes: this.attributes,
        object_id: this.object_id,
        from_tables: this.from,
        condition: this.condition,
        name: this.name,
        objects: this.objects.map(object => object.id)
      }).then(id => {
        this.$emit('modified', id);
      });
    },
    addObject() {
      if (this.selectedOption) {
        this.objects.push(this.selectedOption);
        this.selectedOption = '';
      }
    },
    removeObject(object) {
      let index = this.objects.indexOf(object);
      if (index > -1) {
        this.objects.splice(index, 1);
      }
    }
  }
};
</script>

<style scoped></style>
