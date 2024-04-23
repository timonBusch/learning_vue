<script setup lang="ts">
import type { Ref } from "vue";
import {onMounted, ref } from "vue";
import Product from "./Product.vue";

interface Product {
  id: number
  width: number,
  name: string,
  length: number
}

const products: Ref<Product[]> = ref([])
const isLoading = ref(true)
const url = "http://127.0.0.1:8000/products/?skip=0&limit=100"

onMounted(async() => {
  const result = await fetch(url)
  const response = await result.json()
  products.value = response
  isLoading.value = false
})
</script>

<template>
  <div class="d-flex flex-wrap">
    <div v-if="isLoading">Loading...</div>
    <Product v-else v-for="product in products" :key="product.id" v-bind="product"/>
  </div>
  
</template>

<style scoped>

</style>
