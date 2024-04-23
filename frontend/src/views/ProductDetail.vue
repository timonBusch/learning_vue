<script setup lang="ts">
import { ref, onMounted } from "vue"

interface Props {
  id: string
}

const props = defineProps<Props>()
const product = ref()
const isLoading = ref(true)
const squareMeter = ref()
const quantity = ref()
const customer = ref()
const current_order = ref()

onMounted(async () => {
  const result = await fetch(`http://127.0.0.1:8000/products/${props.id}`)
  const response = await result.json()
  product.value = response

  const result_customer = await fetch("http://127.0.0.1:8000/customers/1/")
  const response_customer = await result_customer
  if (await response_customer.ok) {
    customer.value =  await response_customer.json()
  }

  const result_orders = await fetch("http://127.0.0.1:8000/orders/1/")
  const response_orders = await result_orders
  if (await response_orders.ok) {
    const orders = await response_orders.json()
    orders.forEach((order: any) => {
      if (!order.delivery_date) {
        current_order.value = order
      }
    });
  }

  isLoading.value = false
})


function calc_rolls(event: Event) {
  if(event) {
     quantity.value = Math.ceil(squareMeter.value / (product.value.length * product.value.width))
  }
}

async function create_order(event: Event) {
  if(event) {
    if(!current_order.value) {
      const date = new Date()
      const newDate = date.getUTCFullYear() + "-0" + (date.getUTCMonth() + 1) + "-" + date.getUTCDate()
      const response_order = await fetch(`http://127.0.0.1:8000/orders/1/`, {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({capture_date: newDate})
      })
      current_order.value = await response_order.json()
    }

    const response_order_item = await fetch("http://127.0.0.1:8000/order_items/", {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({product_id: parseInt(props.id), order_id: current_order.value.id, quantity: quantity.value})
      })
      if (await response_order_item.ok) {
        alert("OK")
      }
    
  }
}
</script>

<template>
  <p v-if="isLoading">Loading...</p>
  <div v-else>
    <h1>{{ product.name }}</h1>
    <p>Width: {{ product.width + " meter" }}</p>
    <p>Length: {{ product.length + " meter" }}</p>
    <div v-if="customer" class="d-flex">
      <button @click="create_order" type="button" class="btn btn-primary" :class="{disabled: !quantity}">Add to order</button>
      <input v-model="quantity" type="text" class="form-control ms-3" id="quantity" style="max-width: 40px;">
    </div>
    <h1 class="mt-5">Calculate Rolls</h1>
    <div class="row mb-3">
      <label for="squareMeter" class="col-sm-2 col-form-label">Square meter:</label>
      <div class="col-sm-10">
        <input v-on:input="calc_rolls" v-model="squareMeter" type="text" class="form-control form-control-sm" id="squareMeter">
      </div>
      <p v-if="quantity">Rolls: {{ quantity }}</p>
    </div>
    <button @click="create_order" v-if="customer" :class="{disabled: !squareMeter}" type="button" class="btn btn-primary">Add to order</button>
  </div>
</template>

<style scoped>

</style>
