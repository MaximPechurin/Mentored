<template>
  <div class="crm-table-wrap">
    <div v-if="loading" class="crm-table-loading">
      <div class="crm-table-spinner"></div>
      <p>Cargando...</p>
    </div>

    <div v-else-if="rows.length === 0" class="crm-table-empty">
      {{ emptyText }}
    </div>

    <table v-else class="crm-table">
      <thead>
        <tr>
          <th
            v-for="col in columns"
            :key="col.key"
            :class="[col.align ? `align-${col.align}` : '', { sortable: col.sortable }]"
            @click="col.sortable && onSort(col.key)"
          >
            {{ col.label }}
            <span v-if="col.sortable" class="sort-icon">
              <template v-if="ordering === col.key">▲</template>
              <template v-else-if="ordering === `-${col.key}`">▼</template>
              <template v-else>⇅</template>
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="row in rows"
          :key="row.id"
          :class="{ clickable: clickable }"
          @click="clickable && $emit('row-click', row)"
        >
          <td
            v-for="col in columns"
            :key="col.key"
            :class="col.align ? `align-${col.align}` : ''"
          >
            <slot :name="col.key" :row="row">
              {{ row[col.key] ?? '—' }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const props = defineProps({
  columns: { type: Array, required: true },  // [{key, label, align?, sortable?}]
  rows: { type: Array, required: true },
  loading: { type: Boolean, default: false },
  emptyText: { type: String, default: 'Sin datos.' },
  clickable: { type: Boolean, default: false },
  ordering: { type: String, default: '' },
})

const emit = defineEmits(['row-click', 'update:ordering'])

const onSort = (key) => {
  let next
  if (props.ordering === key) {
    next = `-${key}`
  } else if (props.ordering === `-${key}`) {
    next = ''
  } else {
    next = key
  }
  emit('update:ordering', next)
}
</script>

<style scoped>
.crm-table-wrap {
  background: #ffffff;
  border: 1px solid #ece7e1;
  border-radius: 16px;
  overflow: hidden;
}

.crm-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14.5px;
}

.crm-table thead {
  background: #faf6f0;
}

.crm-table th {
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #8a8079;
  padding: 14px 16px;
  border-bottom: 1px solid #ece7e1;
  white-space: nowrap;
}

.crm-table th.sortable {
  cursor: pointer;
  user-select: none;
}

.crm-table th.sortable:hover {
  color: #15110f;
}

.sort-icon {
  margin-left: 6px;
  font-size: 10px;
  color: #c9bca6;
}

.crm-table td {
  padding: 14px 16px;
  border-bottom: 1px solid #f5f0e8;
  color: #3a342e;
  vertical-align: middle;
}

.crm-table tbody tr:last-child td {
  border-bottom: none;
}

.crm-table tbody tr.clickable {
  cursor: pointer;
  transition: background 0.15s;
}

.crm-table tbody tr.clickable:hover {
  background: #faf6f0;
}

.align-right { text-align: right; }
.align-center { text-align: center; }

.crm-table-loading,
.crm-table-empty {
  padding: 60px 20px;
  text-align: center;
  color: #8a8079;
  font-size: 15px;
}

.crm-table-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #e4ddd2;
  border-top: 3px solid #8e1519;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 12px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>