<template>
  <div>
    <h4>Join Condition</h4>
    <p>
      <select v-model="join.leftTable">
        <option v-for="table in tables" :key="table">{{ table }}</option>
      </select>
      <select v-model="join.leftColumn">
        <option v-for="column in columnsLeft" :key="column">{{ column }}</option>
      </select>
      =
      <select v-model="join.rightTable">
        <option v-for="table in tables" :key="table">{{ table }}</option>
      </select>
      <select v-model="join.rightColumn">
        <option v-for="column in columnsRight" :key="column">{{ column }}</option>
      </select>
    </p>
  </div>
</template>

<script>
export default {
  name: 'JoinConditionComponent',
  props: ['join'],
  data() {
    return {
      tables: ['table1', 'table2'], // TODO: Replace with actual table names
      columnsLeft: ['column1', 'column2'], // TODO: Replace with actual column names
      columnsRight: ['column3', 'column4'], // TODO: Replace with actual column names
    };
  },
};
</script>
