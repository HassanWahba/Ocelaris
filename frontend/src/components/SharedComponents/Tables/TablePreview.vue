<template>
  <table class="table">
    <thead>
      <tr>
        <th v-for="(header, index) in headers" :key="index">{{ header.text }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in items" :key="index">
        <td v-for="(header, index) in headers" :key="index">{{ item[header.value] }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "TablePreview",
  props: {
    headers: {
      type: Array,
      required: true
    },
    items: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 1rem;
  border: 1px solid #e1e4e8;
}

.table thead {
  background-color: #f6f8fa;
}
</style>
