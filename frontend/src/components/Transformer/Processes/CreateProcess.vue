<template>
  <div class="Box">
    <div class="Box-header">
      <h3 class="Box-title">Create a New Processe</h3>
    </div>

    <form>
      <div class="overflow-auto">
        <div class="Box-body overflow-auto">
          <div class="form-group">
            <div class="form-group-header">
              <label for="name" class="required">Process Name</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder='e.g. P2P' id="table" v-model="name"
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
      </div>
    </form>
    <div class="Box-footer">
      <button v-if="id == -1" class="btn btn-primary mr-1" @click="create"><i class="far fa-check-circle"></i> Create
      </button>
      <button v-else class="btn btn-primary mr-1" @click="modify"><i class="fas fa-check-circle"></i> Modify </button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "CreateProcess",
  props: {
    id: {
      type: Number,
      default: -1
    },
    name: {
      type: String,
      default: ''
    },
    p_objects: {
      type: Array,
      default: function () {
        return [];
      }
    },
  },
  data() {
    return {
      selectedOption: '',
      objects: JSON.parse(JSON.stringify(this.p_objects)),
    }
  },
  computed: {
    ...mapGetters('objects', ['objectNames']),
    allObjects() {
      return this.objectNames.filter(obj => !this.objects.some(object => object.id === obj.id));
    }
  },
  methods: {
    create() {
      if (!(this.name)) {
        this.$notify.error("Please fill all mandatory fields.");
        return
      }
      let newProcess = {
        name: this.name,
        objects: this.objects.map(object => object.id),
      }
      this.$store.dispatch('processes/addProcess', newProcess)
        .then(id => {
          this.$emit('created', id);
        })
        .catch(e => {
          this.$notify.error("The creation failed: " + e);
        });

    },
    modify() {
      if (!(this.name)) {
        this.$notify.error("Please fill all mandatory fields.");
        return
      }
      let newProcess = {
        id: this.id,
        name: this.name,
        objects: this.objects.map(object => object.id),
      }
      this.$store.dispatch('processes/updateProcess', newProcess)
        .then(id => {
          this.$emit('modify', id);
        })
        .catch(e => {
          this.$notify.error(`The modification was unsuccessful: ` + e.response.data);
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
  },
};
</script>

<style scoped></style>