<script setup lang="ts">

import OrderItem from "./OrderItem.vue"

interface Item {
    id: number
    product_id: number
    order_id: number
    quantity: number
}
interface Props {
  id: number
  delivery_date: string
  capture_date: string 
  customer_id: number
  items: Item[]
}

const props = defineProps<Props>()

</script>

<template>
    <div class="d-flex flex-row justify-content-between">
        <h3>Order {{ props.id }}</h3>
        <div class="d-flex">
            <p v-if="props.delivery_date" class="me-3">Delivery Date: {{ props.delivery_date }}</p>
            <p>Capture Date: {{ props.capture_date }}</p>
        </div>
    </div>
    <OrderItem v-for="item in props.items" :key="item.id" v-bind="item"/>
</template>