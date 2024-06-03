<template>
  <div class="Box">
    <div class="Box-header">
      <h3 v-if="id == -1" class="Box-title">Create an Event Mapper</h3>
      <h3 v-else class="Box-title">Modify Event Mapper</h3>
    </div>

    <form>
      <div class="overflow-auto">
        <div class="Box-body overflow-auto">

          <div class="form-group">
            <div class="form-group-header">
              <label for="hostname" class="required">Event Mapper Name</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder='e.g. Create Purchase Requisition'
                id="table" v-model="name" required />
            </div>
          </div>

          <div class="form-group-body">
            <div class="form-group-header">
              <label for="selectedLog" class="required">Reference Change Log</label>
            </div>
            <select class="form-select element-drop" id="log-elements" v-model="selectedLog">
              <option disabled value="">Please select...</option>
              <option v-for="item in changeLogNames" :value="item.id" :key="item.id">{{ item.name }}</option>
            </select>
          </div>

          <!--div v-if="selectedLog" class="form-group-body">
            <div class="form-group-header">
              <label for="object_id" class="required">Object ID</label>
            </div>
            <select class="form-select element-drop" id="object-id" v-model="object_id">
              <option disabled value="">Please select...</option>
              <option v-for="item in selectedChangeLogColumns" :value="item" :key="item">{{ item }}</option>
            </select>
          </div>

          <div v-if="selectedLog" class="form-group-body">
            <div class="form-group-header">
              <label for="event_action" class="required">Event action type</label>
            </div>
            <select class="form-select element-drop" id="event-action" v-model="event_action">
              <option disabled value="">Please select...</option>
              <option v-for="item in selectedChangeLogColumns" :value="item" :key="item">{{ item }}</option>
            </select>
          </div>

          <div v-if="selectedLog" class="form-group-body">
            <div class="form-group-header">
              <label for="event_data" class="required">Event date</label>
            </div>
            <select class="form-select element-drop" id="event-data" v-model="event_data">
              <option disabled value="">Please select...</option>
              <option v-for="item in selectedChangeLogColumns" :value="item" :key="item">{{ item }}</option>
            </select>
          </div>
          
          <div class="form-group">
						<div class="form-group-body">
							<select class="form-select element-drop" id="route-elements" v-model="selectedOption">
								<option disbaled value="">Choose Objects</option>
								<option v-for="item in $store.compact.routeElements" :value="item">{{ item }}</option>
							</select>
							<button class="btn" @click.prevent="addElement"><i class="fas fa-plus-circle"></i></button>
						</div>
          </div>

          <div v-if="selectedLog" class="form-group-body">
            <div class="form-group-header">
              <label for="selectedColumns" class="required">Choose Event Attributes</label>
            </div>
            <select class="form-select element-drop" id="log-elements" v-model="selectedColumns">
              <option disabled value="">Please select...</option>
              <option v-for="item in selectedChangeLogColumns" :value="item" :key="item">{{ item }}</option>
            </select>
          </div-->

          <div class="form-group">
            <div class="form-group-header">
              <label for="username">Condition</label>
            </div>
            <div class="form-group-body">
              <input class="form-control width-full" type="text" placeholder="" id="condition" v-model="condition" />
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
  name: "CreateEvent",
  props: {
    id: {
      type: Number,
      default: -1
    },
    name: {
      type: String,
      default: ''
    },
    selectedLog: {
      type: Number,
      default: ''
    },
    selectedColumns: {
      type: String,
      default: ''
    },
    condition: {
      type: String,
      default: ''
    },
    object_id: {
      type: String,
      default: ''
    },
    p_objects: {
      type: Array,
      default: []
    },
  },
  data() {
    return {
      selectedOption: '',
      objects: JSON.parse(JSON.stringify(this.p_objects)),
    }
  },
  computed: {
    ...mapGetters('log', ['changeLogNames']),
    ...mapGetters('objects', ['objectNames']),
    selectedChangeLogColumns() {
      if (this.selectedLog) {
        let c = this.changeLogNames.find(item => item.id == this.selectedLog).columns
        return c
      }
      return []
    },
    allObjects() {
      return this.objectNames.filter(obj => !this.objects.some(object => object.id === obj.id));
    },
  },
  methods: {
    create() {
      if (!(this.name)) {
        this.$notify.error("Please fill all mandatory fields.");
        return
      }
      let newEvent = {
        name: this.name,
        change_log: this.selectedLog,
        objects: this.objects.map(object => object.id),
        condition: this.condition
      }
      this.$store.dispatch('events/addEvent', newEvent)
        .then(id => {
          this.$emit('created', id);
        })
        .catch(e => {
          this.$notify.error(`The creation failed: ` + e.response.data);
        });
    },
    modify() {
      if (!(this.name)) {
        this.$notify.error("Please fill all mandatory fields.");
        return
      }
      let newEvent = {
        id: this.id,
        name: this.name,
        change_log: this.selectedLog,
        objects: this.objects.map(object => object.id),
        condition: this.condition
      }
      this.$store.dispatch('events/updateEvent', newEvent)
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
}
</script>

<style scoped></style>