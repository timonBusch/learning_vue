<script setup lang="ts">
import Order from "../components/orders/Order.vue"
import { onMounted, ref } from "vue"
import type { Ref } from "vue";
import VueDatePicker from "@vuepic/vue-datepicker"

interface Item {
    id: number
    product_id: number
    order_id: number
    quantity: number
}

interface Order {
    capture_date: string,
    id: number,
    customer_id: number,
    delivery_date: string,
    items: Item[]
}

const url = "http://127.0.0.1:8000/orders/1/"

const orders: Ref<Order[]> = ref([])
const isLoading = ref(true)
const date = ref()

const format = (date: Date) => {
    const day = date.getDate()
    const month = date.getMonth() + 1
    const year = date.getFullYear()

    return `${year}-0${month}-${day}`
}

async function load_orders() {
    const result = await fetch(url)
    const response = await result.json()
    orders.value = response
    isLoading.value = false
}

onMounted(load_orders)

async function updateOrder(order: Order, event: Event) {
    if(event) {
        await fetch(`http://127.0.0.1:8000/orders/${order.id}/?delivery_date=${format(date.value)}`, {
        method: "PUT",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        })
        load_orders()
    }
}


</script>

<template>
    <h1>Orders</h1>
    <div v-if="isLoading">Loading...</div>
    <div class="mt-4" v-else v-for="order in orders" :key="order.id">
        <div v-if="!order.delivery_date">
            <Order v-bind="order"/>
            <VueDatePicker v-model="date" :format="format"></VueDatePicker>
            <button @click="(event) => updateOrder(order, event)" type="button" class="btn btn-primary mt-3" :class="{disabled: !date}">Submit order</button>
        </div>
    </div>
    
    <div class="accordion accordion-flush border mt-5" id="accordionFlushExample">
        <div class="accordion-item">
            <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
                Submitted Orders
            </button>
            </h2>
            <div id="flush-collapseOne" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
            <div v-for="order in orders" :key="order.id" class="accordion-body">
                <Order v-if="order.delivery_date" v-bind="order"/>
            </div>
            </div>
        </div>
    </div>
</template>
  
