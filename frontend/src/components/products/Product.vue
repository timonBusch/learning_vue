<script setup lang="ts">
import { computed } from "vue"

interface Props {
  id: number
  width: number
  length: number
  name: string
}

const props = defineProps<Props>()

const productRoute = computed(() => {
  return "/product/" + props.id 
})
</script>

<template>
  <div class="card m-3" style="width: 18rem;">
    <div class="card-body">
      <h5 class="card-title">{{ props.name }}</h5>
    </div>
    <div class="card-footer">
      <RouterLink class="btn btn-primary" :to="productRoute">Details</RouterLink>
    </div>
  </div>
  
</template>

<style scoped>

</style>
