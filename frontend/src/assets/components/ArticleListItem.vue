<template>
<tr class="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700 border-gray-200">
    <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
        {{ book.article }}
    </th>
    <td class="px-6 py-4">
        {{ book.issue_date }}
    </td>
    <td class="px-6 py-4">
        {{ book.due_date }}
    </td>
</tr>
</template>

<script setup>
import { defineProps } from 'vue';
defineProps({
  book: {
    type: Object,
    required: true
  }
});
</script>