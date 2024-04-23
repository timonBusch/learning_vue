<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

interface Props {
    id: number
    product_id: number
    order_id: number
    quantity: number
}

const props = defineProps<Props>()
    const url = computed(() => {
    return `http://127.0.0.1:8000/products/${props.product_id}`
}) 

const product = ref()
const isLoading = ref(true)

onMounted(async() => {
  const result = await fetch(url.value)
  const response = await result.json()
  product.value = response
  isLoading.value = false
})

</script>

<template>

    <div v-if="isLoading">Loading...</div>
    <div v-else>
        <p>Type: {{product.name}}</p>
        <p>Quantity: {{ quantity }}</p>
    </div>
    <hr>
    
</template>