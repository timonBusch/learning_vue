<script setup lang="ts">

</script>

<template>
  <nav class="navbar sticky-top navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/">Naue Demo</RouterLink>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav w-100 justify-content-center">
          <li class="nav-item">
            <RouterLink class="nav-link" to="/products">Products</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/orders">Orders</RouterLink>
          </li>
        </ul> 
      </div>
    </div>
  </nav>

  <div class="d-flex justify-content-center">
    <div class="container w-100 m-3 border border-dark-subtle rounded min-vh-100">
        <RouterView />
    </div>
  </div>
  

</template>

<style scoped>

</style>
